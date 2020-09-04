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

    # Signals
    uploaded = pyqtSignal(unicode)
    upload_completed = pyqtSignal()
    removed = pyqtSignal(tuple)
    persisted = pyqtSignal()

    def __init__(self, cert_info=None, cmis_mngr=None, parent=None):
        super(CertificateUploadHandler, self).__init__(parent)
        self._cert_info_items = cert_info
        if not self._cert_info_items:
            self._cert_info_items = []

        # CMIS Manager
        self._cmis_mngr = cmis_mngr
        if not self._cmis_mngr:
            self._cmis_mngr = CmisManager()

        # Initialize Certificate models variables
        self._cert_model = None
        self._cert_doc_model = None

        # Assign model factory
        cert_models = certificate_model_factory()
        if not cert_models:
            return

        # Assign models values
        self._cert_model = cert_models[0]
        self._cert_doc_model = cert_models[1]

        self._cert_doc_mapper = CmisEntityDocumentMapper(
            cmis_manager=self._cmis_mngr,
            doc_model_cls=self._cert_doc_model
        )

        # Error messages as to why the upload handler is not responsive
        self._error_msg = []

        # Get current profile
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
        cert_doc_type_tbl = cert_entity.supporting_doc.document_type_entity.name

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

        # Stores the upload status of each document with the certificate
        # number as key
        self._cert_upload_status = {}

        # Map the certificate number to cmislib document for successfully uploaded docs
        self._uploaded_certs = {}

        # Error messages in document upload. Key: certificate number, Value:
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
        :return: Returns True of there is an ongoing upload operation or
        removal of the certificate.
        :rtype: bool
        """
        return self._has_active_operation

    @property
    def is_active(self):
        """
        :return: Returns True if the Certificate upload handler is able to
        upload a certificate to the repository.
        :rtype: bool
        """
        return False if len(self._error_msg) > 0 else True

    @property
    def cert_info_items(self):
        """
        :return: Returns values in the cert info dictionary.
        :rtype: list
        """
        return self._cert_info_items

    @cert_info_items.setter
    def cert_info_items(self, cert_info):
        """
        Sets the collection of the CertificateInfo objects to be uploaded.
        :param cert_info: Certificate number.
        :type cert_info: list
        """
        self._cert_info_items = cert_info

    def upload_certificate(self, cert_path):
        """
        Upload the certificate to the temporary directory based on the
        information on the certificate info object.
        :param cert_path: Certificate path.
        :type cert_path: str
        """
        # Upload certificates and supporting docs
        self._upload_cert_info(
            cert_path,
            self.CERT_DOC_TYPE
        )

    def _upload_cert_info(self, file_path, cert_doc_type):
        """
        Upload the certificate with the matching certificate number to the
        CMIS document repository temp folder.
        :param file_path: Certificate file path.
        :type file_path: str
        :param cert_doc_type: Name of the document type to be uploaded.
        The default option is 'Archive'.
        :type cert_doc_type: str
        """
        upload_crt = CmisDocumentUploadThread(
            file_path,
            self._cert_doc_mapper,
            cert_doc_type,
            self
        )

        # Connect signals
        upload_crt.error.connect(
            self._on_upload_error
        )
        upload_crt.succeeded.connect(
            self._on_upload_succeeded
        )
        upload_crt.started.connect(
            self._on_upload_remove_started
        )
        upload_crt.finished.connect(
            self._on_upload_remove_finished
        )
        upload_crt.finished.connect(
            self._on_upload_finished
        )

        # Set the status of the document
        self._cert_upload_status[
            file_path
        ] = CertificateInfo.NOT_UPLOADED

        upload_crt.start()

    def _on_upload_succeeded(self, status_info):
        """
        Slot raised by the upload thread when a document has been
        successfully uploaded to the repository.
        :param status_info: Tuple containing the document type and cmislib
        document object.
        :type status_info: tuple(doc_type, document object)
        """
        sender = self.sender()
        if sender:
            file_path = sender.file_path
            doc_obj = status_info[1]
            self._cert_upload_status[file_path] = CertificateInfo.SUCCESS
            self._uploaded_certs[file_path] = doc_obj
            # Emit signal
            self.uploaded.emit(file_path)

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
            doc_obj = error_info[1]
            self._cert_upload_status[file_path] = CertificateInfo.ERROR
            self._uploaded_certs[file_path] = doc_obj
            # Emit signal
            self.uploaded.emit(file_path)

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

    def _update_cert_upload_status(self, cert_number, status):
        """
        Update the status of the certificate that is being uploaded.
        :param cert_number: Certificate number.
        :param status: Upload status of the certificate info object.
        """
        if cert_number in self._cert_upload_status:
            self._update_cert_upload_status[cert_number] = status

    def upload_error_message(self, certificate_number):
        """
        Gets the error message that occurred during the upload of the given
        file.
        :param certificate_number: Certificate number of the certificate that
        was being uploaded.
        :type certificate_number: str
        :return: Returns the error message associated with the upload of the
        given cert, else return an empty string if the file was not logged as
        having an error.
        :rtype: str
        """
        return self._certificate_upload_error.get(certificate_number, '')

    def persist_certificates(self, cert_number):
        """
        Moves the certificates from the Temp folder to the permanent
        certificate directory in the CMIS server. The document object
        models will also be created and returned as a list.
        :param cert_number: certificate number
        :type cert_number: str
        """
        self._cert_doc_mapper.entity_name = self.CERT_ENTITY_NAME

        cert_objects = self._cert_doc_mapper.persist_documents(
            cert_number
        )
        cert_doc_obj = self._cert_doc_model()
        cert_doc_obj.documents = cert_objects
        cert_doc_obj.save()
        cert_number = cert_number.replace('.', '/')
        self._update_cert_metadata(cert_number)

        # Emit signal
        self.persisted.emit()

        return cert_doc_obj.id

    def _update_cert_metadata(self, cert_number):
        """
        Update the certificate metadata in the database.
        :param cert_number: Certificate number of the certificate whose
        metadata requires updating.
        :type cert_number: str
        """
        # Certificate object
        cert_obj = self._cert_model()
        # Query fetching row based on certificate number
        res = cert_obj.queryObject().filter().all()
        # Updating column values for each fetched certificate.
        for obj in res:
            if obj.certificate_number == str(cert_number):
                obj.archive_date = datetime.now()
                obj.is_uploaded = 'true'
                obj.update()

        self.reset()

    def reset(self):
        """
        Clear any certificates used in any previous sessions.
        """
        self._cert_info_items = []
        self._cert_upload_status = {}
        self._uploaded_certs = {}
        self._certificate_upload_error = {}

    def _uuid_from_doc(self, doc):
        # Returns the UUID for the given document
        cmis_props = doc.getProperties()
        return cmis_props['cmis:versionSeriesId']

    def _doc_name_from_doc(self, doc):
        # Returns the name of the given document
        cmis_props = doc.getProperties()
        return cmis_props['cmis:name']

    def doc_from_cert_number(self, cert_number):
        """
        Gets the cmislib document object from the file path. This only
        applies to those files that have been successfully uploaded.
        :param cert_number: Certificate number of the certificate document.
        :type cert_number: str
        :return: Returns the cmislib document object from the given
        certificate if it has been successfully uploaded, else None.
        :rtype: cmislib.domain.Document
        """
        return self._uploaded_certs.get(cert_number, None)

    def certificate_uuid(self, file_path):
        """
        Gets the document identifier from the cmislib document indexed by the
        given source file path. This only applies for those documents that
        had been successfully uploaded.
        :param file_path: File path of the source document.
        :type file_path: str
        :return: Returns the document identifier from the cmislib document
        indexed by the given source file path, else an empty string if the
        document was not successfully uploaded.
        :rtype: str
        """
        if file_path in self._uploaded_certs:
            doc = self.doc_from_cert_number(file_path)
            return self._uuid_from_doc(doc)

        return ''

    def certificate_name(self, file_path):
        """
        Gets the document name from the cmislib document indexed by the
        given source file path. This only applies for those documents that
        had been successfully uploaded.
        :param file_path: File path of the source document.
        :type file_path: str
        :return: Returns the document name from the cmislib document
        indexed by the given source file path, else an empty string if the
        document was not successfully uploaded.
        :rtype: str
        """
        if file_path in self._uploaded_certs:
            doc = self.doc_from_cert_number(file_path)
            return self._doc_name_from_doc(doc)

        return ''

    def cert_path_from_uuid(self, uuid):
        """
        Gets the file path for the document with the given UUID.
        :param uuid: UUID of the document.
        :type uuid: str
        :return: Returns the file path for the document with the given UUID
        or an empty string if the UUID was not found.
        :rtype: str
        """
        return next(
            (path for path, doc in self._uploaded_certs.iteritems()
             if self._uuid_from_doc(doc) == uuid),
            None
        )

    def document_type_count(self, document_type):
        """
        Gets the number of documents already uploaded for the given document
        type.
        :param document_type: Document type
        :type document_type: str
        :return: Returns the number of documents already uploaded for the
        given type or -1 if the document type has not been mapped.
        :rtype: int
        """
        docs = self._cert_doc_mapper.uploaded_documents_by_type(
            document_type
        )
        if not docs:
            return -1
        else:
            return len(docs)

    def remove_certificate(self, cert_path):
        """
        Remove the certificate with the given path from the document
        repository.
        :param cert_path: Certificate path that uniquely identifies the
        certificate to be removed.
        :type cert_path: str
        """
        self._remove_certificate_supporting_document(cert_path, self.CERT_DOC_TYPE)

    def _remove_certificate_supporting_document(self, cert_path, cert_doc_type):
        """
        Removes the certificate indexed by the given certificate number and of
        the given type. Certificate must have been uploaded successfully
        before initiating the command to remove it else the operation will not
        be executed.
        :param cert_path: Certificate path that uniquely identifies the
        certificate to be removed.
        :type cert_path: str
        :param cert_doc_type: Name of the certificate document type to be
        deleted.
        :type cert_doc_type: str
        """
        # Check if the certificate was previously uploaded.
        crt = self.doc_from_cert_number(cert_path)
        if not crt:
            # Remove reference if there was an error while attempting to
            # upload.
            if cert_path in self._certificate_upload_error:
                del self._certificate_upload_error[cert_path]

            return

        uuid = self._uuid_from_doc(crt)

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

    def _on_remove_certificate_succeeded(self, status_info):
        """
        Slot raised when a certificate has been successfully removed.
        :param status_info
        """
        sender = self.sender()
        if sender:
            uuid = sender.document_uuid
            path = self.cert_path_from_uuid(uuid)
            if path in self._uploaded_certs:
                # Remove all references
                del self._uploaded_certs[path]
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
            uuid = sender.document_uuid
            path = self.cert_path_from_uuid(uuid)
            if path in self._uploaded_certs:
                # Remove all references
                del self._uploaded_certs[path]
                del self._cert_upload_status[path]

                # Emit signal with status info
                self.removed.emit((path, False, err_msg))

    def upload_status(self, file_path):
        """
        Gets the upload status of the document with the given path.
        :param file_path: Certificate file path.
        :type file_path: str
        :return: Returns the status indicating whether the document is
        NOT_UPLOADED, SUCCESSFUL or ERROR occurred, else returns -1 if
        the given file path is not found.
        ":rtype: int
        """
        return self._cert_upload_status.get(file_path, -1)
