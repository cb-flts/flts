from PyQt4.QtGui import (
    QWidget
)

from ui_flts_search import Ui_flts_search


class FLTSSearch(QWidget, Ui_flts_search):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setupUi(self)

