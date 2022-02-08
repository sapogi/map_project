import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lon = 37.530887
        self.lat = 55.703118
        self.z = 17
        self.params = {
            'll':f'{self.lon},{self.lat}',
            'z':self.z,
            'l':'map'
        }

        self.getImage()
        uic.loadUi('design.ui', self)
        self.label.setPixmap(QPixmap('map.png'))

    def getImage(self):

        map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params=self.params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())