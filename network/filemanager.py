# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Source Document File Manager
Description          : Manages the copying of source documents to/from a 
                       shared folder in a network.
Date                 : 7/August/2013 
copyright            : (C) 2013 by John Gitau
email                : gkahiu@gmail.com
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
from uuid import uuid4

from PyQt4.QtCore import (
    QObject,
    QThread,
    SIGNAL,
    pyqtSignal,
    QFile,
    pyqtSlot,
    QDir
)

from qgis.core import *

from stdm.utils.util import (
    guess_extension
)
from stdm.settings import current_profile


class NetworkFileManager(QObject):
    """
    Provides methods for managing the upload and download of source
    documents from a network repository.
    """

    def __init__(self, network_repository, parent=None):
        QObject.__init__(self, parent)
        self.networkPath = network_repository
        self.fileID = None
        self.sourcePath = None
        self.destinationPath = None
        self.curr_profile = current_profile()
        self._entity_source = ''
        self._doc_type = ''

    def uploadDocument(self, entity_source, doc_type, fileinfo):
        """
        Upload document in central repository
        """
        self._entity_source = entity_source
        self._doc_type = doc_type
        self.fileID = self.generateFileID()
        self.sourcePath = unicode(fileinfo.filePath())
        profile_name = self.curr_profile.name
        root_dir = QDir(self.networkPath)
        doc_dir = QDir(u'{}/{}/{}/{}'.format(
            self.networkPath,
            profile_name.lower(),
            self._entity_source,
            self._doc_type.lower().replace(' ', '_')
        )
        )
        doc_path_str = u'{}/{}/{}/{}'.format(
            self.networkPath,
            profile_name.lower(),
            self._entity_source,
            self._doc_type.lower().replace(' ', '_')
        ).lower()

        if not doc_dir.exists():
            res = root_dir.mkpath(doc_path_str)
            if res:
                root_doc_type_path = doc_path_str

            else:
                root_doc_type_path = self.networkPath

        else:
            root_doc_type_path = doc_path_str

        self.destinationPath = u'{}/{}.{}'.format(
            root_doc_type_path,
            self.fileID,
            fileinfo.completeSuffix()
        )

        srcFile = open(self.sourcePath, 'rb')
        destinationFile = open(self.destinationPath, 'wb')

        # srcLen = self.sourceFile.bytesAvailable()
        totalRead = 0
        while True:
            inbytes = srcFile.read(4096)
            if not inbytes:
                break
            destinationFile.write(inbytes)
            totalRead += len(inbytes)
            # Raise signal on each block written
            self.emit(SIGNAL("blockWritten(int)"), totalRead)

        self.emit(SIGNAL("completed(QString)"), self.fileID)

        srcFile.close()
        destinationFile.close()

        return self.fileID

    def downloadDocument(self, documentid):
        """
        Get the document from the central repository using its unique identifier.
        """
        pass

    def deleteDocument(self, docmodel=None, doc_type=None):
        """
        Delete the source document from the central repository.
        """
        if not docmodel is None:
            # Build the path from the model variable values.
            fileName, fileExt = guess_extension(docmodel.filename)
            profile_name = self.curr_profile.name
            # Qt always expects the file separator be be "/" regardless of platform.
            absPath = u'{}/{}/{}/{}/{}{}'.format(
                self.networkPath,
                profile_name.lower(),
                docmodel.source_entity,
                doc_type.lower().replace(' ', '_'),
                docmodel.document_identifier,
                fileExt
            )

            return QFile.remove(absPath)

        else:
            return QFile.remove(self.destinationPath)

    def generateFileID(self):
        """
        Generates a unique file identifier that will be used to copy to the 
        """
        return str(uuid4())


class DocumentTransferWorker(QObject):
    """
    Worker thread for copying source documents to central repository.
    """
    blockWrite = pyqtSignal("int")
    complete = pyqtSignal("QString")

    def __init__(
            self, file_manager, file_info, entity_source='', doc_type='', parent=None):
        QObject.__init__(self, parent)
        self._file_manager = file_manager
        self._file_info = file_info
        self._entity_source = entity_source
        self._doc_type = doc_type
        self.file_uuid = None

    @pyqtSlot()
    def transfer(self):
        """
        Initiate document transfer
        """
        self.connect(self._file_manager, SIGNAL("blockWritten(int)"), self.onBlockWritten)
        self.connect(self._file_manager, SIGNAL("completed(QString)"), self.onWriteComplete)
        self._file_manager.uploadDocument(
            self._entity_source, self._doc_type, self._file_info
        )
        self.file_uuid = self._file_manager.fileID

    def onBlockWritten(self, size):
        """
        Propagate event.
        """
        self.blockWrite.emit(size)

    def onWriteComplete(self, file_uuid):
        """
        Propagate event.
        """
        self.complete.emit(file_uuid)
