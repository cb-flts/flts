"""
/***************************************************************************
Name                 : Plot
Description          : Module for managing importing of a scheme plot
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
import decimal
import itertools
from collections import OrderedDict
import csv
from PyQt4.QtCore import (
    Qt,
    QFile,
    QFileInfo,
    QIODevice,
    QVariant
)
from qgis.core import (
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsMapLayerRegistry,
    QgsProject,
    QgsVectorDataProvider,
    QgsVectorLayer,
    QgsWKBTypes
)
from qgis.utils import iface
from sqlalchemy import exc
from stdm.ui.flts.workflow_manager.data import Save

NAME, IMPORT_AS, DELIMITER, HEADER_ROW, CRS_ID, \
GEOM_FIELD, GEOM_TYPE = range(7)
GEOMETRY, PARCEL_NUM, UPI_NUM, AREA = range(4)
GEOMETRY_PT, X_PT, Y_PT = range(3)
WARNING = "Warning"


class PlotLayer:
    """
    Manages preview of plot geometric shape in a layer.
    """
    qgs_project = None

    def __init__(self, uri, name, provider_lib="memory", fields=None):
        self._uri = uri
        self._name = name
        self._provider_lib = provider_lib
        self._fields = fields
        self._attribute_names = []
        self._data_provider = None
        self._layer = None
        self._features = []
        self.project_instance().legendLayersAdded.connect(self._move_layer_top)

    @property
    def layer(self):
        """
        Returns created layer
        :return _layer: Layer
        :rtype _layer: QgsVectorLayer
        """
        return self._layer

    @layer.setter
    def layer(self, value):
        """
        Returns created layer
        :param value: Value to be set
        :type value: Object
        """
        self._layer = value

    @property
    def features(self):
        """
        Returns list of added features
        :return _feature: Added features
        :rtype _feature: List
        """
        return self._features

    @property
    def attribute_names(self):
        """
        Returns attribute names
        :return _attribute_names: Attribute names
        :rtype _attribute_names: List
        """
        return self._attribute_names

    def create_layer(self):
        """
        Creates a vector layer
        """
        self._layer = QgsVectorLayer(self._uri, self._name, self._provider_lib)
        self._set_data_provider()
        self.add_attributes(self._attribute_fields)
        self._layer.updateFields()

    def _set_data_provider(self):
        """
        Sets the data provider
        """
        self._data_provider = self._layer.dataProvider()

    def add_attributes(self, attributes):
        """
        Adds attributes to the layer
        :param attributes: Layer attributes
        :type attributes: List
        """
        if attributes:
            self._data_provider.addAttributes(attributes)
            self._set_attribute_name(attributes)

    def _set_attribute_name(self, attributes):
        """
        Sets attribute names
        :param attributes: Layer attributes
        :type attributes: List
        """
        for attribute in attributes:
            name = attribute.name()
            if name not in self._attribute_names:
                self._attribute_names.append(name)

    @property
    def _attribute_fields(self):
        """
        Returns QGIS attribute fields
        :return fields: QGIS attribute fields
        :rtype fields: QgsField
        """
        if not self._fields:
            return
        fields = [QgsField(name, type_) for name, type_ in self._fields]
        return fields

    def wkt_geometry(self, wkt, attributes):
        """
        Creates geometry from WKT and
        displays it in the map canvas
        :param wkt: Well-Known Text(WKT)
        :type wkt: String
        :param attributes: Attribute values
        :type attributes: Dictionary
        """
        geom = QgsGeometry.fromWkt(wkt)
        if not geom:
            return
        feature = QgsFeature()
        feature.setGeometry(geom)
        values = self._attribute_values(attributes)
        if values:
            feature.setAttributes(values)
        result, feature = self._data_provider.addFeatures([feature])
        self._features.extend(feature)

    def _attribute_values(self, attributes):
        """
        Returns attribute values given the attribute names
        :param attributes: Attribute values
        :type attributes: Dictionary
        :return values: Attribute values
        :return values: Object
        """
        if not self._fields:
            fields = self.get_fields(self._layer)
            self._fields = self._field_types(fields)
        if self._fields:
            values = [attributes.get(name) for name, type_ in self._fields]
            return values

    def get_fields(self, layer=None):
        """
        Returns the fields associated with this layer
        :param layer: Geometry layer
        :type layer: QgsVectorLayer
        :return layer: QgsFields
        :rtype layer: QgsFields
        """
        if not layer:
            layer = self._layer
        return layer.dataProvider().fields()

    @staticmethod
    def _field_types(fields):
        """
        Returns a list of layer fields and types
        :param fields: Layer fields
        :type fields: QgsFields
        :return fields: Layer fields name and type
        :rtype fields: List
        """
        if len(fields) > 0:
            fields = [(field.name(), field.type()) for field in fields]
            return fields

    @staticmethod
    def feature_area(feature):
        """
        Returns feature geometry area
        :param feature: Feature
        :type feature: QgsFeature
        :return: Feature area
        :rtype: Float
        """
        geom = feature.geometry()
        if geom.wkbType() == QgsWKBTypes.Polygon:
            return geom.area()

    @staticmethod
    def _move_layer_top(layers):
        """
        On new layer, move it to the top of the Layer Order Panel
        :param layers: List of layers
        :type layers: List
        """
        order = iface.layerTreeCanvasBridge().customLayerOrder()
        for _ in layers:
            order.insert(0, order.pop())
        iface.layerTreeCanvasBridge().setCustomLayerOrder(order)

    def add_map_layer(self):
        """
        Adds layer to the project
        """
        self.project_instance().addMapLayer(self._layer)

    def update_extents(self, layer=None):
        """
        Updates layer extent
        :param layer: QgsVectorLayer
        :type layer: QgsVectorLayer
        """
        if not layer:
            layer = self._layer
        layer.updateExtents()

    def remove_layer_by_name(self, name):
        """
        Removes a layer from the project given the name
        :param name: Layer name
        :type name: String
        """
        project = self.project_instance()
        layer = project.mapLayersByName(name)
        if len(layer) > 0:
            project.removeMapLayer(layer[0].id())

    @classmethod
    def remove_layer_by_id(cls, id_):
        """
        Removes a layer from the project given the id
        :param id_: Layer ID
        :type id_: String
        """
        cls.qgs_project.removeMapLayer(id_)

    def select_feature(self, layer, feature_ids):
        """
        Selects a feature given the identifier
        :param layer: Input layer
        :type layer: QgsVectorLayer
        :param feature_ids: Feature identifier
        :type feature_ids: Object
        """
        self._move_node_to_first(layer)
        if not self._is_active(layer):
            iface.setActiveLayer(layer)
        layer.select(feature_ids)

    def _move_node_to_first(self, layer):
        """
        Moves child node to first node position
        :param layer: Input layer
        :type layer: QgsVectorLayer
        """
        index = 0
        first_node = self._layer_child_node(index)
        if first_node.layerId() != layer.id():
            self._move_node(layer, index)

    @staticmethod
    def _layer_child_node(index):
        """
        Returns layer child node
        :param index: Child node index
        :param index: Integer
        :return child_node: Layer child node
        :rtype child_node: QgsLayerTreeLayer
        """
        project = QgsProject.instance()
        root = project.layerTreeRoot()
        child_node = root.children()[index]
        return child_node

    @staticmethod
    def _move_node(layer, index):
        """
        Moves child node
        :param layer: Input layer
        :type layer: QgsVectorLayer
        :param index: Index to move the node to
        :type index: Integer
        """
        project = QgsProject.instance()
        root = project.layerTreeRoot()
        layer_node = root.findLayer(layer.id())
        clone = layer_node.clone()
        parent = layer_node.parent()
        parent.insertChildNode(index, clone)
        parent.removeChildNode(layer_node)

    @staticmethod
    def _is_active(layer):
        """
        Checks if layer is active
        :param layer: Input layer
        :type layer: QgsVectorLayer
        :return: True if active
        :return: Boolean
        """
        if layer == iface.activeLayer():
            return True

    @classmethod
    def clear_feature(cls, layer):
        """
        Clears selected features in a layer
        :param layer: Input layer
        :type layer: QgsVectorLayer
        """
        if layer and layer.isValid():
            layer.removeSelection()

    @classmethod
    def remove_layers(cls, ids):
        """
        Removes list of layers from the project given the IDs
        :param ids: Layer IDs
        :type ids: List
        """
        cls.qgs_project.removeMapLayers(ids)

    @classmethod
    def project_instance(cls):
        """
        Returns the instance pointer
        """
        try:
            cls.qgs_project = QgsMapLayerRegistry.instance()
        except:
            cls.qgs_project = QgsProject.instance()
        else:
            return cls.qgs_project


class Item:
    """
    Items associated properties
    """
    def __init__(self, flags=None, tootltip=None, icon_id=None):
        self.flags = flags if flags else []
        self.tooltip = tootltip
        self.icon_id = icon_id


class Plot(object):
    """
    Plot associated methods
    """
    def __init__(self):
        self._reg_exes = {
            "type_str": re.compile(r'^\s*([\w\s]+)\s*\(\s*(.*)\s*\)\s*$'),
        }

    def geometry_type(self, fpath, hrow=0, delimiter=None):
        """
        Returns dominant geometry type of
        loaded plot import file - CSV/txt
        :param fpath: Plot import file absolute path
        :type fpath: String
        :param hrow: Header row number
        :type hrow: Integer
        :param delimiter: Delimiter
        :type delimiter: String
        :return: Geometry type
        :rtype: String
        """
        if self.is_pdf(fpath):
            return
        try:
            with open(fpath, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=delimiter)
                sample = itertools.islice(csv_reader, 5000)
                match_count = {}
                for row, data in enumerate(sample):
                    if row == hrow:
                        continue
                    for value in data:
                        if value is None or isinstance(value, list):
                            continue
                        geom_type, coordinates, geom = self._geometry(value)
                        if geom_type:
                            if geom_type not in match_count:
                                match_count[geom_type] = 0
                                continue
                            match_count[geom_type] += 1
                return self._default_geometry_type(match_count)
        except (csv.Error, Exception) as e:
            raise e

    @staticmethod
    def is_pdf(fpath):
        """
        Checks if the file extension is PDF
        :param fpath: Plot import file absolute path
        :type fpath: String
        :return True: Returns true if the file extension is PDF
        :rtype True: Boolean
        """

        file_extension = QFileInfo(fpath).suffix()
        if file_extension == "pdf":
            return True

    def _geometry(self, wkt):
        """
        Returns geometry and geometry type given WKT data
        :param wkt: WKT data
        :type wkt: String
        :return geom_type: Geometry type
        :rtype geom_type: String
        :return geom: Geometry
        :rtype geom: QgsGeometry
        """
        geom_type = geom = coordinates = None
        matches = self._reg_exes["type_str"].match(wkt)
        if matches:
            geom_type, coordinates = matches.groups()
            geom = QgsGeometry.fromWkt(wkt.strip())
            if geom_type:
                geom_type = geom_type.strip()
                geom_type = geom_type.lower().capitalize()
        return geom_type, coordinates, geom

    @staticmethod
    def _default_geometry_type(type_count):
        """
        Returns default plot import file geometry type
        :param type_count: Geometry type count
        :type type_count: Dictionary
        :return geom_type: Default geometry type
        :rtype geom_type: String
        """
        geom_type = None
        if type_count:
            geom_type = max(
                type_count.iterkeys(),
                key=lambda k: type_count[k]
            )
        return geom_type

    @property
    def _geometry_types(self):
        """
        Returns a map of expected geometry types
        :return: Geometry types
        :rtype: OrderedDict
        """
        return OrderedDict({
            "Point": "Point", "Linestring": "Line", "Polygon": "Polygon"
        })

    @staticmethod
    def _decoration_tooltip(tip):
        """
        Returns decoration role tooltip item
        :param tip: Tooltip message
        :type tip: String
        :return: Decoration tooltip item
        :return: Item
        """
        return Item([Qt.DecorationRole, Qt.ToolTipRole], unicode(tip))


class UniqueParcelIdentifier:
    """
    Unique Parcel Identifier (UPI) object
    """

    rems = ["REM", "ACCES", "POS"]

    def __init__(self, data_service, prefix):
        self._data_service = data_service
        self._prefix = prefix
        self._plot_counter = 0
        self._wkt_plot_numbers = []

    def scheme_plot_numbers(self):
        """
        Returns the Scheme plot numbers
        :return plot_numbers: Scheme plot numbers
        :rtype plot_numbers: List
        """
        plot_numbers = self._data_service.scheme_plot_numbers()
        plot_numbers = [num for num, in plot_numbers]
        return plot_numbers

    def aucode(self):
        """
        Returns the Scheme AUCODE
        :return: Scheme AUCODE
        :rtype: Unicode
        """
        relevant_authority = self._data_service.scheme_relevant_authority()
        return relevant_authority.au_code

    def plot_number(self, plot_id):
        """
        Returns Scheme Plot Number
        :param plot_id: Plot identifier
        :type: Object
        :return: Plot number
        :rtype: String
        """
        plot_id = str(plot_id)
        if self._is_id_remainder(plot_id):
            return plot_id
        plot_number = self._extract_plot_number(plot_id)
        if plot_number:
            plot_number = self._generate_plot_number(plot_number)
        return plot_number

    @staticmethod
    def _generate_plot_number(num):
        """
        Returns a new plot number
        :param num: New number
        :type num: Integer
        :return: Plot number
        :rtype: String
        """
        prefix = "000000"
        suffix = str(num)
        prefix = prefix[:-len(suffix)]
        return prefix + suffix

    def _is_id_remainder(self, plot_id):
        """
        Checks if the WKT plot ID is the remainder
        :param plot_id: Plot ID
        :param plot_id: String
        :return: True or False
        :return: Boolean
        """
        for rem in self.rems:
            if plot_id.find(rem) != -1:
                return True
        return False

    @staticmethod
    def _extract_plot_number(plot_id):
        """
        Extracts plot number from the WKT plot ID
        :param plot_id: Plot ID
        :param plot_id: String
        :return plot_id: Plot number
        :param plot_id: Integer
        """
        try:
            plot_id = [c for c in plot_id if c.isdigit()]
            plot_id = int("".join(plot_id))
            return plot_id
        except ValueError:
            return

    def wkt_plot_numbers(self):
        """
        Returns plot numbers generated from the WKT file
        :return _wkt_plot_numbers: Plot numbers
        :rtype _wkt_plot_numbers: List
        """
        return self._wkt_plot_numbers

    def store_wkt_plot_number(self, plot_number):
        """
        Stores plot numbers generated from the WKT file
        :param plot_number: Plot number
        :type plot_number: String
        """
        self._wkt_plot_numbers.append(plot_number)

    @staticmethod
    def _is_number(value):
        """
        Checks if value is a number
        :param value: Input value
        :type value: Object
        :return: True if number otherwise return False
        :rtype: Boolean
        """
        try:
            float(value)
            return True
        except (ValueError, TypeError, Exception):
            return False

    def upi(self, plot_number, aucode):
        """
        Returns Unique Parcel Identifier (UPI)
        :param plot_number: Plot number
        :type plot_number: String
        :param aucode: AUCODE
        :type aucode: Unicode
        :return upi: Unique Parcel Identifier
        :return upi: String
        """
        upi = "{0}/{1}/{2}".format(self._prefix, plot_number, aucode)
        return upi


class PlotFileSettings:
    """
    Manages plot file settings
    """

    def __init__(self, file_settings):
        self.header_row = file_settings.get(HEADER_ROW) - 1
        self.delimiter = self._get_delimiter(file_settings.get(DELIMITER))
        self.geom_field = file_settings.get(GEOM_FIELD)
        self.geom_type = file_settings.get(GEOM_TYPE)
        self.crs_id = file_settings.get(CRS_ID)
        self.import_as = file_settings.get(IMPORT_AS)
        self.fpath = file_settings.get("fpath")
        self.file_fields = file_settings.get("fields")

    @staticmethod
    def _get_delimiter(name):
        """
        Returns a delimiter
        :param name: Delimiter name
        :param name: Unicode
        :return: Delimiter
        :rtype: String
        """
        delimiter = str(name.split(" ")[0]).strip()
        if delimiter == "t":
            delimiter = "\t"
        return delimiter


class PlotPreview(Plot):
    """
    Manages preview of plot import data file contents
    """
    type_count = {"Point": 1, "Line": 1, "Polygon": 1}

    def __init__(self, scheme_number, data_service=None):
        super(PlotPreview, self).__init__()
        self._data_service = data_service
        self._scheme_number = scheme_number
        self._items = self._plot_layer = None
        self._error_counter = 0
        self._import_type = {"Point": "Beacons", "Line": "Servitudes", "Polygon": "Plots"}
        self._settings = None
        self._layers = {}
        self._dirty = {}
        self._errors = {}
        self.wkt_header_options = {
            "parcel_number": (
                "id", "parcel_number",
                "parcel number", "parcel"
            )
        }

    def set_settings(self, settings):
        """
        Sets plot file settings
        :param settings: Plot file settings
        :type settings: Dictionary
        """
        if not settings:
            return
        self._settings = PlotFileSettings(settings)

    def load(self):
        """
        Loads plot import file contents
        :return: Plot import file data settings
        :rtype: List
        """
        try:
            qfile = QFile(self._settings.fpath)
            if not qfile.open(QIODevice.ReadOnly):
                raise IOError(unicode(qfile.errorString()))
            return self._file_contents(self._settings.fpath)
        except(IOError, OSError, csv.Error, NotImplementedError, Exception) as e:
            raise e

    def _file_contents(self, fpath):
        """
        Returns plot import file contents
        :param fpath: Plot import file absolute path
        :type fpath: String
        :return results: Plot import file contents
        :rtype results: List
        """
        self._plot_layer = None
        self._error_counter = 0
        try:
            with open(fpath, 'r') as csv_file:
                clean_line = self._filter_whitespace(csv_file, self._settings.header_row)
                csv_reader = csv.DictReader(
                    clean_line,
                    fieldnames=self._settings.file_fields,
                    delimiter=self._settings.delimiter
                )
                self._settings.geom_type = self._geometry_type()
                if self._settings.import_as == "Plots":
                    results = self._plot_file_contents(csv_reader)
                elif self._settings.import_as == "Servitudes":
                    results = self._servitude_file_contents(csv_reader)
                else:
                    results = self._beacon_file_contents(csv_reader)
                if self._plot_layer:
                    self._plot_layer.update_extents()
                    self._plot_layer.add_map_layer()
                    self._signal_layers_removed()
        except (csv.Error, Exception) as e:
            raise e
        if results:
            self._dirty[self._settings.fpath] = True
            self._set_errors(fpath)
        return results

    def _set_errors(self, fpath):
        """
        Sets counted errors in a previewed file
        :param fpath: Plot import file absolute path
        :type fpath: String
        """
        if self._error_counter == 0 and fpath in self._errors:
            del self._errors[fpath]
            return
        self._errors[fpath] = self._error_counter

    def remove_error(self, fpath):
        """
        Removes error
        :param fpath: Plot import file absolute path
        :type fpath: String
        """
        if fpath in self._errors:
            del self._errors[fpath]

    def _plot_file_contents(self, csv_reader):
        """
        Returns plot file contents
        :param csv_reader: CSV dictionary reader
        :param csv_reader: DictReader
        :return results: File content list
        :return results: List
        """
        results = []
        upi = UniqueParcelIdentifier(self._data_service, "W")
        scheme_plot_numbers = upi.scheme_plot_numbers()
        aucode = upi.aucode()
        area_attribute = False
        for row, data in enumerate(csv_reader):
            contents = {}
            self._items = {}
            value = self._get_wkt(data, GEOMETRY)
            if value:
                contents[GEOMETRY] = unicode(value)
                field_options = self.wkt_header_options["parcel_number"]
                value = self._get_value(data, field_options, PARCEL_NUM)
                plot_number = self._plot_number(value, upi, scheme_plot_numbers)
                contents[PARCEL_NUM] = unicode(plot_number)
                if plot_number != WARNING:
                    plot_number = unicode(upi.upi(aucode, plot_number))
                contents[UPI_NUM] = self._on_empty_value(UPI_NUM, plot_number)
                contents[AREA] = ""
                attributes = self._layer_attributes(contents)
                self._create_layer(contents[GEOMETRY], attributes)
                if not area_attribute:
                    self._add_attributes([QgsField("Area", QVariant.Double)])
                    area_attribute = True
                value = self._plot_area()
                self._update_plot_attribute("Area", value)
                contents[AREA] = unicode(self._to_float(value, AREA))
                contents["items"] = self._items
                results.append(contents)
        return results

    def _plot_number(self, value, upi, scheme_plot_numbers):
        """
        Returns plot number
        :param value: WKT value
        :param value: Object
        :param upi: Unique Parcel Identifier
        :param upi: UniqueParcelIdentifier
        :param scheme_plot_numbers: Existing scheme plot numbers
        :param scheme_plot_numbers: String
        :return value: Plot number
        :return value: String
        """
        if value == WARNING:
            return value
        plot_number = upi.plot_number(value)
        wkt_plot_numbers = upi.wkt_plot_numbers()
        if plot_number is None:
            self._set_invalid_tip(PARCEL_NUM, "Invalid identifier")
        elif plot_number in wkt_plot_numbers:
            self._set_invalid_tip(PARCEL_NUM, "Duplicate WKT identifier")
        elif plot_number in scheme_plot_numbers:
            value = plot_number
            tip = "Scheme plot number exist in the database"
            self._set_invalid_tips({PARCEL_NUM: tip, UPI_NUM: tip})
        else:
            value = plot_number
            upi.store_wkt_plot_number(plot_number)
        return value

    def _plot_area(self):
        """
        Returns area value
        :return area: Area value
        :rtype area: Object
        """
        if self._plot_layer and self._plot_layer.features:
            feature = self._plot_layer.features[-1]
            area = self._feature_area(feature)
            area = self._on_empty_value(AREA, area)
            return area
        else:
            return self._on_empty_value(AREA)

    def _update_plot_attribute(self, field_name, value):
        """
        Updates plot attribute
        :param field_name: Field name
        :type field_name: String
        :param value: Update value
        :type value: Object
        """
        if self._plot_layer and self._plot_layer.features:
            layer = self._plot_layer.layer
            feature = self._plot_layer.features[-1]
            value = self._replace_warning(value)
            attribute = {layer.fieldNameIndex(field_name): value}
            self._update_feature_attribute(layer, feature, attribute)

    def _servitude_file_contents(self, csv_reader):
        """
        Returns servitude file contents
        :param csv_reader: CSV dictionary reader
        :param csv_reader: DictReader
        :return results: File content list
        :return results: List
        """
        results = []
        for row, data in enumerate(csv_reader):
            contents = {}
            self._items = {}
            value = self._get_wkt(data, GEOMETRY)
            if value:
                contents[GEOMETRY] = unicode(value)
                contents["items"] = self._items
                attributes = self._layer_attributes(contents)
                self._create_layer(contents[GEOMETRY], attributes)
                results.append(contents)
        return results

    def _beacon_file_contents(self, csv_reader):
        """
        Returns beacon file contents
        :param csv_reader: CSV dictionary reader
        :param csv_reader: DictReader
        :return results: File content list
        :return results: List
        """
        results = []
        for row, data in enumerate(csv_reader):
            contents = {}
            self._items = {}
            value = self._get_wkt(data, GEOMETRY_PT)
            if value:
                contents[GEOMETRY_PT] = unicode(value)
                lat, long_ = self._beacon_coordinates(value)
                contents[X_PT] = unicode(self._to_float(lat, X_PT))
                contents[Y_PT] = unicode(self._to_float(long_, Y_PT))
                contents["items"] = self._items
                attributes = self._layer_attributes(contents)
                self._create_layer(contents[GEOMETRY_PT], attributes)
                results.append(contents)
        return results

    @staticmethod
    def _filter_whitespace(in_file, hrow):
        """
        Returns non-whitespace line of data
        :param in_file: Input file
        :param in_file: TextIOWrapper
        :param hrow: Header row number
        :type hrow: Integer
        :return line: Non-whitespace line
        :return line: generator
        """
        for row, line in enumerate(in_file):
            if row == hrow:
                continue
            if not line.isspace():
                yield line

    def _geometry_type(self):
        """
        Returns dominant geometry type of
        loaded plot import file
        :return: Dominant geometry type
        :rtype: String
        """
        if self._settings.geom_type not in self._geometry_types.values():
            self._settings.geom_type = self.geometry_type(
                self._settings.fpath,
                self._settings.header_row,
                self._settings.delimiter
            )
            type_ = self._geometry_types.get(self._settings.geom_type)
            self._settings.geom_type = type_ if type_ else self._settings.geom_type
        return self._settings.geom_type

    def _get_wkt(self, data, column):
        """
        Returns plot import file wkt value
        :param data: Plot import file contents
        :type data: generator
        :param column: Table view column position
        :type column: Integer
        :return value: Plot import file value
        :return value: Object
        """
        invalid_tip = "Invalid WKT"
        value = data.get(self._settings.geom_field)
        if value is None:
            return
        elif isinstance(value, list):
            self._set_invalid_tip(column, invalid_tip)
            return value
        geom_type, coordinates, geom = self._geometry(value)
        if not geom:
            self._set_invalid_tip(column, invalid_tip)
            return value
        else:
            geom_type = self._geometry_types.get(geom_type)
            if not geom_type:
                self._set_invalid_tip(column, "Geometry type not allowed")
            elif geom_type != self._settings.geom_type:
                tip = "Mismatch with set geometry type ({})".\
                    format(self._settings.geom_type)
                self._set_invalid_tip(column, tip)
            elif self._import_type.get(self._settings.geom_type) != \
                    self._settings.import_as:
                tip = "Mismatch with set import type ({})".\
                    format(self._settings.import_as)
                self._set_invalid_tip(column, tip)
            return value

    def _get_value(self, data, field_names, column):
        """
        Returns plot import file value given field names
        :param data: Plot import file contents
        :type data: generator
        :param field_names: Plot import file field names
        :type field_names: Tuple/List
        :param column: Table view column position
        :type column: Integer
        :return value: Plot import file value
        :return value: Object
        """
        value = self._field_value(data, field_names)
        value = self._on_empty_value(column, value)
        return value

    @staticmethod
    def _field_value(data, field_names):
        """
        Returns plot import file field value given field names
        :param data: Plot import file contents
        :type data: generator
        :param field_names: Plot import file field names
        :type field_names: Tuple/List
        :return value: Plot import file field value
        :rtype value: Object
        """
        fields = {name.lower(): name for name in data.keys()}
        for name in field_names:
            name = name.lower()
            if name in fields:
                return data.get(fields[name])

    def _beacon_coordinates(self, wkt):
        """
        Returns plot beacon coordinates
        :param wkt: WKT data
        :type wkt: String
        :return lat: Beacon coordinates
        :rtype lat: Float
        """
        beacon = {X_PT: "", Y_PT: ""}
        if GEOMETRY_PT not in self._items:
            geom_type, coordinates, geom = self._geometry(wkt)
            lat, long_ = coordinates.split()
            beacon = dict([(X_PT, lat), (Y_PT, long_)])
        beacon = {k: self._coordinate(k, v) for k, v in beacon.items()}
        return beacon[X_PT], beacon[Y_PT]

    def _coordinate(self, column, coordinate):
        """
        Returns coordinate value
        :param column: Table view column position
        :type column: Integer
        :param coordinate: Coordinate value
        :type coordinate: String
        :return coordinate: Coordinate value
        :rtype coordinate: String
        """
        coordinate = self._on_empty_value(column, coordinate)
        return coordinate

    def _on_empty_value(self, column, value=None):
        """
        Set empty value
        :param column: Table view column position
        :type column: Integer
        :param value: Plot import file value
        :type value: Object
        :return value: Empty value flag
        :return value: String
        """
        if value == WARNING or value is None or not str(value).strip():
            value = WARNING
            self._items[column] = self._decoration_tooltip("Missing value")
            self._error_counter += 1
        return value

    def _to_float(self, value, column):
        """
        Casts value to float
        :param value: Value object
        :type value: Object
        :param column: Table view column position
        :type column: Integer
        :return value: Float or other object types
        :return value: Object
        """
        if self._is_number(value):
            value = round(decimal.Decimal(value), 6)
        else:
            if value != WARNING:
                self._set_invalid_tip(column, "Value is not a number")
        return value

    @staticmethod
    def _is_number(value):
        """
        Checks if value is a number
        :param value: Input value
        :type value: Object
        :return: True if number otherwise return False
        :rtype: Boolean
        """
        try:
            float(value)
            return True
        except (ValueError, TypeError, Exception):
            return False

    def _set_invalid_tips(self, tips):
        """
        Sets invalid tips to columns
        :param tips: Table view column tips
        :type tips: Dictionary
        """
        for column, tip in tips.items():
            self._set_invalid_tip(column, tip)

    def _set_invalid_tip(self, column, tip=None):
        """
        Sets invalid tip on a column
        :param column: Table view column position
        :type column: Integer
        :param tip: Tooltip message
        :type tip: String
        """
        invalid_tip = self._display_tooltip("Invalid value", WARNING)
        if tip:
            invalid_tip = self._display_tooltip(tip, WARNING)
        self._items[column] = invalid_tip
        self._error_counter += 1

    @staticmethod
    def _display_tooltip(tip, icon_id):
        """
        Returns display and decoration role tooltip item
        :param tip: Tooltip message
        :type tip: String
        :param icon_id: Icon identifier
        :type icon_id: String
        :return: Decoration tooltip item
        :return: Item
        """
        return Item(
            [Qt.DisplayRole, Qt.DecorationRole, Qt.ToolTipRole],
            unicode(tip),
            icon_id
        )

    def _layer_attributes(self, contents):
        """
        Returns layer attributes (field name, type, value)
        :param contents: Plot import file contents
        :type contents: Dictionary
        :return attributes: Layer attributes
        :rtype attributes: List
        """
        attributes = []
        headers = self.get_headers()
        for column, value in contents.items():
            attr = []
            if column == GEOMETRY or column == 'items':
                continue
            name = headers[column].name
            name = "_".join(name.split())[:10]
            attr.append(name)
            if headers[column].type == "float":
                value = self._attribute_to_float(value)
                attr.extend([QVariant.Double, value])
            else:
                value = self._replace_warning(value)
                attr.extend([QVariant.String, value])
            attributes.append(attr)
        return attributes

    @staticmethod
    def _attribute_to_float(value):
        """
        Returns float layer attribute
        :param value: Object value
        :type value: Object
        :return value: Float value
        :rtype value: Float
        """
        if isinstance(value, str):
            value = float(0)
        return value

    @staticmethod
    def _replace_warning(value):
        """
        Replaces WARNING with None type
        :param value: Object value
        :type value: Object
        :return value: String value
        :rtype value: String
        """
        if value == WARNING:
            value = None
        return value

    def _create_layer(self, wkt, attributes):
        """
        Creates a  vector layer
        :param wkt: WKT data
        :type wkt: String
        :param attributes:
        :return:
        """
        if not self._valid_setup(wkt):
            self._remove_previewed_layers()
            return
        if not self._plot_layer:
            geom_type, coordinates, geom = self._geometry(wkt)
            uri = "{0}?crs={1}&index=yes".format(geom_type, self._settings.crs_id)
            fields = [(field, type_) for field, type_, value in attributes]
            name = self._generate_layer_name()
            self._plot_layer = PlotLayer(uri, name, fields=fields)
            self.remove_layer_by_id(self._settings.fpath)
            self._plot_layer.create_layer()
            self.layer.setReadOnly()
            self._layers[self._settings.fpath] = self.layer
            self.type_count[self._settings.geom_type] += 1
        value = {field: value for field, type_, value in attributes}
        self._plot_layer.wkt_geometry(wkt, value)

    def _valid_setup(self, wkt):
        """
        Checks if the setup items are
        valid for layer creation
        :param wkt: WKT data
        :type wkt: String
        :return: True if valid. Otherwise False
        :rtype: Boolean
        """
        geom_type, coordinates, geom = self._geometry(wkt)
        type_name = self._geometry_types.get(geom_type)
        import_type = self._import_type.get(self._settings.geom_type)
        if not type_name or \
                type_name != self._settings.geom_type or \
                import_type != self._settings.import_as:
            return False
        return True

    def _remove_previewed_layers(self):
        """
        Removes previewed layers
        """
        self.remove_layer_by_id(self._settings.fpath)
        layer = self._layers.get(self._settings.fpath)
        if layer:
            self._remove_stored_layer(layer.id())

    def _generate_layer_name(self):
        """
        Generates layer name
        :return layer_name: Layer name
        :rtype layer_name: String
        """
        layer_name = "{0}_{1}_{2}".format(
            self._scheme_number,
            self._import_type.get(self._settings.geom_type),
            self.type_count[self._settings.geom_type]
        )
        return layer_name

    def remove_layer_by_id(self, parent_id):
        """
        Removes layer from the registry/map canvas
        :param parent_id: Parent record/item identifier
        :type parent_id: String
        """
        if not self._layers:
            return
        try:
            layer = self._layers.get(parent_id)
            if layer:
                PlotLayer.remove_layer_by_id(layer.id())
        except (RuntimeError, OSError, Exception) as e:
            raise e

    def remove_layers(self):
        """
        Removes all layers from the registry/map canvas
        given layer IDs
        """
        if not self._layers:
            return
        try:
            layer_ids = self.layer_ids()
            if layer_ids:
                PlotLayer.remove_layers(layer_ids)
        except (RuntimeError, OSError, Exception) as e:
            raise e

    def layer_ids(self):
        """
        Returns all layers from the registry/map canvas
        :return layer_ids: Layer IDs
        :rtype layer_ids: List
        """
        layer_ids = [layer.id() for layer in self._layers.values()]
        return layer_ids

    @property
    def layer(self):
        """
        Returns created layer
        :return _layer: Layer
        :rtype _layer: QgsVectorLayer
        """
        if self._plot_layer:
            return self._plot_layer.layer

    def _signal_layers_removed(self):
        """
        Emits layersWillBeRemoved signal
        """
        project = self._plot_layer.project_instance()
        project.layersWillBeRemoved.connect(self._remove_stored_layer)
        project.layersWillBeRemoved.connect(self._reset_layer)

    def _remove_stored_layer(self, layer_ids):
        """
        Removes stored layer
        :param layer_ids: Layer IDs
        :param layer_ids: List
        """
        try:
            self._layers = {
                key: layer
                for key, layer in self._layers.items()
                if layer.id() not in layer_ids
            }
        except (RuntimeError, OSError, Exception) as e:
            raise e

    def _reset_layer(self, layer_ids):
        """
        Resets the current layer
        :param layer_ids: Layer IDs
        :param layer_ids: List
        """
        try:
            if not self._plot_layer:
                return
            if self._plot_layer.layer and \
                    self._plot_layer.layer.id() in layer_ids:
                self._plot_layer.layer = None
        except (RuntimeError, OSError, Exception) as e:
            raise e

    def select_feature(self, row):
        """
        Selects a feature given the row index
        :param row: Preview table view row index
        :type row: Integer
        """
        layer = self._layers.get(self._settings.fpath)
        if not self._plot_layer:
            return
        self._plot_layer.select_feature(layer, [row])

    @staticmethod
    def clear_feature(layer):
        """
        Clears selected features in a layer
        :param layer: Input layer
        :type layer: QgsVectorLayer
        """
        PlotLayer.clear_feature(layer)

    @property
    def dirty(self):
        """
        Returns dirty object
        :return _dirty: Dirty object
        :return _dirty: Dictionary
        """
        return self._dirty

    def is_dirty(self, fpath):
        """
        Checks if the file is valid for import
        :param fpath: Plot import file absolute path
        :type fpath: String
        :return: True
        :rtype: Boolean
        """
        return self._dirty.get(fpath)

    def dirty_file_names(self):
        """
        Returns names of files which are valid for import
        :return file_names: Valid import file names
        :rtype file_names: List
        """
        file_names = [
            QFileInfo(fpath).fileName() for fpath in self._dirty.keys()
        ]
        return file_names

    def remove_dirty(self, fpath):
        """
        Removes file name from dirty class variable
        :param fpath: Plot import file absolute path
        :type fpath: String
        """
        try:
            del self._dirty[fpath]
        except KeyError:
            pass

    def reset_dirty(self):
        """
        Resets the dirty class variable
        """
        self._dirty = {}

    def import_error(self, fpath):
        """
        Returns number of errors encountered on preview
        :return errors: Number of errors on preview
        :return errors: Integer
        """
        errors = self._errors.get(fpath)
        if not errors:
            errors = 0
        return errors

    def reset_errors(self):
        """
        Resets errors
        """
        self._errors = {}

    def _add_attributes(self, attributes):
        """
        Adds attributes to the layer
        :param attributes: Layer attributes
        :type attributes: List
        """
        if not self._plot_layer:
            return
        self._plot_layer.add_attributes(attributes)
        self.layer.updateFields()

    def _feature_area(self, feature):
        """
        :param feature: Feature
        :type feature: QgsFeature
        :return: Feature area
        :rtype: Float
        """
        if not self._plot_layer:
            return
        return self._plot_layer.feature_area(feature)

    @staticmethod
    def _update_feature_attribute(layer, feature, attribute):
        """
        Updates feature attribute value
        :param feature: Feature
        :type feature: QgsFeature
        :param attribute: Attribute to be set (field index, value)
        :type attribute: Tuple
        """
        if not layer or not feature:
            return
        caps = layer.dataProvider().capabilities()
        attribute = {feature.id(): attribute}
        if caps and QgsVectorDataProvider.ChangeAttributeValues:
            layer.dataProvider().changeAttributeValues(attribute)

    def get_headers(self):
        """
        Returns column label configurations
        :return: Column/headers configurations - name and flags
        :rtype: List
        """
        return self._data_service.columns


class ImportPlot:
    """
    Imports plot data
    """
    def __init__(self, model, scheme_id, srid, data_service, col_keys):
        self._model = model
        self._scheme_id = scheme_id
        self._srid = srid
        self._data_service = data_service
        self._options = data_service.save_columns
        self._col_keys = col_keys
        self._geom_column = 0

    def save(self):
        """
        Imports plots data into the database
        :return saved: Number of saved items
        :rtype saved: Integer
        """

        try:
            items = self._import_items()
            imported = Save(
                items,
                self._model.results,
                self._data_service
            ).save()
        except (AttributeError, exc.SQLAlchemyError, Exception) as e:
            raise e
        else:
            return imported

    def _import_items(self):
        """
        Returns import items
        :return import_items: Imported items
        :rtype import_items: Dictionary
        """
        try:
            import_items = {}
            for row, data in enumerate(self._model.results):
                items = []
                for key in self._col_keys:
                    value = data[key]
                    option = self._options[key]
                    if key == self._geom_column:
                        value = "SRID={0};{1}".format(self._srid, value)
                    items.append([option.column, value, option.entity])
                items.append(self._scheme_items())
                import_items[row] = items
            return import_items
        except (AttributeError, KeyError, Exception) as e:
            raise e

    def _scheme_items(self):
        """
        Return scheme items
        :return: Scheme items
        :rtype: List
        """
        option = self._options["SCHEME_ID"]
        return list((option.column, self._scheme_id, option.entity))


class PlotFile(Plot):
    """
    Manages plot import data file settings
    """
    def __init__(self, data_service):
        """
        :param data_service: Plot import file data model service
        :type data_service: PlotImportFileDataService
        """
        self._data_service = data_service
        self._fpath = None
        self._fpaths = []
        self._formats = ["csv", "txt", "pdf"]
        super(PlotFile, self).__init__()

    def set_file_path(self, fpath):
        """
        Sets plot import file absolute path
        :param fpath: Plot import file absolute path
        :type fpath: String
        """
        self._fpath = fpath

    @property
    def file_path(self):
        """
        Returns plot import file absolute path
        :return _fpath: Plot import file absolute path
        :rtype _fpath: String
        """
        return self._fpath

    @property
    def file_paths(self):
        """
        Returns plot import file absolute paths
        :return _fpaths: Plot import file absolute paths
        :rtype _fpaths: List
        """
        return self._fpaths

    def remove_filepath(self, item):
        """
        Removes stored file path
        :param item: Item to be removed
        :type item: Object
        """
        if item in self._fpaths:
            self._fpaths.remove(item)

    def file_extensions(self):
        """
        Returns plot import file extensions
        :return extension: Plot import file extensions
        :rtype extension: List
        """
        extension = ["*." + fmt for fmt in self._formats]
        return extension

    @staticmethod
    def import_as():
        """
        Returns import types
        :return: Import types
        :rtype: List
        """
        return ["Beacons", "Plots", "Servitudes"]

    def delimiter_names(self):
        """
        Returns delimiters full name
        :return names: Delimiters full name
        :rtype names: OrderedDict
        """
        names = OrderedDict()
        for k, d in sorted(self.delimiters.items()):
            name = "{0} {1}".format(k, d)
            if k == "\t":
                k = "t"
                names[k] = "{0} {1}".format(k, d)
            else:
                names[k] = name
        return names

    @property
    def delimiters(self):
        """
        Returns delimiters
        :return: Delimiters
        :rtype: Dictionary
        """
        return OrderedDict({",": "Comma", ";": "Semicolon", "\t": "Tab"})

    @property
    def geometry_options(self):
        """
        Returns a map of expected geometry
        type options for the 'Type' column
        :return geom_options: Geometry type options
        :rtype geom_options: OrderedDict
        """
        geom_options = OrderedDict({"Detect": "Detect"})
        geom_options.update(self._geometry_types)
        return geom_options

    def load(self):
        """
        Loads plot import file data settings
        :return: Plot import file data settings
        :rtype: List
        """
        try:
            qfile = QFile(self._fpath)
            if not qfile.open(QIODevice.ReadOnly):
                raise IOError(unicode(qfile.errorString()))
            self.remove_filepath(self._fpath)
            if not self.is_pdf(self._fpath) and self._is_wkt(self._fpath):
                return self._file_settings(self._fpath)
            return self._file_settings(self._fpath)
        except(IOError, OSError, csv.Error, NotImplementedError, Exception) as e:
            raise e

    def _is_wkt(self, fpath):
        """
        Checks if the plot import file is a valid WKT
        :param fpath: Plot import file absolute path
        :type fpath: String
        :return: Returns true if valid
        :rtype: Boolean
        """
        try:
            fname = QFileInfo(fpath).fileName()
            if QFileInfo(fpath).size() == 0:
                raise NotImplementedError(
                    'The file "{}" is empty.'.format(fname)
                )
            delimiter = self._get_csv_delimiter(fpath)
            with open(fpath, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=delimiter)
                sample_size = 5000
                sample = itertools.islice(csv_reader, sample_size)
                count = 0
                for row, data in enumerate(sample):
                    for value in data:
                        if value is None or isinstance(value, list):
                            continue
                        geom_type, coordinates, geom = self._geometry(value)
                        if geom:
                            count += 1
                total_rows = self.row_count(fpath)
                if self._calc_ratio(total_rows, sample_size, count) < 0.5:
                    raise NotImplementedError(
                        'Most of the lines in "{}" file are invalid'.format(fname)
                    )
        except (IOError, csv.Error, NotImplementedError, Exception) as e:
            raise e
        else:
            return True

    def _file_settings(self, fpath):
        """
        Returns plot import file data settings
        :param fpath: Plot import file absolute path
        :type fpath: String
        :return results: Plot import file data settings
        :rtype results: List
        """
        settings = {}
        items = {}
        try:
            header_row = 1
            row = header_row - 1
            delimiter = self._get_csv_delimiter(fpath)
            for pos, column in enumerate(self._data_service.columns):
                if pos == NAME:
                    settings[pos] = QFileInfo(fpath).fileName()
                elif pos == IMPORT_AS:
                    settings[pos] = unicode(self._get_import_type(fpath))
                elif pos == DELIMITER:
                    settings[pos] = unicode(self._delimiter_name(delimiter))
                elif pos == HEADER_ROW:
                    settings[pos] = header_row \
                        if not self.is_pdf(fpath) else unicode("")
                elif pos == GEOM_FIELD:
                    fields = self.get_csv_fields(fpath, row, delimiter)
                    settings["fields"] = fields
                    if fields:
                        fields = self.geometry_field(fpath, fields, row, delimiter)
                    else:
                        fields = ""
                    settings[pos] = unicode(fields)
                elif pos == GEOM_TYPE:
                    geom_type = self.geometry_type(fpath, row, delimiter)
                    geom_type = self._geometry_types.get(geom_type)
                    if not geom_type:
                        geom_type = "Detect"
                    if self.is_pdf(fpath):
                        geom_type = ""
                    settings[pos] = geom_type
                elif pos == CRS_ID:
                    if not self.is_pdf(fpath):
                        settings[pos] = unicode(WARNING)
                        tip = "Missing Coordinate Reference System (CRS)"
                        items[pos] = self._decoration_tooltip(tip)
                settings["items"] = items
                settings["fpath"] = unicode(fpath)
        except (csv.Error, Exception) as e:
            raise e
        self._fpaths.append(fpath)
        results = [settings]
        return results

    def _get_csv_delimiter(self, fpath):
        """
        Returns default plain text common delimiter
        :param fpath: Plot import file absolute path
        :type fpath: String
        :return: Default common delimiter
        :rtype: Unicode
        """
        if self.is_pdf(fpath):
            return
        try:
            with open(fpath, 'r') as csv_file:
                dialect = csv.Sniffer().sniff(csv_file.readline(4096))
                return dialect.delimiter
        except (csv.Error, Exception) as e:
            raise e

    def _get_import_type(self, fpath):
        """
        Returns default import type based on file extension
        :param fpath: Plot import file absolute path
        :type fpath: String
        :return: Default import type
        :rtype: String
        """
        if self.is_pdf(fpath):
            return "Field Book"
        return "Plots"

    def _delimiter_name(self, delimiter):
        """
        Returns delimiter full name
        :param delimiter: Delimiter
        :type delimiter: String
        :return: Delimiter full name
        :return: String
        """
        if not delimiter:
            return ""
        elif delimiter not in self.delimiters.keys():
            return "{0} {1}".format(delimiter, "Custom")
        elif delimiter == "\t":
            return "{0} {1}".format("t", self.delimiters[delimiter])
        else:
            return "{0} {1}".format(delimiter, self.delimiters[delimiter])

    def get_csv_fields(self, fpath, hrow=0, delimiter=None):
        """
        Returns plain text field names
        :param fpath: Plot import file absolute path
        :type fpath: String
        :param hrow: Header row number
        :type hrow: Integer
        :param delimiter: Delimiter
        :type delimiter: String
        :return fields: CSV field names
        :rtype fields: List
        """
        if self.is_pdf(fpath):
            return
        try:
            with open(fpath, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=delimiter)
                fields = next(
                    (data for row, data in enumerate(csv_reader) if row == hrow), []
                )
                return fields
        except (csv.Error, Exception) as e:
            raise e

    def geometry_field(self, fpath, fields, hrow=0, delimiter=None):
        """
        Returns possible geometry field from
        list of fields given a plain text file
        :param fpath: Plot import file absolute path
        :type fpath: String
        :param fields: CSV field names
        :type fields: List
        :param hrow: Header row number
        :type hrow: Integer
        :param delimiter: Delimiter
        :type delimiter: String
        :return: Geometry field
        :rtype: String
        """
        if self.is_pdf(fpath):
            return
        try:
            with open(fpath, 'r') as csv_file:
                csv_reader = csv.DictReader(
                    csv_file, fieldnames=fields, delimiter=delimiter
                )
                match_count = {field: 0 for field in fields}
                sample = itertools.islice(csv_reader, 5000)
                for row, data in enumerate(sample):
                    if row == hrow:
                        continue
                    for field, value in data.items():
                        if value is None or isinstance(value, list):
                            continue
                        matches = self._reg_exes["type_str"].match(value)
                        if matches:
                            match_count[field] += 1
                return max(
                    match_count.iterkeys(),
                    key=lambda k: match_count[k]
                )
        except (csv.Error, Exception) as e:
            raise e

    @staticmethod
    def _calc_ratio(rows, sample, count):
        """
        Returns ratio of valid WKT lines to total or sample rows
        :param rows: Total rows/lines in a WKT file
        :type rows: Integer
        :param sample: Sampled rows/lines
        :type sample: Integer
        :param count: Number of valid rows
        :type count: Integer
        :return ratio: Ratio of valid WKT lines/rows
        :rtype ratio: Float
        """
        if sample <= rows:
            ratio = float(count) / float(sample)
        else:
            ratio = float(count) / float(rows)
        return ratio

    def row_count(self, fpath):
        """
        Returns total number of rows/lines in a CSV/txt file
        :param fpath: Plot import file absolute path
        :type fpath: String
        :return: Total number of rows/lines
        :rtype: Integer
        """
        if self.is_pdf(fpath):
            return
        try:
            with open(fpath, "r") as csv_file:
                return sum(1 for line in csv_file)
        except (csv.Error, Exception) as e:
            raise e

    def get_headers(self):
        """
        Returns column label configurations
        :return: Column/headers configurations - name and flags
        :rtype: List
        """
        return self._data_service.columns

