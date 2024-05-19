import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget,
    QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QLineEdit,
    QMessageBox, QTabWidget, QPlainTextEdit
)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RbYb Plotter")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create the main vertical layout for the central widget
        self.main_vertical_layout = QVBoxLayout(self.central_widget)

        # Create the tab widget and add two tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Python Code")
        self.tabs.addTab(self.tab2, "Plots")

        self.main_vertical_layout.addWidget(self.tabs)

        # Initialize layouts for both tabs
        self.graphics_layout_1 = QGridLayout()
        self.graphics_layout_2 = QGridLayout()

        # Set up the first tab
        self.setup_tab(self.tab1, self.graphics_layout_1, code_tab=True)
        # Set up the second tab
        self.setup_tab(self.tab2, self.graphics_layout_2, code_tab=False)

        # Track the maximum number of columns used
        self.max_col_1 = 0
        self.max_col_2 = 0

    def setup_tab(self, tab, layout, code_tab=False):
        tab_layout = QVBoxLayout(tab)

        # Create the layout for row, col, colspan, and rowspan QLineEdit objects
        span_layout = QHBoxLayout()
        row_edit = QLineEdit()
        col_edit = QLineEdit()
        col_span_edit = QLineEdit()
        row_span_edit = QLineEdit()

        span_layout.addWidget(QLabel("Row:"))
        span_layout.addWidget(row_edit)
        span_layout.addWidget(QLabel("Col:"))
        span_layout.addWidget(col_edit)
        span_layout.addWidget(QLabel("Colspan:"))
        span_layout.addWidget(col_span_edit)
        span_layout.addWidget(QLabel("Rowspan:"))
        span_layout.addWidget(row_span_edit)
        tab_layout.addLayout(span_layout)

        # Add button to add widget
        button = QPushButton("Add QPlainTextEdit" if code_tab else "Add QGraphicsView")
        button.clicked.connect(lambda: self.add_widget(code_tab, row_edit, col_edit, col_span_edit, row_span_edit))
        tab_layout.addWidget(button)

        # Add the grid layout to the tab layout
        tab_layout.addLayout(layout)

        tab.setLayout(tab_layout)

    def add_widget(self, code_tab, row_edit, col_edit, col_span_edit, row_span_edit):
        row_text = row_edit.text()
        col_text = col_edit.text()
        col_span_text = col_span_edit.text()
        row_span_text = row_span_edit.text()

        try:
            row = int(row_text) if row_text else 0
            col = int(col_text) if col_text else max(self.max_col_1 if code_tab else self.max_col_2, 0)
            colspan = int(col_span_text) if col_span_text else 1
            rowspan = int(row_span_text) if row_span_text else 1
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid integer values for row, col, colspan, and rowspan.")
            return

        if code_tab:
            self.add_plain_text_edit_to_layout(self.graphics_layout_1, row, col, rowspan, colspan)
        else:
            self.add_graphics_view_to_layout(self.graphics_layout_2, row, col, rowspan, colspan)

    def add_plain_text_edit_to_layout(self, layout, row, col, rowspan, colspan):
        plain_text_edit = QPlainTextEdit()
        plain_text_edit.setPlainText("Write your Python code here...")
        layout.addWidget(plain_text_edit, row, col, rowspan, colspan)

    def add_graphics_view_to_layout(self, layout, row, col, rowspan, colspan):
        graphics_view = QGraphicsView()
        scene = QGraphicsScene()
        scene.addText("Hello, QGraphicsView!")
        graphics_view.setScene(scene)
        layout.addWidget(graphics_view, row, col, rowspan, colspan)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
