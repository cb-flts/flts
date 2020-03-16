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
    QDateTime,
    QFile
)
from qgis.core import (
    QgsMapLayerRegistry
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
    Utility function that loads plots that belng to a specific scheme.
    """
    scheme_plot_layer = lht_plot_layer(plot.scheme_id, CERTIFICATE_PLOT)
    QgsMapLayerRegistry.instance().addMapLayer(scheme_plot_layer)
    if QFile.exists(STYLE_FILE):
        scheme_plot_layer.loadNamedStyle(STYLE_FILE)
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

