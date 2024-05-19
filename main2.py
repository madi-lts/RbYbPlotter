import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, 
    QGraphicsView, QGraphicsScene, QRadioButton, QHBoxLayout
)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Qt GUI")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.main_layout = QGridLayout(self.central_widget)

        self.label = QLabel("Hello, world!")
        self.main_layout.addWidget(self.label, 0, 0, 1, 2)  # Span across two columns

        self.direction_layout = QHBoxLayout()
        self.main_layout.addLayout(self.direction_layout, 1, 0, 1, 2)  # Span across two columns

        self.horizontal_button = QRadioButton("Horizontal")
        self.vertical_button = QRadioButton("Vertical")
        self.horizontal_button.setChecked(True)
        self.direction_layout.addWidget(self.horizontal_button)
        self.direction_layout.addWidget(self.vertical_button)

        self.button = QPushButton("Add QGraphicsView")
        self.button.clicked.connect(self.add_graphics_view)
        self.main_layout.addWidget(self.button, 2, 0, 1, 2)  # Span across two columns

        self.graphics_grid_start_row = 3  # Starting row for QGraphicsView widgets
        self.graphics_views = []  # List to hold added QGraphicsView widgets

        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def add_graphics_view(self):
        graphics_view = QGraphicsView()
        scene = QGraphicsScene()
        scene.addText("Hello, QGraphicsView!")
        graphics_view.setScene(scene)
        
        num_graphics_views = len(self.graphics_views)
        
        if self.horizontal_button.isChecked():
            row = self.graphics_grid_start_row + (num_graphics_views // 2)
            col = num_graphics_views % 2
        else:
            row = self.graphics_grid_start_row + num_graphics_views
            col = 0
        
        self.main_layout.addWidget(graphics_view, row, col, 1, 1)
        self.graphics_views.append(graphics_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
