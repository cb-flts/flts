"""
/***************************************************************************
Name                 : Search History
Description          : Saves search history to a SQLite database.
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
import logging
from datetime import datetime
from PyQt4.QtGui import QDesktopServices

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    exc,
    func,
    create_engine,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Numeric,
    Text,
    Boolean
)
from sqlalchemy.orm import (
    relationship,
    backref,
    sessionmaker
)


LOGGER = logging.getLogger('stdm')

# Maximum number of saved searches per column
MAX_SEARCH_HISTORY = 50

# SQLite file to store searches
SEARCH_HISTORY_FILE = QDesktopServices.storageLocation(
    QDesktopServices.HomeLocation
) + '/.stdm/search/history.db'

url = 'sqlite:///{0}'.format(SEARCH_HISTORY_FILE)
engine = create_engine(url, echo=False)
Base = declarative_base()


class SearchDataSource(Base):
    """
    Stores the names of the data source.
    """
    __tablename__ = 'cb_search_source'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    columns = relationship('SearchColumn', backref='datasource')


class SearchColumn(Base):
    """
    Stores the column names of the data source.
    """
    __tablename__ = 'cb_search_column'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    source_id = Column(Integer, ForeignKey('cb_search_source.id'))
    searches = relationship('SearchTerm', backref='column')


class SearchTerm(Base):
    """
    Stores the search terms for a given column.
    """
    __tablename__ = 'cb_search_term'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    search_date = Column(DateTime())
    column_id = Column(Integer, ForeignKey('cb_search_column.id'))


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def column_searches(ds, column):
    """
    Gets the previous searches for a column in the given data source.
    :param ds: Data source name.
    :type ds: str
    :param column: Column name.
    :type column: str
    :return: Returns the previously saved searches for a column in the
    given data source.
    :rtype: list
    """
    base_query = _search_term_base_query(ds, column)
    if not base_query:
        return []

    s_terms = base_query.all()
    return [st.name for st in s_terms]


def _search_term_beyond_limit(ds, column):
    # Checks if the search term is beyond the MAX_SEARCH_HISTORY limit
    # and deletes the oldest search term if limit exceeded.
    base_query = _search_term_base_query(ds, column)
    if not base_query:
        return

    rec_count = base_query.count()
    if rec_count >= MAX_SEARCH_HISTORY:
        # Delete oldest search term
        oldest_term = base_query.order_by(
            SearchTerm.search_date.asc()
        ).first()
        if oldest_term:
            try:
                session.delete(oldest_term)
                session.commit()
            except exc.SQLAlchemyError as db_error:
                session.rollback()
                LOGGER.debug(str(db_error))


def _search_term_base_query(ds, column):
    # Base search term query definition
    try:
        return session.query(SearchTerm).join(
                SearchColumn
            ).join(
                SearchDataSource
            ).filter(
                SearchDataSource.name == ds
            ).filter(
                SearchColumn.name == column
            )
    except exc.SQLAlchemyError as db_error:
        session.rollback()
        LOGGER.debug(str(db_error))
        return None


def save_column_search(ds, column, term):
    """
    Saves the search details into the local DB.
    :param ds: Data source name.
    :type ds: str
    :param column: Column name
    :type column: str
    :param term: Search word
    :type term: str
    """
    try:
        # Check if data source exists, if not create
        data_source = session.query(SearchDataSource).filter_by(
            name=ds
        ).first()
        if not data_source:
            data_source = SearchDataSource(name=ds)
            _save_column_term(data_source, column, term)
            session.add(data_source)
            session.commit()

        # Check if column exists, if not create
        search_col = session.query(SearchColumn).filter_by(
            name=column
        ).first()
        if not search_col:
            search_col = _save_column_term(data_source, column, term)
            session.commit()

        # Check if search term exists, if not create
        search_term = session.query(SearchTerm).filter(
            func.lower(SearchTerm.name) == func.lower(term)
        ).first()
        if not search_term:
            # Check if MAX_SEARCH_HISTORY limit has been exceeded before
            # adding a new search term. Delete oldest if limit is exceeded
            _search_term_beyond_limit(ds, column)
            search_term = _save_search_term(search_col, term)
            session.commit()
        else:
            # If it already exists then update the time
            search_term.search_date = datetime.now()
            session.commit()

    except exc.SQLAlchemyError as db_error:
        session.rollback()
        LOGGER.debug(str(db_error))


def _save_column_term(ds, column, term):
    # Creates column and search term information.
    search_col = SearchColumn(name=column)
    search_col.datasource = ds
    _save_search_term(search_col, term)
    session.add(search_col)

    return search_col


def _save_search_term(column, term):
    # Creates search term info for the given column.
    s_term = SearchTerm(
        name=term,
        search_date=datetime.now()
    )
    s_term.column = column
    session.add(s_term)

    return s_term
