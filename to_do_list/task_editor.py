from PySide6.QtWidgets import  QPushButton,  QVBoxLayout,  QComboBox, QDialog
from PySide6.QtCore import Slot 
from PySide6.QtCore import Signal

class TaskEditor(QDialog):
    task_updated = Signal(int, str)

    def __init__(self, row: int, status: str):
        """
        Initializes TaskEditor dialog to edit the status of the task.
        """
        super().__init__()
        self.initialize_widgets(row, status)
        self.__row = row
        self.status_combo.setCurrentText(status) 
        self.save_button.clicked.connect(self.__on_save_status)

    def initialize_widgets(self, row: int, status: str):
        """
        Given:  Code to create and initialize the QWindow
        and all of the widgets on the window.
        DO NOT EDIT.
        """
        self.setWindowTitle("Edit Task Status")

        self.row = row

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done"])
        

        self.save_button = QPushButton("Save", self)


        layout = QVBoxLayout()
        layout.addWidget(self.status_combo)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        self.setFixedWidth(150)

    @Slot()
    def __on_save_status(self):
        """
        A slot method that saves the status for a specified task and emits an update signal

        - Sets a variable to grab the selected status from the status combo box
        - Emits the task_updated signal with the selected row and status
        - Dialog is closed indicating the action is complete 
        """
        status = self.status_combo.currentText()
        self.task_updated.emit(self.__row, status)
        self.accept()




