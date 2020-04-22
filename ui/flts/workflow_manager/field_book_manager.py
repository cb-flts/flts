"""
Name                 : FieldBookManager
Description          : Provides an interface for managing the upload of
                       field book documents.
Date                 : 20/April/2020
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
from PyQt4. QtCore import (
    pyqtSignal,
    QObject
)

from stdm.settings import current_profile
from stdm.data.configuration import entity_model
from stdm.data.pg_utils import export_data
from stdm.network.cmis_manager import (
    CmisDocumentMapperException,
    CmisManager,
    CmisEntityDocumentMapper
)
from stdm.ui.customcontrols.documents_table_widget import (
    CmisDocumentUploadThread,
    CmisDocumentDeleteThread
)


class FieldBookManager(QObject):
    """
    Manages the upload of field book documents used in the plot import
    module.
    """
    FIELD_BOOK_DOC = 'Field Book'

    # Upload state
    NOT_UPLOADED, SUCCESS, ERROR = range(3)

    # Signals
    uploaded = pyqtSignal(tuple) # (path, successful(bool))
    removed = pyqtSignal(tuple) # (path, successful(bool), err_msg)

    def __init__(self, doc_model_cls, parent=None):
        super(FieldBookManager, self).__init__(parent)
        self._doc_model_cls = doc_model_cls

        # Stores the upload status of each document with the source file path
        # as the key
        self._document_upload_status = {}

        # Error messages in document upload. Key: source file path, Value:
        # Error message
        self._document_upload_error = {}

        # Map the file path to cmislib document for successfully uploaded docs
        self._uploaded_docs = {}

        # Flag for checking if there is an active document upload/removal
        self._has_active_operation = False

        self._plt_entity_name = 'Plot'

        # Messages as to why the manager is not active
        self._error_msgs = []
        curr_profile = current_profile()
        if not curr_profile:
            self._error_msgs.append(
                'Current profile is None'
            )
            return

        plot_entity = curr_profile.entity(
            self._plt_entity_name
        )
        if not plot_entity:
            self._error_msgs.append(
                'Plot entity not found'
            )
            return

        cmis_mgr = CmisManager()
        conn_status = cmis_mgr.connect()
        if not conn_status:
            msg = 'Could not connect to CMIS Server'
            self._error_msgs.append(msg)
            return

        self._field_bk_doc_mapper = CmisEntityDocumentMapper(
            cmis_manager=cmis_mgr,
            doc_model_cls=self._doc_model_cls,
            entity_name=self._plt_entity_name
        )

        # Get the name of the lookup table containing the document types associated with
        # the plot entity
        field_bk_table = plot_entity.supporting_doc.document_type_entity.name

        # Get the primary key, name and code of the plot document type in the lookup
        cert_doc_types = export_data(field_bk_table)

        # Map the required document types to the Cmis document mapper
        for doc in cert_doc_types:
            doc_type = doc.value
            code = doc.code
            doc_type_id = doc.id
            self._field_bk_doc_mapper.add_document_type(
                doc_type,
                code,
                doc_type_id
            )

    @property
    def errors(self):
        """
        :return: Returns a list of errors that are causing the manager to be
        inactive.
        :rtype: list
        """
        return self._error_msgs

    @property
    def has_active_operation(self):
        """
        :return: Returns True if there is an ongoing upload or removal of
        document.
        :rtype: bool
        """
        return self._has_active_operation

    @property
    def is_active(self):
        """
        :return: Returns True if the manager is active and is able to
        upload a field book to the repository, else False.
        Use func: errors to get a list of error messages.
        """
        return False if len(self._error_msgs) > 0 else True

    def reset(self):
        # Clears any documents used in any previous sessions.
        self._document_upload_status = {}
        self._uploaded_docs = {}
        self._document_upload_error= {}

    def upload_plot_supporting_document(self, path, document_type):
        """
        Uploads a supporting document to the CMIS server's temp folder.
        :param path: Absolute file path to the field book.
        :type path: str
        :param document_type: Name of the document type to be uploaded.
        Default option is 'Field Book' however this function will support
        additional types in future if the need arises.
        :type document_type: str
        """
        upload_thread = CmisDocumentUploadThread(
            path,
            self._field_bk_doc_mapper,
            document_type,
            self
        )
        # Connect signals
        upload_thread.error.connect(
            self._on_upload_error
        )
        upload_thread.succeeded.connect(
            self._on_successful_upload
        )
        upload_thread.started.connect(
            self._on_upload_remove_started
        )
        upload_thread.finished.connect(
            self._on_upload_remove_finished
        )

        # Set the status of the document
        self._document_upload_status[
            path
        ] = FieldBookManager.NOT_UPLOADED

        upload_thread.start()

    def upload_field_book(self, path):
        """
        Uploads a field book to the CMIS server's temp folder.
        :param path: Path to the field book.
        :type path: str
        :return: Returns the cmislib.domain.Document object if the field book
        was successfully uploaded, else None if the file does not exist in
        the given path or if an error occurred during the upload process.
        """
        self.upload_plot_supporting_document(
            path,
            self.FIELD_BOOK_DOC
        )

    def _update_document_upload_status(self, path, status):
        # Update the status of the document that is being/has been uploaded.
        if path in self._document_upload_status:
            self._document_upload_status[path] = status

    def _on_upload_remove_started(self):
        # Slot raised when a thread for uploading or removing a document
        # has started. It sets an active operation status.
        self._has_active_operation = True

    def _on_upload_remove_finished(self):
        # Slot raised when a thread for uploading or removing a document
        # has finished. It sets the active operation status to False.
        self._has_active_operation = False

    def _on_upload_error(self, error_info):
        """
        Slot raised when there is an error when uploading a document.
        :param error_info: Tuple containing the document type and
        corresponding error message.
        :type error_info: tuple(doc_type, error_msg)
        """
        sender = self.sender()
        if sender:
            file_path = sender.file_path
            err_msg = error_info[1]
            self._document_upload_status[file_path] = FieldBookManager.ERROR
            self._document_upload_error[file_path] = err_msg

            # Emit signal
            self.uploaded.emit((file_path, False))

    def upload_error_message(self, file_path):
        """
        Gets the error message that occurred during the upload of the given
        file.
        :param file_path: Path to the file that was being uploaded.
        :type file_path: str
        :return: Returns the error message associated with the upload of the
        given file, else return an empty string if the file was not logged as
        having an error.
        :rtype: str
        """
        return self._document_upload_error.get(file_path, '')

    def upload_status(self, file_path):
        """
        Gets the upload status of the document with the given path.
        :param file_path: Source document path.
        :type file_path: str
        :return: Returns the status indicating whether the document is
        NOT_UPLOADED, SUCCESSFUL or ERROR occurred, else returns -1 if
        the given file path is not found.
        ":rtype: int
        """
        return self._document_upload_status.get(file_path, -1)

    def _on_successful_upload(self, res_info):
        """
        Slot raised by the upload thread when a document has been
        successfully uploaded to the repository.
        :param res_info: Tuple containing the document type and cmislib
        document object.
        :type res_info: tuple(doc_type, document object)
        """
        sender = self.sender()
        if sender:
            file_path = sender.file_path
            doc_obj = res_info[1]
            self._document_upload_status[file_path] = FieldBookManager.SUCCESS
            self._uploaded_docs[file_path] = doc_obj

            # Emit signal
            self.uploaded.emit((file_path, True))

    def _uuid_from_doc(self, doc):
        # Returns the UUID for the given document
        cmis_props = doc.getProperties()
        return cmis_props['cmis:versionSeriesId']

    def document_from_file_path(self, path):
        """
        Gets the cmislib document object from the file path. This only
        applies to those files that have been successfully uploaded.
        :param path: File path of the source document.
        :type path: str
        :return: Returns the cmislib document object from the given file if
        it has been successfully uploaded, else None.
        """
        return self._uploaded_docs.get(path, None)

    def file_path_from_uuid(self, uuid):
        """
        Gets the file path for the document with the given UUID.
        :param uuid: UUID of the document.
        :type uuid: str
        :return: Returns the file path for the document with the given UUID
        or an empty string if the UUID was not found.
        :rtype: str
        """
        return next(
            (path for path, doc in self._uploaded_docs.iteritems()
             if self._uuid_from_doc(doc) == uuid),
            None
        )

    def document_type_count(self, document_type):
        """
        Gets the number of documents already uploaded for thr given document
        type.
        :param document_type: Document type
        :type document_type: str
        :return: Returns the number of documents already uploaded for the
        given type or -1 if the document type has not been mapped.
        :rtype: int
        """
        docs = self._field_bk_doc_mapper.uploaded_documents_by_type(
            document_type
        )
        if not docs:
            return -1
        else:
            return len(docs)

    def field_book_count(self):
        """
        :return: Returns the number of uploaded field book documents.
        :rtype: int
        """
        return self.document_type_count(
            self.FIELD_BOOK_DOC
        )

    def remove_plot_supporting_document(self, path, document_type):
        """
        Removes document indexed by the given file path and of the given type.
        The document must have been successfully uploaded before initiating
        the command to remove it otherwise the operation will not be
        executed.
        :param path: File path for uniquely identifying the document to be
        removed.
        :type path: str
        :param document_type: Type of the document to be removed, default is
        'Field Book'.
        :type document_type: str
        """
        # Check if the document was previously uploaded.
        doc = self.document_from_file_path(path)
        if not doc:
            # Remove reference if there was an error while attempting to
            # upload.
            if path in self._document_upload_error:
                del self._document_upload_error[path]

            return

        uuid = self._uuid_from_doc(doc)
        delete_thread = CmisDocumentDeleteThread(
            self._field_bk_doc_mapper,
            document_type,
            uuid,
            self
        )

        # connect signals
        delete_thread.succeeded.connect(
            self._on_remove_document_succeeded
        )
        delete_thread.error.connect(
            self._on_remove_document_error
        )
        delete_thread.started.connect(
            self._on_upload_remove_started
        )
        delete_thread.finished.connect(
            self._on_upload_remove_finished
        )

        delete_thread.start()

    def persist_documents(self, scheme_number):
        """
        Moves the plot supporting documents to the permanent plot directory
        in the CMIS server.
        :param scheme_number: Number of the scheme that will also be used to
        name the documents.
        :type scheme_number: str
        :return: Returns a list of document SQLAlchemy objects for attaching
        to the main entity object for saving in the database.
        :rtype: list
        """
        return self._field_bk_doc_mapper.persist_documents(scheme_number)

    def remove_field_book(self, path):
        """
        Removes the field book with the given path from the document
        repository.
        :param path: File path for uniquely identifying the field book to be
        removed.
        :type path: str
        """
        self.remove_plot_supporting_document(path, self.FIELD_BOOK_DOC)

    def _on_remove_document_error(self, err_info):
        # Slot raised when an error occurred while attempting to remove the
        # document.
        sender = self.sender()
        if sender:
            uuid = sender.document_uuid
            err_msg = err_info[1]
            path = self.file_path_from_uuid(uuid)
            if path in self._uploaded_docs:
                # Remove all references
                del self._uploaded_docs[path]
                del self._document_upload_status[path]

                # Emit signal with status info
                self.removed.emit((path, False, err_msg))

    def _on_remove_document_succeeded(self, status_info):
        # Slot raised when a document has been successfully removed.
        sender = self.sender()
        if sender:
            uuid = sender.document_uuid
            path = self.file_path_from_uuid(uuid)
            if path in self._uploaded_docs:
                # Remove all references
                del self._uploaded_docs[path]
                del self._document_upload_status[path]

                # Emit signal with status info
                self.removed.emit((path, True, ''))