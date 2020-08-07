"""
/***************************************************************************
Name                 : Plot Import Widget
Description          : Widget for managing importing of a scheme plot.
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
import copy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import QgsGenericProjectionSelector
from qgis.utils import iface
from sqlalchemy import exc
from stdm.settings.registryconfig import (
    last_document_path,
    set_last_document_path
)
from ...notification import NotificationBar
from stdm.ui.flts.workflow_manager.config import (
    SchemeMessageBox,
    StyleSheet,
    TabIcons,
)
from stdm.ui.flts.workflow_manager.data_service import PlotSTRDataService
from stdm.ui.flts.workflow_manager.plot import (
    ImportPlot,
    PlotFile,
    PlotPreview,
    SavePlotSTR
)
from stdm.ui.flts.workflow_manager.model import WorkflowManagerModel
from stdm.ui.flts.workflow_manager.delegates.plot_file_delegate import PlotFileDelegate
from stdm.ui.flts.workflow_manager.components.plot_import_component import PlotImportComponent
from stdm.ui.flts.workflow_manager.field_book_manager import FieldBookManager
from stdm.ui.flts.workflow_manager.pdf_viewer_widget import PDFViewerWidget


NAME, IMPORT_AS, DELIMITER, HEADER_ROW, CRS_ID, \
GEOM_FIELD, GEOM_TYPE = range(7)
NAM_CRS = [
    "EPSG:29373", "EPSG:29375",
    "EPSG:29377", "EPSG:29379",
    "EPSG:29381", "EPSG:29383",
    "EPSG:29385", "EPSG:4006"
]


class PlotImportWidget(QWidget):
    """
    A widget to import and preview plots of a scheme.
    Called from the Import Plot module.
    """
    def __init__(self, widget_properties, profile, scheme_id, scheme_number, parent=None):
        super(QWidget, self).__init__(parent)
        self._profile = profile
        self._scheme_id = scheme_id
        self._parent = parent
        self.notif_bar = NotificationBar(parent.vlNotification)
        data_service = widget_properties["data_service"]
        self._file_service = data_service["plot_file"]
        self._file_service = self._file_service()
        self._plot_preview_service = data_service["plot_preview"]
        self._plot_file = PlotFile(self._file_service)
        self._previewed = {}
        self.is_dirty = None
        self._import_counter = None
        import_component = PlotImportComponent()
        toolbar = import_component.components
        self._add_button = toolbar["addFiles"]
        self._remove_button = toolbar["removeFiles"]
        self._set_crs_button = toolbar["setCRS"]
        self._preview_button = toolbar["Preview"]
        self._import_button = toolbar["plotsImportButton"]
        header_style = StyleSheet().header_style
        self._file_table_view = QTableView(self)
        self.model = WorkflowManagerModel(self._file_service)
        self._file_table_view.setModel(self.model)
        file_delegate = PlotFileDelegate(self._file_service, self)
        file_delegate = file_delegate.delegate()
        self._file_table_view.setItemDelegate(file_delegate)
        self._file_table_view.setShowGrid(False)
        style = 'QHeaderView::section{color: #2F4F4F;}'
        self._file_table_view.horizontalHeader().setStyleSheet(style)
        self._file_table_view.setSelectionBehavior(QTableView.SelectRows)
        self._file_table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self._preview_table_view = QTableView(self)
        self._preview_models = {}
        self._preview_data_service = self._preview_model = None
        self._plot_preview = PlotPreview(scheme_number, self._preview_data_service)
        self._preview_model = WorkflowManagerModel(self._preview_data_service)
        self._preview_table_view.setModel(self._preview_model)
        self._preview_table_view.setAlternatingRowColors(True)
        self._preview_table_view.setShowGrid(False)
        self._preview_table_view.horizontalHeader().setStyleSheet(header_style)
        self._preview_table_view.setSelectionBehavior(QTableView.SelectRows)
        self._preview_table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        file_layout = QVBoxLayout()
        file_layout.addWidget(self._file_table_view)
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self._preview_table_view)
        file_groupbox = QGroupBox("Added files")
        self._preview_groupbox = QGroupBox("File content")
        file_groupbox.setLayout(file_layout)
        self._preview_groupbox.setLayout(preview_layout)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(file_groupbox)
        splitter.addWidget(self._preview_groupbox)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        layout = QVBoxLayout()
        layout.addLayout(import_component.layout)
        layout.addWidget(splitter)
        self.setLayout(layout)
        self._parent.paginationFrame.hide()
        self._dock_widget.closing.connect(self._on_dock_close)
        self._parent.removeTab.connect(self._on_remove_tab)
        self._file_table_view.clicked.connect(self._on_file_select)
        self._add_button.clicked.connect(self._add_file)
        self._remove_button.clicked.connect(self._remove)
        self._set_crs_button.clicked.connect(self._set_crs)
        self._preview_button.clicked.connect(self._preview)
        self._import_button.clicked.connect(self._import)
        _selection_model = self._preview_table_view.selectionModel()
        _selection_model.selectionChanged.connect(self._on_preview_select)
        QTimer.singleShot(0, self._set_file_path)
        self._scheme_number = scheme_number

        # Object for managing the upload of field book
        self._field_bk_mgr = FieldBookManager(self)
        self._field_bk_mgr.uploaded.connect(
            self._on_field_bk_uploaded
        )
        self._field_bk_mgr.removed.connect(
            self._on_field_bk_removed
        )

    def _set_file_path(self):
        """
        Sets plot import file absolute path
        """
        fpath = last_document_path()
        if not fpath or not QFile.exists(fpath):
            fpath = "."
        self._plot_file.set_file_path(fpath)

    def _add_file(self):
        """
        Adds plot import file data settings into the file table view
        """
        fpath = QFileInfo(self._plot_file.file_path).path()
        extensions = " ".join(self._plot_file.file_extensions())
        fpath = QFileDialog.getOpenFileName(
            self,
            "Workflow Manager - Plot Add Files",
            fpath,
            "Plot Import files {}".format(extensions)
        )
        if fpath and fpath not in self._plot_file.file_paths:
            try:
                # Check if its a PDF and can be uploaded i.e. no other
                # existing field books
                if self._plot_file.is_pdf(fpath) and \
                        not self._can_upload_field_book():
                    return

                self._plot_file.set_file_path(fpath)
                set_last_document_path(fpath)

                if not self.model.results:
                    self._load(self.model, self._plot_file)
                else:
                    self._insert_file()

                # If field book then validate and upload in the background
                if self._plot_file.is_pdf(fpath):
                    self._upload_field_book(fpath)
            except(IOError, OSError, Exception) as e:
                self._show_critical_message(
                    "Workflow Manager - Plot Add Files",
                    "Failed to load: {}".format(e)
                )
            else:
                self._file_table_view.verticalHeader().setDefaultSectionSize(21)
                self._file_table_view.horizontalHeader().\
                    setStretchLastSection(True)

    def _insert_file(self):
        """
        Inserts plot import file data settings into the table view
        """
        position = self.model.rowCount()
        self.model.insertRows(position)

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

    def _on_dock_close(self, event):
        """
        Handles on parent QDockWidget close event
        """
        if not self._plot_preview or not self._plot_preview.dirty:
            event.accept()
            return
        if not self._ok_to_discard():
            event.ignore()
            return
        event.accept()
        self._remove_layers()
        self._plot_preview.reset_errors()
        self._plot_preview.reset_dirty()

    def _on_remove_tab(self):
        """
        Handles on tab remove event
        """
        if not self._plot_preview or not self._plot_preview.dirty:
            self.is_dirty = False
            return
        if not self._ok_to_discard():
            self.is_dirty = True
            return
        self._remove_layers()
        self.is_dirty = False

    def _ok_to_discard(self):
        """
        Returns discard data message box reply
        :return: True or False
        """
        fnames = self._plot_preview.dirty_file_names()
        title = "Workflow Manager - Plot Import"
        msg = "Action will discard data. " \
              "Do you want to proceed? \n\n {}".format(", ".join(fnames))
        return self._show_question_message(title, msg)

    def _remove_layers(self):
        """
        Removes all layers from the
        registry/map canvas given layer IDs
        """
        if self._plot_preview:
            self._plot_preview.remove_layers()

    def _on_file_select(self, index):
        """
        Enables toolbar buttons on selecting a file record
        :param index: Table view item identifier
        :type index: QModelIndex
        """
        self._enable_widgets(self._toolbar_buttons)
        self._enable_crs_button()
        self._enable_disable_preview_import_buttons()

    def _remove(self):
        """
        Removes plot import file from table view
        """
        self._import_counter = None
        fpath = self._selected_file()
        if not fpath or not self._ok_to_remove(fpath):
            return
        if self._import_counter != 0:
            self._remove_file(True)
            self._plot_preview.remove_error(fpath)

    def _ok_to_remove(self, fpath):
        """
        Authorize action on removing a file
        :param fpath: Plot import file absolute path
        :type fpath: String
        :return: True or False
        :rtype: Boolean
        """
        fname = QFileInfo(fpath).fileName()
        title = "Workflow Manager - Plot Add Files"
        msg = 'Remove "{}" and its settings?'.format(fname)
        if not self._plot_preview:
            return self._show_question_message(title, msg)
        elif not self._plot_preview.is_dirty(fpath):
            return self._show_question_message(title, msg)
        return self._ok_to_continue(fpath)

    def _ok_to_continue(self, fpath):
        """
        Authorize action on a dirty file
        :param fpath: Plot import file absolute path
        :type fpath: String
        :return: True or False
        :rtype: Boolean
        """
        if self._plot_preview.is_dirty(fpath):
            fname = QFileInfo(fpath).fileName()
            reply = QMessageBox.question(
                self,
                "Workflow Manager - Plot Import",
                'Do you want to import "{}" data?'.format(fname),
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                if self._import_error_message(fpath):
                    return False
                self._import_plot()
            else:
                self._remove_dirty(fpath)
        return True

    def _preview(self):
        """
        Previews selected plot import file content
        """
        self._import_counter = None
        index = self._current_index(self._file_table_view)
        if index is None:
            return
        row = index.row()
        settings = self._file_settings(row)
        fpath = settings.get("fpath")
        if not self._plot_file.is_pdf(fpath):
            if self._crs_not_set(row):
                return
            self._clear_feature()
            import_type = settings.get(IMPORT_AS)
            self._set_preview_data_service(import_type)
            self._plot_preview._data_service = \
                self._preview_data_service[import_type]
            self._plot_preview.set_settings(settings)
            self._preview_load()
            self._set_preview_groupbox_title(settings[NAME])
            self._set_preview_models(fpath)
            self._previewed[fpath] = fpath
        else:
            self._on_preview_field_book(fpath)

    def _on_preview_field_book(self, path):
        # Loads a window for previewing the field book.
        status = self._field_bk_mgr.upload_status(path)
        self.notif_bar.clear()

        if status == -1:
            msg = '{0} could not be found in the list of uploaded ' \
                  'documents'.format(path)
            self.notif_bar.insertWarningNotification(msg)
        elif status == FieldBookManager.NOT_UPLOADED:
            msg = 'Field book is currently being uploaded, please try again ' \
                  'in a few moments'
            self.notif_bar.insertInformationNotification(msg)
        elif status == FieldBookManager.ERROR:
            err = self._field_bk_mgr.upload_error_message(path)
            msg = 'Error in uploading field book: {0}'.format(err)
            self.notif_bar.insertWarningNotification(msg)
        elif status == FieldBookManager.SUCCESS:
            doc_uuid = self._field_bk_mgr.document_uuid(path)
            doc_name = self._field_bk_mgr.document_name(path)
            if not doc_uuid or not doc_name:
                msg = 'An error occurred, the field book cannot be previewed.'
                self.notif_bar.insertWarningNotification(msg)
                return

            pdf_viewer = PDFViewerWidget(
                doc_uuid,
                doc_name
            )
            pdf_viewer.view_document()

            # Flag the field book as viewed
            self._previewed[path] = path

    def _clear_feature(self):
        """
        On add/previewing clear selected features
        """
        if self._plot_preview.layer:
            self._plot_preview.clear_feature(
                self._plot_preview.layer
            )

    def _set_preview_data_service(self, import_type):
        """
        Sets plot preview data service
        :param import_type: Plot file import type
        :type import_type: String
        """
        if not self._preview_data_service:
            self._preview_data_service = {}
        if import_type not in self._preview_data_service:
            service = self._preview_service(import_type)
            self._preview_data_service[import_type] = service

    def _set_preview_models(self, fpath):
        """
        Sets plot preview models
        :param fpath: Plot import file absolute path
        :type fpath: String
        """
        self._preview_models[fpath] = copy.copy(self._preview_model)

    def _preview_service(self, import_type):
        """
        Returns plot preview data service
        :param import_type: Plot file import type
        :type import_type: String
        :return: Plot preview data service object
        :rtype: Service Object
        """
        service = self._plot_preview_service(import_type)
        return service(self._profile, self._scheme_id)

    def _can_upload_field_book(self):
        # Checks if a field book can be uploaded.
        if not self._field_bk_mgr.is_active:
            msg = 'Field books cannot be uploaded at this time as there are ' \
                  'issues in connecting to the CMIS Server.'
            self._show_critical_message(
                'Uploading Field Book',
                msg
            )
            return False

        field_bk_count = self._field_bk_mgr.field_book_count()
        if field_bk_count > 0:
            self._show_critical_message(
                'Existing Field Book',
                'Only one field book can be uploaded for a scheme, please '
                'remove the current one and try again.')
            return False

        return True

    def _upload_field_book(self, file_path):
        # Uploads the field book to the CMIS server temp directory
        # First check if there are prior uploads of the field book
        self._field_bk_mgr.upload_field_book(file_path)

    def _on_field_bk_uploaded(self, upload_info):
        # Slot raised when a field book has been uploaded to the CMIS
        # server temp repository.
        file_path = upload_info[0]
        status = upload_info[1]
        # To insert additional operations required from the upload status

    def _on_field_bk_removed(self, remove_info):
        # Slot raised when a document is removed from the CMIS server.
        file_path = remove_info[0]
        success = remove_info[1]
        err_msg = remove_info[2]
        if success:
            msg = '\'{0}\' has been successfully removed from the document ' \
                  'repository'.format(file_path)
            self.notif_bar.insertSuccessNotification(msg)
        else:
            msg = 'Error in removing \'{0}\': {1}'.format(
                file_path,
                err_msg
            )
            self.notif_bar.insertErrorNotification(msg)

    def _crs_not_set(self, row):
        """
        Returns Tru if CRS is not set
        :param row: Table view item identifier
        :type row: Integer
        :return True: True if CRS is not set
        :return True: Boolean
        """
        if not self._is_crs(row):
            title = "Workflow Manager - Plot Preview"
            msg = "Coordinate reference system (CRS) is missing.\n" \
                  "Do you want to set it to preview?"
            if not self._show_question_message(title, msg):
                return True
            self._set_crs()

    def _is_crs(self, row):
        """
        Returns true if coordinate reference
        system (CRS) has been set. Otherwise none
        :param row: Table view item identifier
        :type row: Integer
        :return: True
        :return: Boolean
        """
        crs_id = self.model.data(self.model.index(row, CRS_ID))
        if crs_id:
            return True

    def _preview_load(self):
        """
        Loads selected plot import file content
        """
        try:
            self._load(self._preview_model, self._plot_preview)
        except(IOError, OSError) as e:
            self._show_critical_message(
                "Workflow Manager - Plot Preview",
                "Failed to load: {}".format(e)
            )
        else:
            self._preview_table_view.horizontalHeader(). \
                setStretchLastSection(True)

    def _import(self):
        """
        Imports selected plot import file content
        """
        index = self._current_index(self._file_table_view)
        if index is None:
            return
        row = index.row()
        settings = self._file_settings(row)
        import_type = settings.get(IMPORT_AS)
        fpath = self.model.results[row].get("fpath")

        if self._previewed_message(fpath) or \
                self._import_error_message(fpath) or \
                not self._ok_to_import(index, import_type):
            return

        # Notify about import process of field book
        if self._plot_file.is_pdf(fpath):
            msg = 'The field book will not be imported separately but rather ' \
                  'together with the plots when they are being uploaded.'
            self._show_critical_message(
                'Field Book Upload',
                msg
            )
            return

        else:
            # Checks if a field book has been uploaded
            if not self._contains_field_book():
                msg = 'Plots cannot be imported without an accompanying field ' \
                      'book, please add one and try again.'
                self._show_critical_message(
                    'Plots Import',
                    msg
                )
                return

        self._import_plot()
        if self._import_counter != 0:
            self._remove_file(False)
            # Select and remove field book
            self._select_field_book()
            self._remove_file(False)

    def _import_plot(self):
        """
        Imports plot values
        """
        self.notif_bar.clear()
        index = self._current_index(self._file_table_view)
        if index is None:
            return
        row = index.row()
        fpath = self.model.results[row].get("fpath")
        model = self._preview_models[fpath]
        settings = self._file_settings(row)
        crs_id = settings.get(CRS_ID)
        srid_id = None
        import_type = settings.get(IMPORT_AS)
        data_service = self._preview_data_service[import_type]
        columns = self._import_type_columns(import_type)

        try:
            # Move field book to permanent plot directory in CMIS server
            sch_number = self._scheme_number.replace(" / ", "_")
            sch_fld_bk_id = self._field_bk_mgr.persist_documents(
                sch_number,
                self._scheme_id
            )
            import_plot = ImportPlot(
                model, self._scheme_id, data_service, columns, crs_id,
                srid_id, sch_fld_bk_id
            )
            self._import_counter = import_plot.save()

        except (AttributeError, exc.SQLAlchemyError, Exception) as e:
            self._show_critical_message(
                "Workflow Manager - Plot Import",
                "Failed to import: {}".format(e)
            )
        else:
            if self._import_counter == 0:
                msg = "Failed to import. {0} {1} imported ".\
                    format(self._import_counter, import_type.lower())
                self.notif_bar.insertWarningNotification(msg)
                return
            msg = "Successfully imported {0} {1}, the third examination can " \
                  "commence.".\
                format(self._import_counter, import_type.lower())
            self.notif_bar.insertInformationNotification(msg)
            if import_type == "Plots":
                self._save_plot_str(fpath)

    def _save_plot_str(self, fpath):
        """
        Saves Plot (spatial unit) and  Holders (Party)
        Social Tenure Relationship (STR) database record(s)
        :param fpath: Plot import file absolute path
        :type fpath: String
        """
        plot_numbers = self._plot_preview.plot_numbers.get(fpath)
        if not plot_numbers:
            return
        model = self._preview_models[fpath]
        str_data_service = PlotSTRDataService(self._profile, self._scheme_id)
        plot_str = SavePlotSTR(
            str_data_service,
            model.results,
            plot_numbers,
            self._scheme_id
        )
        plot_str.save()

    @staticmethod
    def _import_type_columns(import_type):
        """
        Return preview table view column positions
        based on import type (Plots, Beacons or Servitudes)
        :param import_type: Import type
        :param import_type: String
        :return: Preview table view column positions
        :rtype: Integer
        """
        if import_type == "Plots":
            return range(4)
            # TODO: On success update upload_status in the Scheme entity
            #  Update method to be coded in the ImportPlot Class
        elif import_type == "Servitudes":
            return 0
        else:
            return range(3)

    def _file_settings(self, row):
        """
        Returns plot import file data settings
        :param row: Table view item identifier
        :type row: Integer
        :return: Plot import file data settings
        :rtype: Dictionary
        """
        return self.model.results[row]

    def _previewed_message(self, fpath):
        """
        Returns True if the plot import file has not been previewed
        :param fpath: Plot import file absolute path
        :type fpath: String
        :return: True if not previewed
        :rtype: Boolean
        """
        if fpath not in self._previewed:
            fname = QFileInfo(fpath).fileName()
            self._show_critical_message(
                "Workflow Manager - Plot Import",
                "{} has not been previewed. "
                "Kindly preview then import.".format(fname)
            )
            return True

    def _ok_to_import(self, index, import_type):
        """
        Returns import data message box reply
        :return: True or False.
        """
        row = index.row()
        fpath = self.model.results[row].get("fpath")
        fname = QFileInfo(fpath).fileName()
        import_type = import_type.lower()
        title = "Workflow Manager - Plot Import"
        msg = "Do you want to import {0} in {1} file ?".format(import_type, fname)
        return self._show_question_message(title, msg)

    def _import_error_message(self, fpath):
        """
        Returns True if there is an error in the import file
        :param fpath: Plot import file absolute path
        :type fpath: String
        :return: True if import error
        :rtype: Boolean
        """
        error = self._plot_preview.import_error(fpath)
        if error > 0:
            self._show_critical_message(
                "Workflow Manager - Plot Import",
                "{0} preview errors were reported. "
                "Please correct the errors and import.".format(error)
            )
            return True

    def _remove_field_book(self, path):
        # Deletes the previously uploaded field book from the repository
        self.notif_bar.clear()
        status = self._field_bk_mgr.upload_status(path)
        if status == -1:
            return

        elif status == FieldBookManager.ERROR:
            msg = 'The field book was not uploaded successfully hence it will ' \
                  'not be removed from the document repository'
            self.notif_bar.insertWarningNotification(msg)

        elif status == FieldBookManager.NOT_UPLOADED:
            msg = 'There is an ongoing upload operation, please try again ' \
                  'in a few moments.'
            self.notif_bar.insertWarningNotification(msg)

        elif status == FieldBookManager.SUCCESS:
            self._field_bk_mgr.remove_field_book(path)

    def _remove_file(self, user_action=True):
        """
        Removes plot import file and its settings from table view.
        If user_action is True and the document is a field book, then the
        document will be deleted from the repository.
        """
        index = self._current_index(self._file_table_view)
        if index is None:
            return

        row = index.row()
        fpath = self.model.results[row].get("fpath")
        if self._plot_preview:
            self._plot_preview.remove_layer_by_id(fpath)
        self._reset_preview(fpath)
        self._set_preview_groupbox_title()
        self.model.removeRows(row)
        self._remove_dirty(fpath)
        self._plot_file.remove_filepath(fpath)
        self._enable_crs_button()

        # If field book and user_action then delete field book
        if self._plot_file.is_pdf(fpath) and user_action:
            self._remove_field_book(fpath)

        if not self.model.results:
            self.model.reset()
            self._disable_widgets(self._toolbar_buttons)
            self._set_crs_button.setEnabled(False)

    def _remove_dirty(self, fpath):
        """
        Removes file name from dirty class variable
        :param fpath: Plot import file absolute path
        :type fpath: String
        """
        if self._plot_preview.is_dirty(fpath):
            self._plot_preview.remove_dirty(fpath)

    @staticmethod
    def _load(model, data_source):
        """
        Loads model data
        :param model: Table view model
        :type model: QAbstractTableModel
        :param data_source: Data source object
        :rtype data_source: Object
        """
        model.layoutAboutToBeChanged.emit()
        model.load(data_source)
        model.layoutChanged.emit()

    def _show_critical_message(self, title, msg):
        """
        Message box to communicate critical message
        :param title: Title of the message box
        :type title: String
        :param msg: Message to be communicated
        :type msg: String
        """
        QMessageBox.critical(
            self,
            self.tr(title),
            self.tr(msg)
        )

    def _set_preview_groupbox_title(self, title=None):
        """
        Sets the preview groupbox title
        :param title: Groupbox title
        :type title: String
        """
        default = "File content"
        if title:
            if len(title) > 20:
                title = "{0}{1}".format(title[:20], "...")
            title = "{0}: {1}".format(default, title)
        else:
            title = default
        self._preview_groupbox.setTitle(title)

    def _show_question_message(self, title, msg):
        """
        Message box to communicate a question
        :param title: Title of the message box
        :type title: String
        :param msg: Message to be communicated
        :type msg: String
        :return: True or False
        :rtype: Boolean
        """
        if QMessageBox.question(
            self, self.tr(title), self.tr(msg),
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.No:
            return False
        return True

    @property
    def _toolbar_buttons(self):
        """
        Returns toolbar buttons
        :return buttons: Toolbar buttons
        :return buttons: List
        """
        buttons = [
            self._remove_button,
            self._preview_button,
            self._import_button
        ]
        return buttons

    @staticmethod
    def _enable_widgets(widgets):
        """
        Enables list of widgets
        :param widgets: List of QWidget
        :rtype widgets: List
        """
        for widget in widgets:
            if widget:
                widget.setEnabled(True)

    @staticmethod
    def _disable_widgets(widgets):
        """
        Disables list of widgets
        :param widgets: List of QWidget
        :rtype widgets: List
        """
        for widget in widgets:
            if widget:
                widget.setEnabled(False)

    def _set_crs(self):
        """
        Sets coordinate reference system (CRS) to
        property to a plot import file
        """
        index = self._current_index(self._file_table_view)
        if index is None:
            return
        row = index.row()
        index = self.model.create_index(row, CRS_ID)
        value = self._crs_authority_id()
        items = self.model.results[row].get("items")
        items[CRS_ID] = None
        self.model.setData(index, value)

    def _enable_disable_preview_import_buttons(self):
        # Enable or disable the preview and import buttons if the field book
        # manager is active or inactive respectively.
        fpath = self._selected_file()
        if not fpath:
            return
        if self._plot_file.is_pdf(fpath):
            if not self._field_bk_mgr.is_active:
                status = False
            else:
                status = True
        else:
            status = True

        self._preview_button.setEnabled(status)
        self._import_button.setEnabled(status)

    def _enable_crs_button(self):
        """
        Enables/disables Set CRS button
        """
        fpath = self._selected_file()
        if not fpath:
            return
        if self._plot_file.is_pdf(fpath):
            self._set_crs_button.setEnabled(False)
        else:
            self._set_crs_button.setEnabled(True)

    def _selected_file(self):
        """
        Returns selected file
        :return fpath: Selected file
        :return fpath: String
        """
        index = self._current_index(self._file_table_view)
        if index is None:
            return
        fpath = self.model.results[index.row()].get("fpath")
        return fpath

    def _select_field_book(self):
        # Loops through the files in the view and selects the first field
        # book it encounters. Returns True if field book found and selected.
        file_count = self.model.rowCount()
        selection_model = self._file_table_view.selectionModel()

        if file_count == 0:
            return False

        status = False
        for r in range(file_count):
            fpath = self.model.results[r].get("fpath")
            if self._plot_file.is_pdf(fpath):
                sel_index = self.model.index(r, 0)
                selection_model.select(
                    sel_index,
                    QItemSelectionModel.ClearAndSelect
                )
                status = True
                break

        return status

    def _contains_field_book(self):
        # Checks if the file view contains a field book.
        file_count = self.model.rowCount()
        if file_count == 0:
            return False

        status = False
        for r in range(file_count):
            fpath = self.model.results[r].get("fpath")
            if self._plot_file.is_pdf(fpath):
                status = True
                break

        return status

    @staticmethod
    def _crs_authority_id():
        """
        Returns selected coordinate
        reference system (CRS) authority ID
        :return auth_id: CRS authority ID
        :return auth_id: String
        """
        proj_selector = QgsGenericProjectionSelector()
        proj_selector.setOgcWmsCrsFilter(NAM_CRS)
        proj_selector.exec_()
        auth_id = proj_selector.selectedAuthId()
        return auth_id

    @staticmethod
    def _current_index(table_view):
        """
        Returns index of the current selected rowe
        :return table_view: Table view object
        :type table_view: QTableView
        :return: Current row index
        :rtype: Integer
        """
        index = table_view.currentIndex()
        if not index.isValid():
            return
        return index

    def _reset_preview(self, fpath):
        """
        Resets preview QTableView
        :param fpath: Plot import file absolute path
        :type fpath: String
        """
        if fpath in self._previewed:
            self._preview_model.reset()
            del self._previewed[fpath]

    def _on_preview_select(self, selected):
        """
        Selects a layer feature on table view row
        :param selected: Currently selected items
        :type selected: QItemSelection
        """
        if self._plot_preview.layer:
            index = selected.indexes()[0]
            self._plot_preview.clear_feature(self._plot_preview.layer)
            self._plot_preview.select_feature(index.row() + 1)
