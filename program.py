import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
from PIL import Image
import numpy as np

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Программа')
    
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
    
        self.open_button = QPushButton('Открыть изображение')
        self.open_button.clicked.connect(self.open_image)
    
        self.image_label = QLabel()
    
        self.plot_button = QPushButton('Создать график')
        self.plot_button.clicked.connect(self.create_plot)
    
        self.save_button = QPushButton('Сохранить график')
        self.save_button.clicked.connect(self.save_plot)
    
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
    
        self.left_layout.addWidget(self.open_button)
        self.left_layout.addWidget(self.image_label)
        self.right_layout.addWidget(self.plot_button)
        self.right_layout.addWidget(self.save_button)
        self.right_layout.addWidget(self.canvas)
    
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.left_layout)
        main_layout.addLayout(self.right_layout)
    
        self.setLayout(main_layout)
    
    def save_plot(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить график', 
                                                   '', 
                                                   'Images (*.png *.jpg *.bmp)')
        if file_name:
            self.figure.savefig(file_name)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Открыть изображение', 
                                                   '', 
                                                   'Images (*.png *.xpm *.jpg *.bmp)')
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)

    def create_plot(self):
        x = range(-20, 20)
        y = [math.sin(i) for i in x]
    
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
    
        # Добавляем оси координат
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True)
    
        # Открываем изображение
        image_path = self.image_label.pixmap().toImage().save('image.png')
        img = Image.open('image.png')
    
        # Вырезаем фрагмент изображения
        width, height = img.size
        cropped_img = img.crop((width // 10, height // 1.9, width // 2.1, height // 1.1))
    
        # Преобразуем изображение в numpy-массив
        arr = np.array(cropped_img)
    
        # Помещаем изображение поверх графика
        image = OffsetImage(arr, zoom=1.0)
        ab = AnnotationBbox(image, (20, -1), frameon=False)
        ax.add_artist(ab)
    
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())