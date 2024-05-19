import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QMessageBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ClickableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.on_click()
        super().mousePressEvent(event)

    def on_click(self):
        QMessageBox.information(self, "Click Event", "Graphics view clicked!")

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matplotlib in PyQt")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a Matplotlib figure with a larger size
        fig = Figure(figsize=(10, 6))  # Width, Height in inches
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3, 4], [1, 4, 9, 16])

        # Add text annotation directly to the figure
        fig.text(0.5, 0.5, 'Sample Text', fontsize=12, color='red', ha='center')

        # Adjust the layout to prevent clipping of labels/titles
        fig.tight_layout(pad=2.0, h_pad=2.0, w_pad=2.0)  # pad, h_pad, and w_pad in inches

        # Create a FigureCanvasQTAgg instance
        canvas = FigureCanvas(fig)

        # Create a QGraphicsScene and add the FigureCanvasQTAgg widget to it
        scene = QGraphicsScene()
        proxy = scene.addWidget(canvas)

        # Create a ClickableGraphicsView instance and set the scene
        graphics_view = ClickableGraphicsView()
        graphics_view.setScene(scene)
        
        # Add the ClickableGraphicsView to the layout
        layout.addWidget(graphics_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
