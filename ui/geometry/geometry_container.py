from collections import OrderedDict

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDockWidget, QApplication, QStatusBar
from qgis.PyQt.QtCore import NULL
from qgis.core import QgsMapLayer

from stdm.data.pg_utils import spatial_tables, pg_views
from stdm.ui.feature_details import LayerSelectionHandler

from stdm.data.configuration import entity_model
from stdm.settings import current_profile
from stdm.ui.forms.widgets import ColumnWidgetRegistry
from ui_geometry_container import Ui_GeometryContainer



class GeometryToolsContainer(QDockWidget, Ui_GeometryContainer, LayerSelectionHandler):
    """
    The logic for the spatial entity details dock widget.
    """

    def __init__(self, iface, plugin):
        """
        Initializes the DetailsDockWidget.
        :param iface: The QGIS interface
        :type iface: Object
        :param plugin: The STDM plugin object
        :type plugin: Object
        """
        QDockWidget.__init__(self, iface.mainWindow())
        self.setupUi(self)
        self.plugin = plugin
        self.iface = iface
        self._entity = None
        LayerSelectionHandler.__init__(self, iface, plugin)
        self.setBaseSize(300, 5000)

    def init_dock(self):
        """
        Creates dock on right dock widget area and set window title.
        """
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self)
        self.init_signals()
        # self.set_style()

    def init_signals(self):
        self.geom_tools_combo.currentIndexChanged.connect(
            self.on_geom_tools_combo_changed)

    def on_geom_tools_combo_changed(self, index):
        self.geom_tools_widgets.setCurrentIndex(index)

    def close_dock(self, tool):
        """
        Closes the dock by replacing select tool with pan tool,
        clearing feature selection, and hiding the dock.
        :param tool: Feature detail tool button
        :type tool: QAction
        """
        self.iface.actionPan().trigger()
        tool.setChecked(False)
        self.clear_feature_selection()
        self.clear_sel_highlight()
        self.hide()

    def closeEvent(self, event):
        """
        On close of the dock window, this event is executed
        to run close_dock method
        :param event: The close event
        :type event: QCloseEvent
        :return: None
        """
        if self.plugin is None:
            return
        self.close_dock(
            self.plugin.geom_tools_cont_act
        )

    def hideEvent(self, event):
        """
        Listens to the hide event of the dock and properly close the dock
        using the close_dock method.
        :param event: The close event
        :type event: QCloseEvent
        """
        self.close_dock(
            self.plugin.geom_tools_cont_act
        )


    def activate_geometry_tools(self, button_clicked=True):
        """
        A slot raised when the feature details button is clicked.
        :param button_clicked: A boolean to identify if it is activated
        because of button click or because of change in the active layer.
        :type button_clicked: Boolean
        """
        # Get and set the active layer.
        self.layer = self.iface.activeLayer()
        # if no active layer, show error message
        # and uncheck the feature tool
        if self.layer is None:
            if button_clicked:
                self.active_layer_check()
            self.plugin.geom_tools_cont_act.setChecked(False)
            return
        # If the button is unchecked, close dock.
        if not self.plugin.geom_tools_cont_act.isChecked():
            self.close_dock(self.plugin.geom_tools_cont_act)
            self.geometry_tools = None
            return
        # if the selected layer is not an STDM layer,
        # show not feature layer.
        if not self.stdm_layer(self.layer):
            if button_clicked and self.isHidden():
                # show popup message if dock is hidden and button clicked

                self.non_stdm_layer_error()
                self.plugin.geom_tools_cont_act.setChecked(False)

        # If the selected layer is feature layer, get data and
        # display geometry_tools in a dock widget
        else:
            self.prepare_for_selection()



    def prepare_for_selection(self):
        """
        Prepares the dock widget for data loading.
        """
        self.init_dock()

        self.activate_select_tool()
        self.update_layer_source(self.layer)


    def activate_select_tool(self):
        """
        Enables the select tool to be used to select features.
        """
        self.iface.actionSelect().trigger()
        layer_select_tool = self.iface.mapCanvas().mapTool()
        layer_select_tool.deactivated.connect(
            self.disable_feature_details_btn
        )

        layer_select_tool.activate()


    def disable_feature_details_btn(self):
        """
        Disables features details button.
        :return:
        :rtype:
        """
        self.plugin.geom_tools_cont_act.setChecked(False)


    def update_layer_source(self, active_layer):
        """
        Updates the layer source in case of layer change.
        :param active_layer: The active layer on the canvas.
        :type active_layer: QgsVectorLayer
        """
        if active_layer.type() != QgsMapLayer.VectorLayer:
            return
        # set entity from active layer in the child class
        self.set_layer_entity()
        # set entity for the super class DetailModel
        self.set_entity(self.entity)


    def feature_model(self, entity, id):
        """
        Gets the model of an entity based on an id and the entity.
        :param entity: Entity
        :type entity: Object
        :param id: Id of the record
        :type id: Integer
        :return: SQLAlchemy result proxy
        :rtype: Object
        """
        model = entity_model(entity)
        model_obj = model()
        result = model_obj.queryObject().filter(model.id == id).all()
        if len(result) > 0:
            return result[0]
        else:
            return None

    def set_layer_entity(self):
        """
        Sets the entity property using the layer table.
        """
        self.layer_table = self.get_layer_source(
            self.iface.activeLayer()
        )
        if self.layer_table is None:
            return

        if self.layer_table in spatial_tables() and \
                        self.layer_table not in pg_views():
            self.entity = self.current_profile.entity_by_name(self.layer_table)


    def set_entity(self, entity):
        """
        Sets the spatial entity.
        :param entity: The entity object
        :type entity: Object
        """
        self._entity = entity