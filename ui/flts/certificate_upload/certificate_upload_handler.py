"""
/***************************************************************************
Name                 : Certificate upload handler
Description          : Class that manages the uploading of the certificate to
                       the CMIS repository.
Date                 : 30/May/2020
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
from datetime import datetime
from PyQt4.QtCore import (
    pyqtSignal,
    QObject
)

from stdm.settings import current_profile
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

from stdm.ui.flts.certificate_upload import certificate_model_factory
from stdm.ui.flts.certificate_upload.certificate_info import (
    CertificateInfo
)


class CertificateUploadHandler(QObject):
    """
    Container that manages uploading processes of the certificate.
    """
    CERT_ENTITY_NAME = 'Certificate'
    CERT_DOC_TYPE = 'Archive'

    # Certificate Upload state
    NOT_UPLOADED, SUCCESS, ERROR = range(3)

    # Signals
    uploaded = pyqtSignal(CertificateInfo)
    upload_completed = pyqtSignal()
    removed = pyqtSignal(CertificateInfo)
    persisted = pyqtSignal()

    def __init__(self, cert_info=None, cmis_mngr=None, parent=None):
        super(CertificateUploadHandler, self).__init__(parent)
        self._cert_info_items = cert_info
        if not self._cert_info_items:
            self._cert_info_items = []

        self._cmis_mngr = cmis_mngr
        if not self._cmis_mngr:
            self._cmis_mngr = CmisManager()

        self._cert_model = None
        self._cert_doc_model = None

        self._cert_doc_mapper = CmisEntityDocumentMapper(
            cmis_manager=self._cmis_mngr,
            doc_model_cls=self._cert_doc_model,
            entity_name=self.CERT_ENTITY_NAME
        )

        # Error messages as to why the upload handler is not responsive
        self._error_msg = []
        curr_profile = current_profile()
        if not curr_profile:
            self._error_msgs.append(
                'Current profile is None'
            )
            return

        cert_entity = curr_profile.entity(
            self.CERT_ENTITY_NAME
        )
        if not cert_entity:
            self._error_msgs.append(
                'Certificate entity not found'
            )
            return

        # Get the name of the lookup table containing the document types
        # associated with the certificate entity
        cert_doc_type_tbl = cert_entity.supporting_doc.document_type_entity\
            .name

        # Get the primary key, name and code of the certificate document type
        # in the lookup.
        cert_doc_types = export_data(cert_doc_type_tbl)

        # Map the required document types to the Cmis document mapper.
        for doc in cert_doc_types:
            doc_type = doc.value
            code = doc.code
            doc_type_id = doc.id
            self._cert_doc_mapper.add_document_type(
                doc_type,
                code,
                doc_type_id
            )

        # Stores the upload status of each document with the source file path
        # as key
        self._cert_upload_status = {}

        # Map the file path to cmislib document for successfully uploaded docs
        self._uploaded_certs = {}

        # Error messages in document upload. Key: source file path, Value:
        # Error message
        self._certificate_upload_error = {}

        # Flag for checking if there is an active certificate upload/removal
        self._has_active_operation = False

    @property
    def errors(self):
        """
        :return: Returns a list of errors that are causing the handler to be
        inactive.
        :rtype: list
        """
        return self._err_msg

    @property
    def has_active_operation(self):
        """
        :return: Returns True of there is an onging upload operation or removal
        of the certificate.
        :rtype: bool
        """
        return self._has_active_operation

    @property
    def is_active(self):
        """
        :return: Returns True if the Certificate upload handler is able to
        upload a certificate to the repository
        :rtype: bool
        """
        return False if len(self._error_msg) > 0 else True

    @property
    def cert_info_items(self):
        """
        :return: Returns a list of certificate items.
        :rtype: list
        """
        return self._cert_info_items

    @cert_info_items.setter
    def cert_info_items(self, cert_info):
        """
        Sets the collection of the CertificateInfo objects to be uploaded.
        :param cert_info: List of certificate items.
        :type cert_info: list
        """
        self._cert_info_items = cert_info

    def upload(self, cert_info):
        """
        Upload the certificate info.
        :param cert_info: Certificate information objects.
        :type cert_info: object
        """
        # Upload certificates and supporting docs
        self._upload_cert_info(
            cert_info.filename,
            self._cert_doc_model
        )

    def _upload_cert_info(self, path, cert_doc_type):
        """
        Upload the certificate in path to the CMIS document repository temp
        folder.
        :param path: Absolute path to the certificate.
        :type path: str
        :param cert_doc_type: Name of the document type to be uploaded.
        The default option is 'Archive'.
        :type cert_doc_type: str
        """
        upload_crt = CmisDocumentUploadThread(
            path,
            self._cert_doc_mapper,
            cert_doc_type,
            self
        )

        # Connect signals
        upload_crt.succeeded.connect(
            self._on_upload_succeeded
        )
        upload_crt.finished.connect(
            self._on_upload_finished
        )
        upload_crt.started.connect(
            self._on_upload_remove_started
        )
        upload_crt.connect(
            self._on_upload_remove_finished
        )

        # Set the status of the document
        self._cert_upload_status[
            path
        ] = CertificateUploadHandler.NOT_UPLOADED

        upload_crt.start()

    def _update_cert_upload_status(self, path, status):
        """
        Update the status of the certificate that is being uploaded.
        :param path:
        :param status:
        :return:
        """
        if path in self._cert_upload_status:
            self._update_cert_upload_status[path] = status

    def _on_upload_error(self, error_info):
        """
        Slot raised when there is an error when uploading a certificate.
        :param error_info: Tuple containing the cert doc type and
        corresponding error message.
        :type error_info: tuple(cert_doc_type, error_msg)
        """
        sender = self.sender()
        if sender:
            file_path = sender.file_path
            error_msg = error_info[1]
            self._cert_upload_status[file_path] = \
                CertificateUploadHandler.ERROR
            self._certificate_upload_error[file_path] = error_msg

            # Emit signal
            self.uploaded.emit(error_info)

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
        return self._certificate_upload_error.get(file_path, '')

    def persist_certificates(self):
        """
        Moves the certificates from the Temp folder to the permanent
        certificate directory in the CMIS server.
        """
        if not self._cert_model:
            self._cert_model = certificate_model_factory[0]
        cert_obj = self._cert_model()
        # Create certificate object models and return as a list
        cert_objs = self._cert_doc_mapper.persist_documents(
            cert_obj.certificate_number
        )
        cert_obj.documents = cert_objs
        cert_obj.save()
        self.reset()

        self.persisted.emit()

    def _save_cert_metadata(self):
        """
        Save the certificate metadata in the database.
        """
        if not self._cert_model:
            self._cert_model = certificate_model_factory[0]
        cert_obj = self._cert_model()
        # Set the archive date
        cert_obj.archive_date = datetime.now()
        # Set the uploaded status
        cert_obj.is_uploaded = 't'
        # Update certificate column values
        cert_obj.update()

    def reset(self):
        """
        Clear any certificates used in any previous sessions.
        """
        self._cert_upload_status = {}
        self._uploaded_certs = {}
        self._certificate_upload_error = {}

    def cert_from_file_path(self, path):
        """
        Gets the cmislib document object from the file path. This only
        applies to those files that have been successfully uploaded.
        :param path: File path of the source document.
        :type path: str
        :return: Returns the cmislib document object from the given file if
        it has been successfully uploaded, else None.
        :rtype: cmislib.domain.Document
        """
        return self._uploaded_certs.get(path, None)

    def remove_certificate(self, path):
        """
        Remove the certificate with the given path from the document
        repository.
        :param path:  File path for uniquely identifying the certificate to
        be removed.
        :type path: str
        """
        self._remove_certificate_supporting_document(path, self.CERT_DOC_TYPE)

    def _remove_certificate_supporting_document(self, path, cert_doc_type):
        """
        Removes the certificate indexed by the given file path and of the 
        given type. Certificate must have been uploaded successfully before
        initiating the command to remove it else the operation will not be
        executed.
        :param path: File path for uniquely identifying the certificate to be
        removed.
        :type path: str
        :param cert_doc_type: Name of the certificate document type to be
        deleted.
        :type cert_doc_type: str
        """
        # Check if the certificate was previously uploaded.
        crt = self.cert_from_file_path(path)
        if not crt:
            # Remove reference if there was an error while attempting to
            # upload.
            if path in self._certificate_upload_error:
                del self._certificate_upload_error[path]

            return

        uuid = self._uuid_from_cert(crt)
        delete_crt = CmisDocumentDeleteThread(
            self._cert_doc_mapper,
            cert_doc_type,
            uuid,
            self
        )

        # connect signals
        delete_crt.succeeded.connect(
            self._on_remove_certificate_succeeded
        )
        delete_crt.error.connect(
            self._on_remove_certificate_error
        )
        delete_crt.started.connect(
            self._on_upload_remove_started
        )
        delete_crt.finished.connect(
            self._on_upload_remove_finished
        )

        delete_crt.start()

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
        return self._cert_upload_status.get(file_path, -1)

    def _on_upload_succeeded(self, status_info):
        """
        Slot raised when a certificate has been uploaded successfully.
        """
        sender = self.sender()
        if sender:
            file_path = sender.file_path
            doc_obj = status_info[1]
            self._cert_upload_status[file_path] = \
                CertificateUploadHandler.SUCCESS
            self._uploaded_certs[file_path] = doc_obj
        self.uploaded.emit()

    def _on_upload_finished(self):
        """
        Slot raised when uploading process has completed.
        """
        self.upload_completed.emit()

    def _on_upload_remove_started(self):
        """
        Slot raised when a thread of uploading or removing a certificate has
        started hence, setting an active operation status.
        """
        self._has_active_operation = True

    def _on_upload_remove_finished(self):
        """
        Slot raised when a thread of uploading or removing a certificate has
        finished hence, setting an active operation status.
        """
        self._has_active_operation = False

    def _on_remove_certificate_succeeded(self):
        """
         Slot raised when a certificate has been successfully removed.
        """
        sender = self.sender()
        if sender:
            path = sender.file_path
            if path in self._uploaded_certs:
                # Remove all references
                del self._uploaded_docs[path]
                del self._cert_upload_status[path]

                # Emit signal with status info
                self.removed.emit((path, True, ''))

    def _on_remove_certificate_error(self, error_info):
        """
        Slot raised when an error occurs during the removal of a certificate.
        :param error_info: Contains the error info items
        :type error_info: list
        """
        sender = self.sender()
        if sender:
            err_msg = error_info[1]
            path = sender.file_path
            if path in self._uploaded_certs:
                # Remove all references
                del self._uploaded_certs[path]
                del self._cert_upload_status[path]

                # Emit signal with status info
                self.removed.emit((path, False, err_msg))
