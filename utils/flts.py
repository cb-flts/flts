"""
/***************************************************************************
Name                 : FLTS utilities
Description          : FLTS utility function.
Date                 : 11/March/2020
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
from stdm.data.pg_utils import vector_layer


def lht_plot_layer(scheme_id=-1, layer_name='Plot'):
    """
    Creates the plot layer for the given scheme and sets the name to plot.
    :param scheme_id: Primary key of the scheme for which the plots belong to
    and loads all the plots within it. If -1 it loads all plots in the table.
    :type scheme_id: int
    :param layer_name: Name assigned to the layer containing the plots.
    type: layer_name: str
    """
    if scheme_id == -1:
        sql = ''
    else:
        sql = 'scheme_id={0}'.format(scheme_id)

    return vector_layer(
        table_name='cb_plot',
        sql=sql,
        key='',
        geom_column='geom',
        layer_name=layer_name
    )
