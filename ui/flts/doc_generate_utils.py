"""
/***************************************************************************
Name                 : Document Generator Utilities
Description          : Document generator wrapper utility functions.
Date                 : 12/March/2020
copyright            : (C) 2020 by Joseph Kariuki
email                : joehene@gmail.com
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
import time

from PyQt4.QtCore import (
    Qt,
    QDateTime,
    QFile
)
from qgis.core import (
    QgsMapLayerRegistry,
    QgsRuleBasedRendererV2,
    QgsSymbolV2
)
from qgis.utils import iface
from qgis.core import QgsApplication

from sqlalchemy.sql.expression import text

from stdm.settings import current_profile
from stdm.data.configuration import entity_model
from stdm.data.pg_utils import _execute
import stdm.data
from stdm.utils.flts import lht_plot_layer
from stdm import STYLES_DIR

CERTIFICATE_PLOT = 'Certificate Plot'
STYLE_FILE = '{0}/scheme_plots_label.qml'.format(STYLES_DIR)


def certificate_preprocess(plot, plots):
    """
    Utility function that loads and renders plots that belong to a specific
    scheme.
    """
    scheme_plot_layer = lht_plot_layer(plot.scheme_id, CERTIFICATE_PLOT)
    QgsMapLayerRegistry.instance().addMapLayer(scheme_plot_layer)
    # if QFile.exists(STYLE_FILE):
    #     scheme_plot_layer.loadNamedStyle(STYLE_FILE)
    #     scheme_plot_layer.triggerRepaint()
    # iface.mapCanvas().setExtent(scheme_plot_layer.extent())
    # QgsApplication.processEvents()

    # Styling reference plot using primary key
    filter_exp = '"id" = ' + str(plot.id)
    scheme_symbol = QgsSymbolV2.defaultSymbol(
        scheme_plot_layer.geometryType()
    )
    rule_renderer = QgsRuleBasedRendererV2(scheme_symbol)
    root_rule = rule_renderer.rootRule()

    # Rule for highlighting reference plot
    scheme_rule = root_rule.children()[0].clone()
    scheme_rule.setLabel('Reference Plot')
    scheme_rule.setFilterExpression(filter_exp)
    scheme_symbol_layer = scheme_rule.symbol().symbolLayer(0)
    scheme_symbol_layer.setFillColor(Qt.yellow)
    scheme_symbol_layer.setOutlineColor(Qt.black)
    scheme_symbol_layer.setBorderWidth(0.5)
    root_rule.appendChild(scheme_rule)

    # Rule for other plots
    def_rule = root_rule.children()[0].clone()
    def_rule.setLabel('Plots')
    def_rule.setIsElse(True)
    def_symbol_layer = def_rule.symbol().symbolLayer(0)
    def_symbol_layer.setFillColor(Qt.transparent)
    def_symbol_layer.setOutlineColor(Qt.black)
    root_rule.appendChild(def_rule)

    # Remove default rule
    root_rule.removeChildAt(0)

    # Set renderer
    scheme_plot_layer.setRendererV2(rule_renderer)

    # Enable labeling
    scheme_plot_layer.setCustomProperty("labeling", "pal")
    scheme_plot_layer.setCustomProperty("labeling/enabled", "true")
    scheme_plot_layer.setCustomProperty("labeling/fontFamily", "Arial")
    scheme_plot_layer.setCustomProperty("labeling/fontSize", "8")
    scheme_plot_layer.setCustomProperty("labeling/fieldName", "plot_number")
    scheme_plot_layer.setCustomProperty("labeling/placement", "0")

    scheme_plot_layer.triggerRepaint()

    iface.mapCanvas().setExtent(scheme_plot_layer.extent())
    QgsApplication.processEvents()

    return True


def certificate_postprocess(plot, plots):
    """
    Updates the certificate details and removes the layers after generation
    of the certificate.
    """
    cert_number = pg_certificate_number()
    user_name = stdm.data.app_dbconn.User.UserName
    curr_datetime = QDateTime.currentDateTime().toPyDateTime()
    curr_profile = current_profile()
    if not current_profile:
        return

    cert_entity = curr_profile.entity('Certificate')
    if not cert_entity:
        return
    cert_model = entity_model(cert_entity)
    cert_obj = cert_model()
    cert_obj.plot_id = plot.id
    cert_obj.certificate_number = cert_number
    cert_obj.production_date = curr_datetime
    cert_obj.prod_user = user_name
    cert_obj.save()

    # Remove certificate plot layer
    layers = QgsMapLayerRegistry.instance().mapLayersByName(CERTIFICATE_PLOT)
    if len(layers) > 0:
        QgsMapLayerRegistry.instance().removeMapLayer(layers[0])


def pg_certificate_number():
    """
    Get flts certificate view from the database
    """
    t = text('SELECT flts_gen_cert_number();')
    result = _execute(t)
    cert_number = ''
    for row in result:
        cert_number = row[0]
    return cert_number

