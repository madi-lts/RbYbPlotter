import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matplotlib in PyQt")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a Matplotlib figure
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3, 4], [1, 4, 9, 16])

        # Add text annotation directly to the figure
        fig.text(0.5, 0.5, 'Sample Text', fontsize=12, color='red', ha='center')

        # Create a FigureCanvasQTAgg instance and add it to the layout
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
