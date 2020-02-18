"""
/***************************************************************************
Name                 : Plot Viewer Widget
Description          : Widget for viewing imported scheme plots.
Date                 : 24/December/2019
copyright            : (C) 2019
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import exc
from stdm.ui.flts.workflow_manager.data import Load
from stdm.ui.flts.workflow_manager.config import StyleSheet
from stdm.ui.flts.workflow_manager.model import WorkflowManagerModel
from stdm.ui.flts.workflow_manager.plot import PlotLayer


class PlotViewerTableView(QTableView):
    """
    Plot viewer base table view
    """

    def __init__(self, data_service, load_collections, parent=None):
        super(QTableView, self).__init__(parent)
        self._data_service = data_service
        self._load_collections = load_collections
        self._data_loader = Load(self._data_service)
        self.model = WorkflowManagerModel(self._data_service)
        self.setModel(self.model)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.horizontalHeader().setStyleSheet(StyleSheet().header_style)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def _initial_load(self):
        """
        Initial table view data load
        """
        try:
            if self._load_collections:
                self.model.load_collection(self._data_loader)
            else:
                self.model.load(self._data_loader)
        except (AttributeError, exc.SQLAlchemyError, Exception) as e:
            QMessageBox.critical(
                self,
                self.tr('{} Entity Model'.format(self.model.entity_name)),
                self.tr("{0} failed to load: {1}".format(
                    self.model.entity_name, e
                ))
            )
        else:
            self.horizontalHeader().setStretchLastSection(True)
            self.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)


class PlotTableView(PlotViewerTableView):
    """
    Beacon table view
    """
    def __init__(self, data_service, load_collections, scheme_id, parent=None):

        PlotViewerTableView.__init__(self, data_service, load_collections, parent)
        PlotViewerTableView._initial_load(self)


class ServitudeTableView(PlotViewerTableView):
    """
    Beacon table view
    """
    def __init__(self, data_service, load_collections, scheme_id, parent=None):
        PlotViewerTableView.__init__(self, data_service, load_collections, parent)
        PlotViewerTableView._initial_load(self)


class BeaconTableView(PlotViewerTableView):
    """
    Beacon table view
    """
    def __init__(self, data_service, load_collections, scheme_id, parent=None):
        PlotViewerTableView.__init__(self, data_service, load_collections, parent)
        PlotViewerTableView._initial_load(self)


class PlotViewerWidget(QWidget):
    """
    Widget to view plots of a scheme.
    """
    def __init__(self, widget_properties, profile, scheme_id, scheme_number, parent=None):
        super(QWidget, self).__init__(parent)
        self._tab_label = ["Plots", "Servitudes", "Beacons"]
        self._data_service = widget_properties["data_service"]
        self._load_collections = widget_properties["load_collections"]
        self._profile = profile
        self._scheme_id = scheme_id
        self._table_views = OrderedDict()
        self._init_table_views()
        self._default_table = self._default_table_view()
        self.model = self._default_table.model
        parent.paginationFrame.hide()
        self._tab_widget = QTabWidget()
        self._add_tab_widgets(self._table_views)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 11, 0, 0)
        layout.addWidget(self._tab_widget)
        self.setLayout(layout)

    def _init_table_views(self):
        """
        Initialize table view widgets
        """
        for label in self._tab_label:
            data_service = self._data_service(label)
            data_service = data_service(self._profile, self._scheme_id)
            if not data_service.is_entity_empty():
                view = plot_table_view(label)
                self._table_views[label] = \
                    view(data_service, self._load_collections, self._scheme_id, self)

    def _default_table_view(self):
        """
        Returns default table view
        :return table_view: Default table view
        :rtype table_view: QTableView
        """
        if self._table_views:
            table_view = self._table_views.itervalues().next()
            return table_view
        label = self._tab_label[0]
        data_service = self._data_service(label)
        data_service = data_service(self._profile, self._scheme_id)
        table_view = plot_table_view(label)
        table_view = \
            table_view(data_service, self._load_collections, self._scheme_id, self)
        return table_view

    def _add_tab_widgets(self, widgets):
        """
        Adds a widget to a tab
        :param widgets: Widgets to be added
        :type widgets: Dictionary
        """
        if not widgets:
            widgets = {self._tab_label[0]: self._default_table}
        for label, widget in widgets.items():
            self._tab_widget.addTab(widget, label)


def plot_table_view(tab_label):
    """
    Returns plot QTableView class based on tab label
    :param tab_label: QTabWidget label
    :type tab_label: String
    :return: Plot QTableView class
    :rtype: QTableView
    """
    table_view = {
        "Plots": PlotTableView,
        "Servitudes": ServitudeTableView,
        "Beacons": BeaconTableView
    }
    return table_view[tab_label]
