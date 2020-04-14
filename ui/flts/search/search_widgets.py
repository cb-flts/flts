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
    QCompleter,
    QDialog,
    QDockWidget,
    QIcon,
    QStackedWidget,
    QWidget
)

from PyQt4.QtCore import (
    Qt
)

from qgis.core import (
    QgsExpression,
    QgsFeatureRequest
)
from qgis.gui import (
    QgsExpressionBuilderDialog
)

from stdm.settings.search_config import SearchConfigurationRegistry
from stdm.data.pg_utils import (
    columnType,
    pg_table_exists,
    table_column_names,
    vector_layer
)
from stdm.data.flts.search import (
    column_searches,
    save_column_search
)
from stdm.utils.util import clone_vector_layer
from stdm.ui.notification import NotificationBar, ERROR
from stdm.ui.flts.search.search_model import SearchResultsModel
from stdm.ui.flts.search.sort_dialog import SortColumnDialog
from stdm.ui.flts.search.operators import (
    PG_QUOTE_TYPES,
    PG_TYPE_EXPRESSIONS,
    operator_format_value
)
from ui_flts_search_widget import Ui_FltsSearchWidget


class FltsSearchDockWidget(QDockWidget):
    """
    Dock widget for showing search widgets with each widget corresponding to
    a search configuration.
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


class FltsSearchException(Exception):
    """
    Exceptions related to search operations.
    """
    pass


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
        self._valid_filter_cols = OrderedDict()
        self._vector_layer = None
        self._column_types = {}

        # Set attributes if data source is valid
        if self._is_valid:
            self._geom_columns = table_column_names(
                self._config.data_source,
                True
            )
            self._valid_cols = self._validate_columns()
            self._valid_filter_cols = self._validate_filter_columns()

            # Use the first geometry column in the list. Hence, it is
            # important to ensure that each data has not more than one
            # geometry column.
            geom_col = self._geom_columns[0] if len(self._geom_columns) > 0 else ''
            self._vector_layer = vector_layer(
                self._config.data_source,
                layer_name=self._config.display_name,
                geom_column=geom_col
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
            # Set column type
            col_type = columnType(
                self._config.data_source,
                vc
            )
            if col_type:
                self._column_types[vc] = col_type

        return v_col_mapping

    def _validate_filter_columns(self):
        # Assert filter columns exist and create the mapping
        filter_col_mapping = OrderedDict()
        for fc in self._config.filter_columns:
            if fc in self._valid_cols:
                filter_col_mapping[fc] = self._valid_cols.get(fc)

        return filter_col_mapping

    @property
    def search_config(self):
        """
        :return: Returns the search configuration used in the widget.
        :rtype: FltsSearchConfiguration
        """
        return self._config

    @property
    def column_types(self):
        """
        :return: Returns a collection of the PostgreSQL/PostGIS column types
        for each validated column in the data source.
        :rtype: OrderedDict
        """
        return self._column_types

    def column_type(self, column_name):
        """
        Gets the PostgreSQL/PostGIS column type for the given column name.
        :param column_name: Column name for which the type is to be extracted.
        :type column_name: str
        :return: Returns the corresponding column type or an empty string if
        the column was not found.
        :rtype: str
        """
        return self._column_types.get(column_name, '')

    def column_type_expression(self, column_name):
        """
        Gets the matching expressions for the data type of the specified
        column.
        :param column_name: Column name for the required type expressions.
        :type column_name: str
        :return: Returns the matching expressions for the data type of the
        specified column or an empty collection if the column type was not
        found or the matching expression has not been specified.
        :rtype: dict
        """
        col_type = self.column_type(column_name)
        if not col_type:
            return {}

        return PG_TYPE_EXPRESSIONS.get(col_type, {})

    def format_value_by_operator(self, op, value):
        """
        Formats the search keywords based on the given search operator.
        :param op: Operator.
        :type op: str
        :param value: Search keyword to be formatted.
        :type value: object
        :return: Returns the formatted search keyword based on the
        pre-defined list of input value formatters, else returns the original
        value if not formatter function is defined for the given operator.
        :rtype: object
        """
        return operator_format_value(op, value)

    def quote_column_value(self, column_name):
        """
        True if the value of the given column requires to be quoted when
        used in a QgsExpression.
        :param column_name: Column name used to determine the type.
        :type column_name: str
        :return: Returns True if the value of the given column requires to be
        quoted when used in a QgsExpression, else False.
        :rtype: bool
        """
        c_type = self.column_type(column_name)
        if not c_type:
            return False
        if c_type in PG_QUOTE_TYPES:
            return True
        return False

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

    @property
    def filter_column_mapping(self):
        """
        :return: Returns a collection containing a validated mapping of
        filter columns.
        :rtype: OrderedDict
        """
        return self._valid_filter_cols

    def clone_source_layer(self):
        """
        :return: Returns a cloned memory vector layer. If the source vector
        layer is invalid then it returns None.
        :rtype: QgsVectorLayer
        """
        return clone_vector_layer(
            self._vector_layer,
            self._config.display_name
        )

    def search_data_source(self, search_expression, sort_map):
        """
        Searches the data source using the specified search expression.
        :param search_expression: Search expression either as a string or
        instance of QgsExpression.
        :type search_expression: str or QgsExpression
        :param sort_map: List containing a definition of column sorting.
        :type sort_map: list
        :return: Returns a list containing search results consisting of
        QgsFeature objects.
        :rtype: list
        """
        results = []
        if not self._vector_layer.isValid():
            raise FltsSearchException(
                'Search cannot be performed, data source is invalid.'
            )
        if isinstance(search_expression, basestring):
            search_expression = QgsExpression(search_expression)

        # Assert if there are errors in the expression
        if search_expression.hasParserError():
            raise FltsSearchException(
                search_expression.parserErrorString()
            )

        fr = QgsFeatureRequest(search_expression)
        if not self._config.limit:
            limit = -1
        else:
            limit = self._config.limit
        fr.setLimit(limit)

        # Set sorting if specified.
        if sort_map:
            for s in sort_map:
                ascending = True if s[1] == 0 else False
                fr.addOrderBy(s[0], ascending)

        feat_iter = self._vector_layer.getFeatures(fr)
        for f in feat_iter:
            results.append(f)

        return results


class BasicSearchQuery(object):
    """
    Container for the definition of basic search parameters.
    """
    def __init__(self, **kwargs):
        self.filter_column = kwargs.pop('filter_column', '')
        self.expression = kwargs.pop('expression', '')
        self.search_term = kwargs.pop('search_term', '')
        self.quote_column_value = False

    def is_valid(self):
        if not self.filter_column or not self.expression or not \
                self.search_term:
            return False

        return True

    def _quoted_column_value(self):
        # Quote filter column value if flag has been set.
        search_term = self.search_term.strip()
        if self.quote_column_value:
            search_term = '\'{0}\''.format(search_term)

        return search_term

    def expression_text(self):
        """
        :return: Builds a string search expression using the specified
        search parameters.
        :rtype: str
        """
        if not self.is_valid():
            return ''

        return u'"{0}" {1} {2}'.format(
            self.filter_column,
            self.expression,
            self._quoted_column_value()
        )


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

        # Sort dialog and mapping
        self._sort_dialog = None
        self._sort_map = None

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
        self.btn_sort.setEnabled(enable)

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
        # Connect signals
        self.btn_search.clicked.connect(
            self.on_basic_search
        )
        self.cbo_column.currentIndexChanged.connect(
            self._on_filter_col_changed
        )
        self.btn_clear.clicked.connect(
            self.clear_results
        )
        self.btn_advanced_search.clicked.connect(
            self.on_advanced_search
        )
        self.btn_sort.clicked.connect(
            self.on_sort_columns
        )
        self.txt_keyword.returnPressed.connect(
            self.on_basic_search
        )

        # Set filter columns
        self.cbo_column.clear()
        col_ico = QIcon(':/plugins/stdm/images/icons/column.png')
        for col, disp_col in self._ds_mgr.filter_column_mapping.iteritems():
            self.cbo_column.addItem(col_ico, disp_col, col)

        # Set model
        self._res_model = SearchResultsModel(self._ds_mgr)
        self.tb_results.setModel(self._res_model)
        self.tb_results.hideColumn(0)

        # Connect to item selection chnaged signal
        selection_model = self.tb_results.selectionModel()
        selection_model.selectionChanged.connect(
            self.on_selection_changed
        )

        self.txt_keyword.setFocus()

    def _on_filter_col_changed(self, idx):
        # Set the valid expressions based on the type of the filter column.
        self.cbo_expression.clear()
        self.txt_keyword.clearValue()
        if idx == -1:
            return

        filter_col = self.cbo_column.itemData(idx)
        filter_exp = self._ds_mgr.column_type_expression(filter_col)
        exp_ico = QIcon(':/plugins/stdm/images/icons/math_operators.png')
        for disp, exp in filter_exp.iteritems():
            self.cbo_expression.addItem(exp_ico, disp, exp)

        # Update the search completer
        self._set_search_completer()

    def _set_search_completer(self):
        # Set the completer for the search line edit for showing
        # previously saved searches.
        ds = self._config.data_source
        filter_col = self.cbo_column.itemData(
            self.cbo_column.currentIndex()
        )
        searches = column_searches(
            ds,
            filter_col
        )

        # Create and set completer
        completer = QCompleter(searches, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.txt_keyword.setCompleter(completer)

    def clear_results(self):
        """
        Removes any previous search results in the view.
        """
        self._res_model.clear_results()
        self._update_search_status(-1)

    def on_basic_search(self):
        """
        Slot raised to execute basic search.
        """
        # Validate if input parameters have been specified
        filter_col = ''
        msgs = []
        if not self.cbo_column.currentText():
            msgs.append('Filter column has not been specified.')
        else:
            filter_col = self.cbo_column.itemData(
                self.cbo_column.currentIndex()
            )

        filter_exp = None
        if not self.cbo_expression.currentText():
            msgs.append('Filter expression has not been specified.')
        else:
            filter_exp = self.cbo_expression.itemData(
                self.cbo_expression.currentIndex()
            )

        search_term = self.txt_keyword.value()
        if not search_term:
            msgs.append('Please specify the search keyword.')

        # Clear any previous notifications
        self.notif_bar.clear()

        # Insert warning messages
        for msg in msgs:
            self.notif_bar.insertWarningNotification(msg)

        if len(msgs) > 0:
            return

        # Save search and update completer with historical searches
        save_column_search(self._config.data_source, filter_col, search_term)
        self._set_search_completer()

        # Format the input value depending on the selected operator
        fm_search_term = self._ds_mgr.format_value_by_operator(
            filter_exp,
            search_term
        )

        # Build search query object
        search_query = BasicSearchQuery()
        search_query.filter_column = filter_col
        search_query.expression = filter_exp
        search_query.search_term = fm_search_term
        search_query.quote_column_value = self._ds_mgr.quote_column_value(
            filter_col
        )

        exp_text = search_query.expression_text()
        self.exec_search(exp_text)

    def exec_search(self, search_expression):
        """
        Execute a search operation based on the specified filter expression.
        :param search_expression: Filter expression.
        :type search_expression: str
        """
        self.clear_results()
        if not search_expression:
            msg = 'Search expression cannot be empty.'
            self.notif_bar.insertWarningNotification(msg)
            return

        try:
            results = self._ds_mgr.search_data_source(
                search_expression,
                self._sort_map
            )
            self._update_search_status(len(results))
            # Update model
            self._res_model.set_results(results)

            # Notify user if there are no results
            if len(results) == 0:
                self.notif_bar.insertInformationNotification(
                    'No results found matching the search keyword.'
                )
        except FltsSearchException as fe:
            self.notif_bar.insertWarningNotification(
                str(fe)
            )

    def _update_search_status(self, count=-1):
        # Updates search count label.
        txt = ''
        suffix = 'record' if count == 1 else 'records'
        if count != -1:
            # Separate thousand using comma
            cs_count = format(count, ',')
            txt = '{0} {1}'.format(cs_count, suffix)

        self.lbl_results_count.setText(txt)

    def on_advanced_search(self):
        # Slot raised to show the expression editor.
        filter_col = self.cbo_column.itemData(
            self.cbo_column.currentIndex()
        )
        start_txt = '"{0}" = '.format(filter_col)
        exp_dlg = QgsExpressionBuilderDialog(
            self._ds_mgr.vector_layer,
            start_txt,
            self,
            self._config.display_name
        )
        exp_dlg.setWindowTitle('{0} Expression Editor'. format(
            self._config.display_name)
        )
        if exp_dlg.exec_() == QDialog.Accepted:
            exp_text = exp_dlg.expressionText()
            self.exec_search(exp_text)

    def on_sort_columns(self):
        # Slot raised to show the sort column dialog
        col_mapping = self._ds_mgr.valid_column_mapping
        if not self._sort_dialog:
            self._sort_dialog = SortColumnDialog(
                col_mapping,
                self
            )

        if self._sort_dialog.exec_() == QDialog.Accepted:
            sort_map = self._sort_dialog.sort_mapping()
            if len(sort_map) > 0:
                self._sort_map = sort_map
            else:
                self._sort_map = None

    def selected_rows(self):
        """
        :return: Returns the row numbers of the selected results.
        :rtype: list
        """
        return [
            idx.row() for idx in self.tb_results.selectionModel().selectedRows()
        ]

    def selected_features(self):
        """
        :return: Returns a list of QgsFeatures corresponding to the selected
        results.
        :rtype: list
        """
        features = []
        for r in self.selected_rows():
            feat = self._res_model.row_to_feature(r)
            if feat:
                features.append(feat)

        return features

    def on_selection_changed(self, previous_selection, current_selection):
        # Slot raised when the selection changes in the results table.
        features = self.selected_features()