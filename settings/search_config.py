"""
/***************************************************************************
Name                 : SearchConfiguration
Description          : Core classes for managing search configurations.
Date                 : 07/March/2020
copyright            : (C) 2020 by UN-Habitat and implementing partners.
                       See the accompanying file CONTRIBUTORS.txt in the root
email                : stdm@unhabitat.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from abc import (
    ABCMeta,
    abstractmethod
)
from collections import OrderedDict
from ConfigParser import ConfigParser
from PyQt4.QtGui import (
    QAction,
    QIcon,
    QWidget
)

from stdm.data.database import (
    Content,
    Singleton
)
from stdm.navigation.content_group import ContentGroup


class AbstractSearchConfiguration(object):
    """
    An abstract class that contains information about the search
    configuration for a given data source.
    """
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self._data_source = kwargs.pop('data_source', '')
        self._display_name = kwargs.pop('display_name', '')
        self._columns = kwargs.pop('column_mapping', OrderedDict())
        self._icon_file = kwargs.pop('icon', '')
        self._contains_geometry = False
        self._search_prefix = 'Search'

    @property
    def data_source(self):
        """
        :return: Returns the data source name.
        :rtype: str
        """
        return self._data_source

    @property
    def display_name(self):
        """
        :return: Returns a friendly display name for the data source.
        :rtype: str
        """
        return self._display_name

    @property
    def columns(self):
        """
        :return: Returns the collection of column names and corresponding
        display names in a dictionary.
        :rtype: OrderedDict
        """
        return self._columns

    def add_column(self, column_name, display_name):
        """
        Adds a column mapping to the collection.
        :param column_name: Column name in the data source.
        :type column_name: str
        :param display_name: User-friendly display name for the column. This
        will be used in the search widget.
        :type display_name: str
        """
        self._columns[column_name] = display_name

    def create_action(self):
        """
        Factory method that creates a QAction from the specified icon file
        and data source display name.
        :return: Returns a QAction object.
        :rtype: QAction
        """
        name = u'{0} {1}'.format(self._search_prefix, self._display_name)
        if not self._icon_file:
            icon = QIcon()
        else:
            icon = QIcon(self._icon_file)

        action = QAction(icon, name, None)
        action.setCheckable(True)
        action.setData(self._data_source)

        return action

    @abstractmethod
    def create_widget(self):
        """
        Factory method that returns the search widget for the search
        configuration. Should be implemented by sub-classes.
        :return: Returns the search widget for this configuration.
        :rtype: QWidget
        """
        raise NotImplementedError


class AbstractSearchConfigurationLoader(object):
    """
    Abstract loader that creates search configuration objects defined in an
    *.INI file.
    """
    __metaclass__ = ABCMeta

    def __init__(self, files):
        self._files = files
        self._configs = OrderedDict()

        # Creates config parser object that will read the INI file(s)
        self._config_parser = ConfigParser()
        self._config_parser.read(self._files)

        # Load search configurations
        self._load_configs()

    @abstractmethod
    def _load_configs(self):
        # To be implemented by subclasses specifying how the search
        # configuration objects should be created.
        raise NotImplementedError

    @property
    def configs(self):
        """
        :return: Returns the search configuration objects as specified in
        the specified *.INI file.
        :rtype: OrderedDict
        """
        return self._configs


@Singleton
class SearchConfigurationRegistry(object):
    """
    Container for managing search configuration objects.
    """
    def __init__(self, files=None, loader_cls=None):
        self._files = files
        self._config_loader_cls = loader_cls
        self._configs = OrderedDict()
        self._actions = OrderedDict()

        # Populate defaults
        self._populate_defaults()

    def _populate_defaults(self):
        # Load default search configuration objects defined in the source
        # files.
        if not self._files or not self._config_loader_cls:
            return

        # Loads the search configs defined in the files
        loader_obj = self._config_loader_cls(self._files)
        def_configs = loader_obj.configs
        for dc in def_configs.values():
            self.add_config(dc)

    def add_config(self, config):
        """
        Adds a search configuration to the registry. Items are indexed by the
        name of the data source hence if there exists a configuration object
        with the same, then it will be replaced.
        :param config: Object containing search config information.
        :type config: AbstractSearchConfiguration
        """
        self._configs[config.data_source] = config
        self._actions[config.data_source] = config.create_action()

    def search_config(self, data_source):
        """
        Gets the corresponding search configuration object based on the data
        source name.
        :param data_source: Name of the data source.
        :type data_source: str
        :return: Returns the matching search configuration object else None
        if not found.
        :rtype: AbstractSearchConfiguration
        """
        return self._configs.get(data_source, None)

    def action(self, data_source):
        """
        Gets the action corresponding to the given data source name.
        :param data_source: Data source name.
        :type data_source: str
        :return: Returns the matching action object else None.
        :rtype: QAction
        """
        return self._actions.get(data_source, None)

    def all(self):
        """
        :return: Returns a list containing all the search configuration
        objects in the registry.
        :rtype: list
        """
        return self._configs.values()

    def actions(self):
        """
        :return: Returns a list of QActions corresponding to the search
        configuration objects in the registry.
        :rtype: list
        """
        return self._actions.values()

    def content_items(self):
        """
        :return: Returns a collection of content times specifying permissions
        for the various search operations.
        :rtype: list
        """
        cnt_items = []

        for a in self.actions():
            c = Content()
            c.name = a.text()
            cnt_items.append(c)

        return cnt_items

    def content_group(self, username, container):
        """
        :param username: Name of the currently logged in user.
        :type username: str
        :param container" Container widget for the actions.
        :type container: QObject
        :return: Return a ContentGroup object for managing permissions
        related to the search actions in the registry.
        :rtype: ContentGroup
        """
        cnt_group = ContentGroup(username)
        cnt_group.setContainerItem(container)
        for ci in self.content_items():
            cnt_group.addContentItem(ci)

        return cnt_group

    def create_widget(self, data_source):
        """
        Creates a widget based on the factory method defined in the search
        configuration object that matches the specified in the data source.
        :param data_source: Name of the data source.
        :type data_source: str
        :return: Returns the widget specified in the search configutation
        object if it exists in the registry, else None.
        :rtype: QWidget
        """
        if not data_source in self._configs:
            return None

        return self._configs[data_source].create_widget()