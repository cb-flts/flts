"""
/***************************************************************************
Name                 : Search operators
Description          : Operators for performing a basic search
Date                 : 02/April/2020
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


# Expression by data type
NUM_DATE = OrderedDict({
    'Equal to': '=',
    'Less than': '<',
    'Greater than': '>',
    'Not equal to': '<>',
    'Less than or equal to': '<=',
    'Greater than or equal to': '>='
})
TEXT = OrderedDict({
    'Equal to': '=',
    'Like': 'ILIKE'
})
BOOL = OrderedDict({
    'Equal to': '=',
    'Not equal to': '<>'
})

# PostgreSQL type mapping to valid expressions
PG_TYPE_EXPRESSIONS = {
    'character varying': TEXT,
    'varchar': TEXT,
    'character': TEXT,
    'char': TEXT,
    'text': TEXT,
    'integer': NUM_DATE,
    'numeric': NUM_DATE,
    'bigint': NUM_DATE,
    'decimal': NUM_DATE,
    'smallint': NUM_DATE,
    'double precision': NUM_DATE,
    'date': NUM_DATE,
    'timestamp': NUM_DATE,
    'timestamp with time zone': NUM_DATE,
    'boolean': BOOL
}

# Column types that require their values to be quoted in a query
PG_QUOTE_TYPES = [
    'character varying',
    'varchar',
    'character',
    'char',
    'text'
]


# Input value formatters based on the operator
def like_value_formatter(value):
    """
    Formats the search input value for the ILIKE operator.
    :param value: Search value to be formatted.
    :type value: str
    :return: Returns the formatted value for the ILIKE operator.
    :rtype: str
    """
    if not value:
        return value

    return '%{0}%'.format(value)


OPERATOR_VALUE_FORMATTER = {
    'ILIKE': like_value_formatter
}


def operator_format_value(op, value):
    """
    Formats the search input value based on the given operator.
    :param op: Operator type.
    :type op: str
    :param value: Search value to be formatted.
    :type value: object
    :return: Returns the formatted search input value, else an
    unformatted value if there is no formatter defined for the given
    operator.
    :rtype: object
    """
    if not op in OPERATOR_VALUE_FORMATTER:
        return value

    fm_func = OPERATOR_VALUE_FORMATTER.get(op)
    return fm_func(value)