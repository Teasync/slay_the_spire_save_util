from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import *


# {'upgrades': 0, 'misc': 0, 'id': 'Strike_P'}

class CardListModel(QAbstractListModel):
    def __init__(self, *args, cards=None, **kwargs):
        super(CardListModel, self).__init__(*args, **kwargs)
        self.cards = cards or []

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if role == Qt.DisplayRole or role == Qt.EditRole:
            text = self.cards[index.row()]['id']
            return text

        if role == Qt.DecorationRole:
            upgraded = self.cards[index.row()]['upgrades'] != 0
            if upgraded:
                return QColor('green')
            else:
                return QColor('lightGray')

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.cards)

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def setData(self, index: QModelIndex, value: Any, role: int = ...) -> bool:
        if index.isValid() and role == Qt.EditRole:
            self.cards[index.row()]['id'] = value
            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        return False


class RelicListModel(QAbstractListModel):
    def __init__(self, *args, relics=None, **kwargs):
        super(RelicListModel, self).__init__(*args, **kwargs)
        self.relics = relics or []

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if role == Qt.DisplayRole or role == Qt.EditRole:
            text = self.relics[index.row()]
            return text

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.relics)

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def setData(self, index: QModelIndex, value: Any, role: int = ...) -> bool:
        if index.isValid() and role == Qt.EditRole:
            self.relics[index.row()] = value
            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        return False
