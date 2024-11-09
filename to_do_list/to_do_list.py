"""
Description: Creating a to-do list that allows us to add tasks and their status as well as edit tasks on completion.
Author: Ranindi Gunasekera
"""

from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel, QMessageBox, QVBoxLayout, QWidget, QTableWidgetItem, QComboBox
from PySide6.QtCore import Slot
from to_do_list.task_editor import TaskEditor
import csv

class ToDoList(QMainWindow):
    def __init__(self):
        """
        Initializes main application window and sets up widgets and connections.
        """
        super().__init__()
        self.__initialize_widgets()
        self.add_button.clicked.connect(self.__on_add_task)
        self.task_table.cellClicked.connect(self.__on_edit_task)


    def __initialize_widgets(self):
        """
        Given:  Code to create and initialize the QWindow
        and all of the widgets on the window.
        DO NOT EDIT.
        """
        self.setWindowTitle("To-Do List")

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("New Task")

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done"])

        self.add_button = QPushButton("Add Task", self)

        self.save_button = QPushButton("Save to CSV", self)
        

        self.task_table = QTableWidget(self)
        self.task_table.setColumnCount(2)
        self.task_table.setHorizontalHeaderLabels(["Task", "Status"])


        self.status_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.task_input)
        layout.addWidget(self.status_combo)
        layout.addWidget(self.add_button)
        layout.addWidget(self.task_table)
        layout.addWidget(self.save_button)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Part 3
    def __load_data(self, file_path: str):
        """
        Reads data from the .csv file provided.
        Calls the __add_table_row method (to be implemented) 
        for each row of data.
        Args:
            file_path (str): The name of the file (including relative path).
        """
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header row
            header = next(reader)  
            for row in reader:
                self.__add_table_row(row)
    
    def __add_table_row(self, row_data):
        """
        Remove the pass statement below to implement this method.
        """
        pass
    
    def __save_to_csv(self):
        """
        Saves the QTable data to a file.
        """
        file_path = 'output/todos.csv'
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(["Task", "Status"])

    @Slot()
    def __on_add_task(self):
        """
        Slot method to add a new task into the task table

        - Retrieves text from task input and the status combo
        - Checks if task has been inputted (if blank or not) and
            adds a new row with task description and status
        - Adds a success message when task successfully added
        - If no task inputted, message displayed to enter a task    
            with its corresponding status
        """
        task = self.task_input.text()
        status = self.status_combo.currentText()

        if len(task.strip()) > 0:
            current_rows = self.task_table.rowCount()
            self.task_table.insertRow(current_rows)

            task_item = QTableWidgetItem(task)
            status_item = QTableWidgetItem(status)

            self.task_table.setItem(current_rows, 0, task_item)
            self.task_table.setItem(current_rows, 1, status_item)

            self.status_label.setText(f"Added task: {task}")
        else:
            self.status_label.setText(f"Please enter a task and select its status.")

    @Slot(int, int)
    def __on_edit_task(self, row:int, column:int):
        """
        Slot method to edit the status of a task by opening a dialog

        Parameters:
            row(int): the row of the clicked cell which indicates the task to edit
            column(int): column of the clicked cell
            
        - Grabs the current status of the selected row
        - Creates an instance of the TaskEditor class to open a dialog with the current task status
        - Connects the task_updated signal from TaskEditor to __update_task_status
        - Opens the TaskEditor dialog 
        """
        current_status = self.task_table.item(row, 1).text()

        task_editor = TaskEditor(row, current_status)
        task_editor.task_updated.connect(self.__update_task_status)
        task_editor.exec()

    @Slot()
    def __update_task_status(self, row: int, new_status:str):
        """
        A slot method that updates the status of a task on the table

        Parameters:
            row(int): the row of the clicked cell which indicates the task to edit
            new_status(str): the new status text that will be set for the task

        - Creates a new QTableWidgetItem with the new_status text
        - Replaces the status item in the table with the new item i.e the updated status
        - Updates the status label to display a message that shows the task has been successfully updated
        """
        new_status_item = QTableWidgetItem(new_status)
        self.task_table.setItem(row, 1, new_status_item)
        self.status_label.setText(f"Task status updated to: {new_status}")
