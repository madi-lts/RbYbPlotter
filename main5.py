import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, 
    QGraphicsView, QGraphicsScene, QRadioButton, QVBoxLayout, QHBoxLayout
)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Qt GUI")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()

        # Create the main vertical layout
        self.main_vertical_layout = QVBoxLayout(self.central_widget)

        # Create the layout for direction radio buttons
        self.direction_layout = QHBoxLayout()
        self.horizontal_button = QRadioButton("Horizontal")
        self.vertical_button = QRadioButton("Vertical")
        self.horizontal_button.setChecked(True)
        self.direction_layout.addWidget(self.horizontal_button)
        self.direction_layout.addWidget(self.vertical_button)

        # Add the direction layout to the main vertical layout
        self.main_vertical_layout.addLayout(self.direction_layout)

        # Create the grid layout for QGraphicsView widgets
        self.graphics_layout = QGridLayout()
        self.graphics_layout_shape = []
        self.button = QPushButton("Add QGraphicsView")
        self.button.clicked.connect(self.add_graphics_view)
        self.main_vertical_layout.addWidget(self.button)

        self.graphics_grid_start_row = 0  # Starting row for QGraphicsView widgets
        self.graphics_views = []  # List to hold added QGraphicsView widgets

        # Add the grid layout to the main vertical layout
        self.main_vertical_layout.addLayout(self.graphics_layout)

        self.central_widget.setLayout(self.main_vertical_layout)
        self.setCentralWidget(self.central_widget)

    def add_graphics_view(self):
        graphics_view = QGraphicsView()
        scene = QGraphicsScene()
        scene.addText("Hello, QGraphicsView!")
        graphics_view.setScene(scene)

        num_graphics_views = len(self.graphics_views)

        if self.horizontal_button.isChecked():
            row = self.graphics_grid_start_row
            col = num_graphics_views
            # Add the widget and make it span the same number of columns as the total count of graphics views
            colspan = 1
            self.graphics_layout.addWidget(graphics_view, row, col, 1, colspan)
        else:
            row = self.graphics_grid_start_row + num_graphics_views
            col = 0
            rowspan = 1
            self.graphics_layout.addWidget(graphics_view, row, col, rowspan, 1)  # Span 1 row and 1 column

        self.graphics_views.append(graphics_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
