"""
/***************************************************************************
Name                 : SearchResultsModel
Description          : Table model for search results.
Date                 : 31/March/2020
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
from datetime import datetime

from PyQt4.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt
)

from qgis.gui import QgsEditorWidgetRegistry


class SearchResultsModel(QAbstractTableModel):
    """Table model for rendering search results."""
    def __init__(self, ds_manager, parent=None):
        super(SearchResultsModel, self).__init__(parent)
        self._ds_manager = ds_manager
        self._vector_layer = self._ds_manager.vector_layer
        self._config = self._ds_manager.search_config
        self._res_features = []
        self._field_idx_name = {}
        # Store index of 'id' column
        self._id_col_idx = -1
        self._update_field_index_name()

        # Container for widget factories based on field type. Key: column
        # name, value: widget factory
        self._col_widget_factories = {}
        self._col_widget_config = {}
        self._col_cache = {}
        self._layer_col_idx = {}

        # Populate the column mappings
        self._populate_widget_factories()

    @property
    def datasource_manager(self):
        """
        :return: Returns the datasource manager used for the model.
        :rtype: FltsSearchConfigDataSourceManager
        """
        return self._ds_manager

    def _update_field_index_name(self):
        # Update the mapping of field names based on the index.
        col_names = self._ds_manager.valid_column_mapping.keys()
        self._field_idx_name = {i:col_names[i] for i in range(len(col_names))}

    def _populate_widget_factories(self):
        """
        We use the widget factories for proper representation of string
        values for different field types. This is preferred to writing custom
        value formatters based on the data type.
        """
        if not self._vector_layer.isValid():
            return

        fields = self._vector_layer.dataProvider().fields()
        for i in range(fields.count()):
            field_name = fields.at(i).name()
            widget_type = self._vector_layer.editFormConfig().widgetType(i)
            widget_factory = QgsEditorWidgetRegistry.instance().factory(
                widget_type
            )
            if widget_factory:
                self._col_widget_factories[field_name] = widget_factory
                widget_config = self._vector_layer.editFormConfig().\
                    widgetConfig(i)
                self._col_widget_config[field_name] = widget_config
                self._layer_col_idx[field_name] = i
                cache = widget_factory.createCache(
                    self._vector_layer,
                    i,
                    widget_config
                )
                self._col_cache[field_name] = cache

    def _column_string_representation(self, col_name, value):
        # Returns a friendly string representation of the column value.
        if not col_name in self._col_widget_factories:
            return value

        return self._col_widget_factories.get(col_name).representValue(
            self._vector_layer,
            self._layer_col_idx[col_name],
            self._col_widget_config[col_name],
            self._col_cache[col_name],
            value
        )

    def columnCount(self, index=QModelIndex()):
        # Returns number of columns based on the valid mapped columns in the
        # data source.
        return len(self._ds_manager.valid_column_mapping) + 1

    def rowCount(self, index=QModelIndex()):
        # Returns number of features in the results layer.
        return len(self._res_features)

    def headerData(self, section, orientation, role):
        # Set the horizontal and vertical header labels
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return 'fid'
            else:
                return self._column_display_name(section - 1)
        else:
            return int(section) + 1

        return None

    def _column_display_name(self, idx):
        # Returns the column display name based on the column index in the
        # validated column mapping.
        col_name = self._ds_manager.valid_column_mapping.keys()[idx]

        return self._ds_manager.valid_column_mapping[col_name]

    def data(self, index, role):
        # Returns the data in the memory layer for the item referred by index.
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        if row < 0 or row >= len(self._res_features):
            return None

        if role == Qt.DisplayRole:
            feat = self._res_features[row]
            if col == 0:
                return feat.id()
            else:
                # Get name from index
                col_name = self._field_idx_name.get((col - 1), '')
                if not col_name:
                    return None
                val = feat.attribute(col_name)
                return self._column_string_representation(col_name, val)

        return None

    @property
    def id_index(self):
        """
        :return: Returns the index of the column named 'id'. This can be
        used by the view to hide the column.
        :rtype: int
        """
        return self._id_col_idx

    def insertRows(self, position, count=1, index=QModelIndex()):
        # Insert rows to the table. Results be will added separately to the
        # list.
        self.beginInsertRows(QModelIndex(), position, position + count - 1)
        self.endInsertRows()

        return True

    def removeRows(self, position, count=1, index=QModelIndex()):
        # Remove items from the model.
        self.beginRemoveRows(QModelIndex(), position, position + count - 1)
        del self._res_features[position:position + count]
        self.endRemoveRows()

        return True

    def set_results(self, results):
        """
        Adds search results to the model.
        :param results: A list of QgsFeature objects consisting the search
        results.
        :type results: list
        """
        if len(results) == 0:
            return

        self.clear_results()
        self._res_features = results
        self.insertRows(
            0,
            len(results)
        )

    def clear_results(self):
        """
        Removes any previous search results in the model.
        """
        self.removeRows(0, len(self._res_features))
        self._res_features = []

