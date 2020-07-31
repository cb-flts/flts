from PyQt4.QtCore import (
    Qt,
    QSize
)
from PyQt4.QtGui import QStyledItemDelegate


class IconDelegate(QStyledItemDelegate):
    """
    Sets the properties of icons in the view widget.
    """
    def initStyleOption(self, option, index):
        super(IconDelegate, self).initStyleOption(option, index)
        option.decorationSize = QSize(24, 24)
        # Position decoration to top
        option.decorationPosition = 2
        # Align decoration to center
        option.decorationAlignment = Qt.AlignHCenter
