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
import re
from collections import OrderedDict
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import iface
from sqlalchemy import exc
from stdm.data.database import STDMDb
from stdm.ui.flts.workflow_manager.data import Load
from stdm.ui.flts.workflow_manager.config import StyleSheet
from stdm.ui.flts.workflow_manager.model import WorkflowManagerModel
from stdm.ui.flts.workflow_manager.plot import PlotLayer


class PlotViewerTableView(QTableView):
    """
    Plot viewer base table view
    """

    def __init__(self, data_service, load_collections, scheme_number, label, parent=None):
        super(QTableView, self).__init__(parent)
        self._data_service = data_service
        self._data_loader = Load(self._data_service)
        self.model = WorkflowManagerModel(self._data_service)
        self._load_collections = load_collections
        self._scheme_number = scheme_number
        self._label = label
        self._plot_layer = None
        self._reg_exes = re.compile(r'^\s*([\w\s]+)\s*\(\s*(.*)\s*\)\s*$')
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

    def add_layer(self):
        """
        Adds map layer to the canvas
        """
        for row, data in enumerate(self.model.results):
            attributes = self._layer_attributes(data)
            query_obj = data.get("data")
            self._create_layer(query_obj.geom, attributes)
        if self._plot_layer:
            self._plot_layer.update_extents()
            self._plot_layer.add_map_layer()

    def _layer_attributes(self, data):
        """
        Returns layer attributes (field name, type, value)
        :param data: Model data
        :type data: Dictionary
        :return attributes: Layer attributes
        :rtype attributes: List
        """
        attributes = []
        for n, prop in enumerate(self._data_service.columns):
            column = prop.keys()[0]
            header = self._condense_header(column.name)
            value = data.get(n)
            field_type = QVariant.String
            if column.type == "float":
                value = float(QVariant.Double)
                field_type = QVariant.String
            attributes.append([header, field_type, value])
        return attributes

    @staticmethod
    def _condense_header(name):
        """
        Returns condensed layer attribute header name
        :param name: Layer attribute header name
        :type name: String
        :return name: Condensed layer attribute header name
        :rtype name: String
        """
        if name.find("(") > 0:
            name = name.split("(")[0]
        else:
            name = name.strip().replace(" ", "_")
        return name

    def _create_layer(self, wkb_element, attributes):
        """
        Creates a  vector layer
        :param wkb_element: Geoalchemy WKB data type class wrap
        :type wkb_element: WKBElement
        :param attributes: Layer attributes
        :type attributes: List
        """
        db_session = STDMDb.instance().session
        wkt = db_session.scalar(wkb_element.ST_AsText())
        if not self._plot_layer:
            crs_id = "EPSG:{0}".format(wkb_element.srid)
            geom_type = self._wkt_type(wkt)
            uri = "{0}?crs={1}&index=yes".format(geom_type, crs_id)
            fields = [(field, type_) for field, type_, value in attributes]
            name = self._generate_layer_name()
            self._plot_layer = PlotLayer(uri, name, fields=fields)
            self._plot_layer.create_layer()
            self.layer.setReadOnly()
        value = {field: value for field, type_, value in attributes}
        self._plot_layer.wkt_geometry(wkt, value)

    def _wkt_type(self, wkt):
        """
        Returns WKT geometry type
        :param wkt: WKT data
        :type wkt: String
        :return geom_type: Geometry type
        :rtype geom_type: String
        """
        geom_type = None
        matches = self._reg_exes.match(wkt)
        if matches:
            geom_type, coordinates = matches.groups()
            if geom_type:
                geom_type = geom_type.strip()
                geom_type = geom_type.lower().capitalize()
        return geom_type

    def _generate_layer_name(self):
        """
        Generates layer name
        :return layer_name: Layer name
        :rtype layer_name: String
        """
        layer_name = "{0}_{1}".format(self._scheme_number, self._label)
        return layer_name

    @property
    def layer(self):
        """
        Returns created layer
        :return _layer: Layer
        :rtype _layer: QgsVectorLayer
        """
        if self._plot_layer:
            return self._plot_layer.layer


class PlotTableView(PlotViewerTableView):
    """
    Beacon table view
    """
    def __init__(self, data_service, load_collections, scheme_id, scheme_number, label, parent=None):
        PlotViewerTableView.__init__(self, data_service, load_collections, scheme_number, label, parent)
        PlotViewerTableView._initial_load(self)


class ServitudeTableView(PlotViewerTableView):
    """
    Beacon table view
    """
    def __init__(self, data_service, load_collections, scheme_id, scheme_number, label, parent=None):
        PlotViewerTableView.__init__(self, data_service, load_collections, scheme_number, label, parent)
        PlotViewerTableView._initial_load(self)


class BeaconTableView(PlotViewerTableView):
    """
    Beacon table view
    """
    def __init__(self, data_service, load_collections, scheme_id, scheme_number, label, parent=None):
        PlotViewerTableView.__init__(self, data_service, load_collections, scheme_number, label, parent)
        PlotViewerTableView._initial_load(self)


class PlotViewerWidget(QWidget):
    """
    Widget to view plots of a scheme.
    """
    layers = {}

    def __init__(self, widget_properties, profile, scheme_id, scheme_number, parent=None):
        super(QWidget, self).__init__(parent)
        self._tab_label = ["Plots", "Servitudes", "Beacons"]
        self._data_service = widget_properties["data_service"]
        self._load_collections = widget_properties["load_collections"]
        self._profile = profile
        self._scheme_id = scheme_id
        self._scheme_number = scheme_number
        self._parent = parent
        self._table_views = OrderedDict()
        self._init_table_views()
        self._default_table = self._default_table_view()
        self.model = self._default_table.model
        self._parent.paginationFrame.hide()
        self._tab_widget = QTabWidget()
        self._add_tab_widgets(self._table_views)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 11, 0, 0)
        layout.addWidget(self._tab_widget)
        self.setLayout(layout)
        self._dock_widget.closing.connect(PlotViewerWidget._on_dock_close)
        self._parent.removeTab.connect(self._on_remove_tab)
        self._add_layers()

    def _init_table_views(self):
        """
        Initialize table view widgets
        """
        for label in self._tab_label:
            data_service = self._data_service(label)
            data_service = data_service(self._profile, self._scheme_id)
            if not data_service.is_entity_empty():
                view = plot_table_view(label)
                # noinspection PyCallingNonCallable
                self._table_views[label] = view(
                    data_service,
                    self._load_collections,
                    self._scheme_id,
                    self._scheme_number,
                    label,
                    self
                )

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
        # noinspection PyCallingNonCallable
        table_view = table_view(
            data_service,
            self._load_collections,
            self._scheme_id,
            self._scheme_number,
            label,
            self
        )
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

    def _add_layers(self):
        """
        Adds map layers to the canvas
        """
        self._remove_layers()
        if not self._table_views:
            return
        for label, table_view in self._table_views.items():
            table_view.add_layer()
            PlotViewerWidget.layers[label] = table_view.layer

    @property
    def _dock_widget(self):
        """
        Returns parent dock widget
        :return: Parent dock widget
        :rtype: QDockWidget
        """
        return iface.mainWindow().findChild(
            QDockWidget,
            self._parent.objectName()
        )

    @classmethod
    def _on_dock_close(cls, event):
        """
        Handles on parent QDockWidget close event
        """
        cls._remove_layers()
        event.accept()

    @classmethod
    def _on_remove_tab(cls):
        """
        Handles on tab remove event
        """
        cls._remove_layers()

    @classmethod
    def _remove_layers(cls):
        """
        Removes all layers from the registry/map canvas
        given layer IDs
        """
        if not cls.layers:
            return
        try:
            layer_ids = cls.layer_ids()
            if layer_ids:
                PlotLayer.remove_layers(layer_ids)
                cls.layers = {}
        except (RuntimeError, OSError, Exception) as e:
            raise e

    @classmethod
    def layer_ids(cls):
        """
        Returns all layers from the registry/map canvas
        :return layer_ids: Layer IDs
        :rtype layer_ids: List
        """
        layer_ids = [layer.id() for layer in cls.layers.values()]
        return layer_ids


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
