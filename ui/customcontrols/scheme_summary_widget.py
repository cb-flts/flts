"""
/***************************************************************************
Name                 : SchemeSummaryWidget
Description          : A table widget that provides a quick access menus for
                       uploading and viewing supporting documents.
Date                 : 16/July/2019
copyright            : (C) 2019 by UN-Habitat and implementing partners.
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

from PyQt4.QtGui import (
    QTreeWidget,
    QTreeWidgetItem,
    QLabel,
    QWidget,
    QMessageBox
)
from PyQt4.QtCore import (
    pyqtSignal,
    Qt
)


class SchemeSummaryWidget(QTreeWidget):
    """
    A widget for displaying scheme summary information after lodgement
    """
    link_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QTreeWidget, self).__init__(parent)

        self.setHeaderHidden(True)
        self.setColumnCount(2)
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 200)
        self._scheme = None
        self._documents = None
        self._holder = None

        # Widget items
        self.scheme_info = QTreeWidgetItem()
        self.supporting_document = QTreeWidgetItem()
        self.holders_info = QTreeWidgetItem()
        self.scm_num = QTreeWidgetItem()
        self.scm_name = QTreeWidgetItem()
        self.scm_date_apprv = QTreeWidgetItem()
        self.scm_date_est = QTreeWidgetItem()
        self.scm_ra_type = QTreeWidgetItem()
        self.scm_ra_name = QTreeWidgetItem()
        self.scm_land_hold_num = QTreeWidgetItem()
        self.scm_sg_num = QTreeWidgetItem()
        self.scm_title_deed_num = QTreeWidgetItem()
        self.scm_lro = QTreeWidgetItem()
        self.scm_region = QTreeWidgetItem()
        self.scm_desc = QTreeWidgetItem()
        self.scm_reg_div = QTreeWidgetItem()
        self.scm_numplots = QTreeWidgetItem()
        self.scm_blk_area = QTreeWidgetItem()

        self._page_name = 'page_name'

        view_str = self.tr('Go to page')

        # Labels for holders and documents
        self.lbl_view_holders = self.create_hyperlink_widget(view_str, 'HLD')
        self.lbl_view_holders.linkActivated.connect(self.on_hyperlink_click)
        self.lbl_view_support_docs = self.create_hyperlink_widget(view_str, 'DOC')
        self.lbl_view_support_docs.linkActivated.connect(self.on_hyperlink_click)

        self._initialize_view()

    def _initialize_view(self):
        """
        Set scheme details to be shown in a summary as collapsed items.
        """
        # call label
        # Define top-level items
        self.scheme_info.setText(0, self.tr('Scheme Information'))
        self.supporting_document.setText(0, self.tr('Supporting Documents'))
        self.holders_info.setText(0, self.tr('List of Holders: '))
        self.addTopLevelItems([self.scheme_info, self.supporting_document,
                               self.holders_info])

        # Add child elements items to categories
        self.scheme_info.addChildren(
            [self.scm_num,
             self.scm_name,
             self.scm_date_apprv,
             self.scm_date_est,
             self.scm_ra_type,
             self.scm_ra_name,
             self.scm_land_hold_num,
             self.scm_sg_num,
             self.scm_title_deed_num,
             self.scm_lro,
             self.scm_region,
             self.scm_desc,
             self.scm_reg_div,
             self.scm_numplots,
             self.scm_blk_area]
        )

        # Expand top-level items
        self.scheme_info.setExpanded(True)
        # self.supporting_document.setExpanded(True)

        # Static children items
        # Scheme
        self.scm_region.setText(0,
                                self.tr('Region ')
                                )
        self.scm_ra_type.setText(0,
                                 self.tr('Type of Relevant Authority ')
                                 )
        self.scm_ra_name.setText(0,
                                 self.tr('Name of Relevant Authority ')
                                 )
        self.scm_land_hold_num.setText(0,
                                       self.tr('Land Hold Plan Number ')
                                       )
        self.scm_sg_num.setText(0,
                                self.tr('Surveyor General Number ')
                                )
        self.scm_title_deed_num.setText(0,
                                        self.tr('Title Deed Number ')
                                        )
        self.scm_num.setText(0,
                             self.tr('Number of Scheme ')
                             )
        self.scm_name.setText(0,
                              self.tr('Name of Scheme ')
                              )
        self.scm_date_apprv.setText(0,
                                    self.tr('Date of Approval')
                                    )
        self.scm_date_est.setText(0,
                                  self.tr('Date of Establishment ')
                                  )
        self.scm_lro.setText(0,
                             self.tr('Land Rights Office ')
                             )
        self.scm_desc.setText(0,
                              self.tr('Scheme Description ')
                              )
        self.scm_reg_div.setText(0,
                                 self.tr('Registration Division ')
                                 )
        self.scm_numplots.setText(0,
                                  self.tr('Number of Plots ')
                                  )
        self.scm_blk_area.setText(0,
                                  self.tr('Block Area ')
                                  )

        # Set links for holders and documents
        self.setItemWidget(self.holders_info, 1,
                           self.lbl_view_holders)
        self.setItemWidget(self.supporting_document, 1,
                           self.lbl_view_support_docs)

    def create_hyperlink_widget(self, name, code):
        """
        Creates a clickable QLabel widget that appears like a hyperlink.
        :param name: Display name of the hyperlink.
        :type name: str
        :return: Returns the QLabel widget with appearance of a hyperlink.
        :rtype: QLabel
        """
        lbl_link = QLabel()
        lbl_link.setAlignment(Qt.AlignLeft)
        lbl_link.setText(u'<a href=\'placeholder\'>{0}</a>'.format(name))
        lbl_link.setTextInteractionFlags(Qt.TextBrowserInteraction)

        lbl_link.setProperty(self._page_name, code)

        return lbl_link

    def on_hyperlink_click(self):
        """
        Slot raised when hyperlink to view documents has been clicked.
        Navigate back to the documents page or holders page based on the
        clicked link.
        :return:str
        """
        sender = self.sender()
        if not self._is_page_name_valid(sender):
            return

        code = sender.property(self._page_name)

        self.link_clicked.emit(code)

    def _is_page_name_valid(self, sender):
        # Assert if the page called by signal can be found
        if not sender:
            QMessageBox.critical(
                self,
                self.tr('Error'),
                self.tr(
                    'Error in finding the page'
                )
            )
            return False

        return True
