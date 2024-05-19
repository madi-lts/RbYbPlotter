import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget,
    QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QLineEdit,
    QMessageBox, QTabWidget
)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Qt GUI")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create the main vertical layout for the central widget
        self.main_vertical_layout = QVBoxLayout(self.central_widget)

        # Create the tab widget and add two tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        self.main_vertical_layout.addWidget(self.tabs)

        # Initialize layouts for both tabs
        self.graphics_layout_1 = QGridLayout()
        self.graphics_layout_2 = QGridLayout()

        # Set up the first tab
        self.setup_tab(self.tab1, self.graphics_layout_1)
        # Set up the second tab
        self.setup_tab(self.tab2, self.graphics_layout_2)

    def setup_tab(self, tab, graphics_layout):
        tab_layout = QVBoxLayout(tab)

        # Create the layout for row, col, colspan, and rowspan QLineEdit objects
        span_layout = QHBoxLayout()
        self.row_edit = QLineEdit()
        self.col_edit = QLineEdit()
        self.col_span_edit = QLineEdit()
        self.row_span_edit = QLineEdit()

        span_layout.addWidget(QLabel("Row:"))
        span_layout.addWidget(self.row_edit)
        span_layout.addWidget(QLabel("Col:"))
        span_layout.addWidget(self.col_edit)
        span_layout.addWidget(QLabel("Colspan:"))
        span_layout.addWidget(self.col_span_edit)
        span_layout.addWidget(QLabel("Rowspan:"))
        span_layout.addWidget(self.row_span_edit)
        tab_layout.addLayout(span_layout)

        # Add button to add QGraphicsView
        button = QPushButton("Add QGraphicsView")
        button.clicked.connect(self.add_graphics_view)
        tab_layout.addWidget(button)

        # Add the grid layout to the tab layout
        tab_layout.addLayout(graphics_layout)

        tab.setLayout(tab_layout)

    def add_graphics_view(self):
        row_text = self.row_edit.text()
        col_text = self.col_edit.text()
        col_span_text = self.col_span_edit.text()
        row_span_text = self.row_span_edit.text()

        try:
            row = int(row_text) if row_text else 0
            col = int(col_text) if col_text else max(self.graphics_layout_1.columnCount(), self.graphics_layout_2.columnCount())
            colspan = int(col_span_text) if col_span_text else 1
            rowspan = int(row_span_text) if row_span_text else 1
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid integer values for row, col, colspan, and rowspan.")
            return

        self.add_graphics_view_to_layout(self.graphics_layout_1, row, col, rowspan, colspan)
        self.add_graphics_view_to_layout(self.graphics_layout_2, row, col, rowspan, colspan)

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
