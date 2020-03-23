"""
/***************************************************************************
Name                 : Default Search Configuration Implementation
Description          : Default implementation for search configuration
Date                 : 09/March/2020
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
from collections import OrderedDict
from PyQt4.QtGui import QWidget

from stdm.settings.search_config import (
    AbstractSearchConfiguration,
    AbstractSearchConfigurationLoader,
    SearchConfigurationRegistry
)

from stdm.ui.flts.search.search_widgets import FltsSearchWidget


def search_widget_factory(config):
    return FltsSearchWidget(config)


class FltsSearchConfiguration(AbstractSearchConfiguration):
    """
    Default implementation for use in the FLTS.
    """
    def __init__(self, **kwargs):
        self._create_widget_func = kwargs.pop('create_widget_func', None)
        super(FltsSearchConfiguration, self).__init__(**kwargs)

    def create_widget(self):
        return self._create_widget_func(self)


class FltsSearchConfigurationLoader(AbstractSearchConfigurationLoader):
    """
    Loads search configuration specified in the FLTS search_config.INI file.
    """
    DATA_SOURCE = 'DataSource'
    ICONS = 'Icon'
    BASE_ICON_PATH = ':/plugins/stdm/images/icons/'

    def _load_configs(self):
        # Get data source section and create configuration objects
        data_src_mapping = self._config_parser.items(self.DATA_SOURCE)
        for dsm in data_src_mapping:
            data_source = dsm[0]
            config = self._create_config(data_source, dsm[1])
            self._configs[data_source] = config

    def _create_config(self, data_source, display_name):
        # Create config for the given data source.
        column_map = self._column_mapping(data_source)
        icon_file = self._icon(data_source)
        args = {
            'data_source': data_source,
            'display_name': display_name,
            'column_mapping': column_map,
            'icon': icon_file,
            'create_widget_func': search_widget_factory
        }

        return FltsSearchConfiguration(**args)

    def _column_mapping(self, data_source):
        # Create column mapping for the given data source.
        col_mapping = OrderedDict()
        if self._config_parser.has_section(data_source):
            col_items = self._config_parser.items(data_source)
            col_mapping.update(col_items)

        return col_mapping

    def _icon(self, data_source):
        # Gets the icon file name for the given data source.
        if self._config_parser.has_option(self.ICONS, data_source):
            icon_file = self.BASE_ICON_PATH + self._config_parser.get(
                self.ICONS, data_source
            )
        else:
            icon_file = ''

        return icon_file
