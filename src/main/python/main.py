import json
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from models import CardListModel, RelicListModel
from util import encode_dict, decode_data_str


class SaveEditor(QDialog):
    def __init__(self, parent=None):
        super(SaveEditor, self).__init__(parent)

        self.key = 'key'
        self.game_save = None
        self.import_path = None

        self.create_import_group_box()
        self.create_card_selection_group_box()
        self.create_relic_selection_group_box()
        self.create_export_group_box()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.import_group_box)

        card_and_relic_selection_layout = QHBoxLayout()
        card_and_relic_selection_layout.addWidget(self.card_selection_group_box)
        card_and_relic_selection_layout.addWidget(self.relic_selection_group_box)
        main_layout.addLayout(card_and_relic_selection_layout)

        main_layout.addWidget(self.export_group_box)

        self.setLayout(main_layout)
        self.setMinimumWidth(720)
        self.setMinimumHeight(720)
        self.setWindowTitle("Save Editor")

    def create_export_group_box(self) -> None:
        self.export_group_box = QGroupBox("Export")
        layout = QHBoxLayout()
        export_json_button = QPushButton("Export JSON")
        export_json_button.clicked.connect(self.export_json)
        export_save_button = QPushButton("Export Save File")
        export_save_button.clicked.connect(self.export_file)

        layout.addWidget(export_save_button)
        layout.addWidget(export_json_button)
        self.export_group_box.setLayout(layout)
        self.export_group_box.setDisabled(True)

    def create_import_group_box(self) -> None:
        self.import_group_box = QGroupBox("Import")
        outer_layout = QVBoxLayout()
        status_label = QLabel('Choose a save file to import')
        status_label.setWordWrap(True)
        self.status_label = status_label
        status_label.setAlignment(Qt.AlignCenter)
        outer_layout.addWidget(status_label)

        import_json_button = QPushButton("Import JSON")
        import_json_button.clicked.connect(self.import_json)

        import_save_file_button = QPushButton("Import Save File")
        import_save_file_button.clicked.connect(self.import_file)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(import_save_file_button)
        buttons_layout.addWidget(import_json_button)

        outer_layout.addLayout(buttons_layout)
        self.import_group_box.setLayout(outer_layout)

    def create_card_selection_group_box(self) -> None:
        self.card_selection_group_box = QGroupBox("Cards")
        layout = QVBoxLayout()

        self.card_list_model = CardListModel()
        card_list_view = QListView()
        self.card_list_view = card_list_view
        card_list_view.setSelectionMode(QListWidget.ExtendedSelection)
        card_list_view.setModel(self.card_list_model)
        layout.addWidget(card_list_view)

        button_group = QHBoxLayout()

        add_button = QPushButton('Add')
        add_button.clicked.connect(self.add_card)

        remove_button = QPushButton('Remove')
        remove_button.clicked.connect(self.remove_card)

        upgrade_button = QPushButton('Upgrade')
        upgrade_button.clicked.connect(self.upgrade_card)

        button_group.addWidget(add_button)
        button_group.addWidget(remove_button)
        button_group.addWidget(upgrade_button)
        layout.addLayout(button_group)

        self.card_selection_group_box.setLayout(layout)
        self.card_selection_group_box.setDisabled(True)

    def create_relic_selection_group_box(self) -> None:
        self.relic_selection_group_box = QGroupBox("Relics")
        layout = QVBoxLayout()

        self.relic_list_model = RelicListModel()
        relic_list_view = QListView()
        self.relic_list_view = relic_list_view
        relic_list_view.setSelectionMode(QListWidget.ExtendedSelection)
        relic_list_view.setModel(self.relic_list_model)
        layout.addWidget(relic_list_view)

        button_group = QHBoxLayout()
        add_button = QPushButton('Add')
        add_button.clicked.connect(self.add_relic)
        remove_button = QPushButton('Remove')
        remove_button.clicked.connect(self.remove_relic)

        button_group.addWidget(add_button)
        button_group.addWidget(remove_button)
        layout.addLayout(button_group)

        self.relic_selection_group_box.setLayout(layout)
        self.relic_selection_group_box.setDisabled(True)

    def save_file_dialog(self, file_type: str = 'All Files (*)', dir: str = '') -> str:
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save file", dir, file_type, options=options)
        return file_name

    def open_file_dialog(self, file_type: str = 'All Files (*)', dir: str = '') -> str:
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Browse for file", dir, file_type, options=options)
        return file_name

    def import_file(self) -> None:
        self.import_path = self.open_file_dialog('Autosave Files (*.autosave);;All Files(*)',
                                                 'C:/Program Files (x86)/Steam/steamapps/common/SlayTheSpire/saves')
        if self.import_path:
            self.status_label.setText('Imported save file at:\n' + self.import_path or 'none')
            with open(self.import_path, 'r') as file:
                data = file.read()
                self.game_save = decode_data_str(data, self.key)
                self.game_save_to_models()
        else:
            self.alert('No path specified!', QMessageBox.Warning)

    def import_json(self) -> None:
        json_path = self.open_file_dialog('JSON Files (*.json);;All Files(*)')
        if json_path:
            self.status_label.setText('Imported JSON file at:\n' + json_path)
            with open(json_path, 'r') as file:
                data = file.read()
                self.game_save = json.loads(data)
                self.game_save_to_models()
        else:
            self.alert('No path specified!', QMessageBox.Warning)

    def game_save_to_models(self) -> None:

        self.card_list_model.cards = []
        for card in self.game_save['cards']:
            self.card_list_model.cards.append(card)
        self.card_list_model.layoutChanged.emit()

        self.relic_list_model.relics = []
        for relic in self.game_save['relics']:
            self.relic_list_model.relics.append(relic)
        self.relic_list_model.layoutChanged.emit()

        self.card_selection_group_box.setDisabled(False)
        self.relic_selection_group_box.setDisabled(False)
        self.export_group_box.setDisabled(False)

    def export_json(self) -> None:
        json_file_name = self.save_file_dialog('JSON Files (*.json);;All Files (*)')
        if json_file_name:
            with open(json_file_name, 'w') as file:
                file.write(json.dumps(self.game_save, indent=4))
        else:
            self.alert('No path specified!', QMessageBox.Warning)

    def export_file(self) -> None:
        save_file_name = self.save_file_dialog('Save Files (*.autosave);;All Files (*)')
        if save_file_name:
            with open(save_file_name, 'wb') as file:
                file.write(encode_dict(self.game_save, self.key))
        else:
            self.alert('No path specified!', QMessageBox.Warning)

    def replace_file(self) -> None:
        if self.import_path:
            with open(self.import_path, 'wb') as file:
                file.write(encode_dict(self.game_save, self.key))
        else:
            self.alert('No path specified!', QMessageBox.Warning)

    def alert(self, text: str = 'Error', icon=QMessageBox.Critical) -> None:
        alert = QMessageBox()
        alert.setText(text)
        alert.setIcon(icon)
        alert.setWindowTitle(' ')
        alert.exec_()

    def add_card(self):
        self.card_list_model.cards.append({'upgrades': 0, 'misc': 0, 'id': 'New Card'})

        self.game_save['cards'] = self.card_list_model.cards
        self.card_list_model.layoutChanged.emit()

    def remove_card(self):
        indices = [i.row() for i in self.card_list_view.selectedIndexes()]
        for index in sorted(indices, reverse=True):
            del self.card_list_model.cards[index]

        self.game_save['cards'] = self.card_list_model.cards
        self.card_list_model.layoutChanged.emit()
        self.card_list_view.clearSelection()

    def upgrade_card(self):
        indices = [i.row() for i in self.card_list_view.selectedIndexes()]
        for index in indices:
            self.card_list_model.cards[index]['upgrades'] = 1

        self.game_save['cards'] = self.card_list_model.cards
        self.card_list_model.layoutChanged.emit()
        self.card_list_view.clearSelection()

    def add_relic(self):
        self.relic_list_model.relics.append('New Relic')
        self.game_save['relics'] = self.relic_list_model.relics
        self.relic_list_model.layoutChanged.emit()

    def remove_relic(self):
        indices = [i.row() for i in self.relic_list_view.selectedIndexes()]
        for index in sorted(indices, reverse=True):
            del self.relic_list_model.relics[index]

        self.game_save['relics'] = self.relic_list_model.relics
        self.relic_list_model.layoutChanged.emit()
        self.relic_list_view.clearSelection()


if __name__ == '__main__':
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    editor = SaveEditor()
    editor.show()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
