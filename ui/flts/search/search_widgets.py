"""
/***************************************************************************
Name                 : Search widgets
Description          : Widgets for searching various entities.
Date                 : 11/March/2020
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
from PyQt4.QtGui import (
    QDockWidget,
    QStackedWidget,
    QWidget
)
from PyQt4.QtCore import (
    Qt
)

from stdm.settings.search_config import SearchConfigurationRegistry
from stdm.data.pg_utils import (
    pg_table_exists,
    table_column_names,
    vector_layer
)
from stdm.ui.notification import NotificationBar, ERROR
from ui_flts_search_widget import Ui_FltsSearchWidget


class FltsSearchDockWidget(QDockWidget):
    """
    Dock widget for showing search widgets based on the search
    configuration.
    """
    def __init__(self, *args, **kwargs):
        super(FltsSearchDockWidget, self).__init__(*args, **kwargs)
        self.setAllowedAreas(Qt.BottomDockWidgetArea)
        self._search_reg = SearchConfigurationRegistry.instance()
        self._stack_widget = QStackedWidget(self)
        self.setWidget(self._stack_widget)

        # Index data source to their location in the stack widget
        self._search_widget_idx = dict()

    def show_search_widget(self, data_source):
        """
        Shows the search widget associated with the given data source. If
        not found then it will create a new one by using the factory
        method in the search configuration.
        :param data_source: Data source name.
        :type data_source: str
        :return: Returns True if the operation was successful else False. It
        will be false if the data source is not found in the registry.
        :rtype: bool
        """
        config = self._search_reg.search_config(data_source)
        if not config:
            return False

        # Set current search widget
        self._set_current_widget(config)

        return True

    def _set_current_widget(self, config):
        # Updates dock widget based on the specified config.
        data_source = config.data_source

        # Create widget if it does not exist in the stack
        if not data_source in self._search_widget_idx:
            search_widget = config.create_widget()
            idx = self._stack_widget.addWidget(search_widget)
            self._search_widget_idx[data_source] = idx
        else:
            idx = self._search_widget_idx[data_source]

        self._stack_widget.setCurrentIndex(idx)

        # Set title
        self.setWindowTitle(u'Search {0}'.format(config.display_name))

    def current_widget(self):
        """
        :return: Returns the current search widget or None if there are no
        widgets in the stack.
        :rtype: QWidget
        """
        return self._stack_widget.currentWidget()

    def clear(self):
        """
        Removes all the search widgets and resets the indices.
        """
        while self._stack_widget.count() > 0:
            sw = self._stack_widget.widget(0)
            self._stack_widget.removeWidget(sw)
            del sw

        self._search_widget_idx = dict()


class FltsSearchConfigDataSourceManager(object):
    """
    Provides data management functions based on a given search configuration
    object.
    """
    def __init__(self, search_config):
        self._config = search_config
        self._is_valid = self._validate_data_source()
        self._geom_columns = []
        self._valid_cols = OrderedDict()
        self._vector_layer = None

        # Set attributes if data source is valid
        if self._is_valid:
            self._geom_columns = table_column_names(
                self._config.data_source,
                True
            )
            self._valid_cols = self._validate_columns()
            self._vector_layer = vector_layer(
                self._config.data_source,
                layer_name=self._config.display_name
            )

    def _validate_data_source(self):
        # Check if the specified data source exists.
        status = pg_table_exists(self._config.data_source)
        is_valid = True
        if not status:
            is_valid = False

        return is_valid

    def _validate_columns(self):
        # Validates if the columns in the config exist in the data source.
        ds_set = set(table_column_names(self._config.data_source))
        conf_set = set(self._config.columns.keys())
        valid_cols_set = ds_set.intersection(conf_set)
        v_col_mapping = OrderedDict()
        for vc in valid_cols_set:
            v_col_mapping[vc] = self._config.columns.get(vc)

        return v_col_mapping

    @property
    def search_config(self):
        """
        :return: Returns the search configuration used in the widget.
        :rtype: FltsSearchConfiguration
        """
        return self._config

    @property
    def vector_layer(self):
        """
        :return: Returns the vector layer associated with the search
        configuration data source.
        :rtype: QgsVectorLayer
        """
        return self._vector_layer

    @property
    def is_valid(self):
        """
        :return: Returns True if the data source exists, else False.
        :rtype: bool
        """
        return self._is_valid

    @property
    def is_spatial(self):
        """
        :return: Returns True if the data source contains one or more geometry columns.
        :rtype: bool
        """
        return [True if len(self._geom_columns) > 0 else False]

    @property
    def geometry_columns(self):
        """
        :return: Returns a list of geometry column names in the data source.
        :rtype: list
        """
        return self._geom_columns

    @property
    def valid_column_mapping(self):
        """
        :return: Returns a validated collection of column mappings.
        :rtype: OrderedDict
        """
        return self._valid_cols


class FltsSearchWidget(QWidget, Ui_FltsSearchWidget):
    """
    Widget that provides an interface for searching data from a given data
    source specified in the search configuration.
    """
    def __init__(self, search_config):
        """
        :param search_config: Search configuration object.
        :type search_config: FltsSearchConfiguration
        """
        super(FltsSearchWidget, self).__init__(None)
        self.setupUi(self)
        self.notif_bar = NotificationBar(
            self.vlNotification
        )
        self._config = search_config
        self._ds_mgr = FltsSearchConfigDataSourceManager(self._config)

        # Check validity
        self._check_validity()
        if not self._ds_mgr.is_valid:
            return

        # Initialize UI
        self._init_gui()

    def _enable_controls(self, enable):
        # Enables or disables UI controls
        self.cbo_column.setEnabled(enable)
        self.cbo_expression.setEnabled(enable)
        self.txt_keyword.setEnabled(enable)
        self.btn_search.setEnabled(enable)
        self.btn_advanced_search.setEnabled(enable)
        self.btn_clear.setEnabled(enable)
        self.tb_results.setEnabled(enable)

    def _check_validity(self):
        # Notify is the data source is invalid.
        if not self._ds_mgr.is_valid:
            self._enable_controls(False)
            self.notif_bar.insertErrorNotification(
                u'\'{0}\' data source does not exist in the database.'.format(
                    self._config.data_source
                )
            )

    def _init_gui(self):
        # Initialize GUI controls.
        for col, disp_col in self._ds_mgr.valid_column_mapping.iteritems():
            self.cbo_column.addItem(disp_col, col)