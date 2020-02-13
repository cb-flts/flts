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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import exc
from stdm.ui.flts.workflow_manager.data import Load
from stdm.ui.flts.workflow_manager.config import StyleSheet
from stdm.ui.flts.workflow_manager.model import WorkflowManagerModel
from stdm.ui.flts.workflow_manager.plot import PlotLayer


class BeaconWidget(QTableView):
    """
    A widget to view beacons of a scheme.
    """
    def __init__(self, widget_properties, profile, scheme_id, scheme_number, parent=None):
        super(QTableView, self).__init__(parent)
        self._load_collections = widget_properties["load_collections"]
        self._data_service = widget_properties["data_service"]
        self._data_service = self._data_service("Beacons")
        self._data_service = self._data_service(profile, scheme_id)
        self._data_loader = Load(self._data_service)
        self.model = WorkflowManagerModel(self._data_service)
        self.setModel(self.model)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.horizontalHeader().setStyleSheet(StyleSheet().header_style)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self._initial_load()

    def _initial_load(self):
        """
        Initial table view data load
        """
        try:
            if self._load_collections:
                self.model.load_collection(self._data_loader)
            else:
                self.model.load(self._data_loader)
                pass
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


class PlotWidget(QTableView):
    """
    A widget to view plots of a scheme.
    """
    def __init__(self, widget_properties, profile, scheme_id, scheme_number, parent=None):
        super(QTableView, self).__init__(parent)
        self._load_collections = widget_properties["load_collections"]
        self._data_service = widget_properties["data_service"]
        self._data_service = self._data_service("Plots")
        self._data_service = self._data_service(profile, scheme_id)
        self._data_loader = Load(self._data_service)
        self.model = WorkflowManagerModel(self._data_service)
        self.setModel(self.model)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.horizontalHeader().setStyleSheet(StyleSheet().header_style)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self._initial_load()

    def _initial_load(self):
        """
        Initial table view data load
        """
        try:
            if self._load_collections:
                self.model.load_collection(self._data_loader)
            else:
                self.model.load(self._data_loader)
                pass
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


class PlotViewerWidget(QWidget):
    """
    Widget to view plots of a scheme.
    """
    def __init__(self, widget_properties, profile, scheme_id, scheme_number, parent=None):
        super(QWidget, self).__init__(parent)
        plot_tab = PlotWidget(widget_properties, profile, scheme_id, scheme_number, self)
        beacon_tab = BeaconWidget(widget_properties, profile, scheme_id, scheme_number, self)
        self.model = plot_tab.model
        parent.paginationFrame.hide()
        tab_widget = QTabWidget()
        tab_widget.addTab(plot_tab, "Plots")
        tab_widget.addTab(beacon_tab, "Beacons")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 11, 0, 0)
        layout.addWidget(tab_widget)
        self.setLayout(layout)
