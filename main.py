import os
import sys
import math
import requests

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lon = 37.530887
        self.lat = 55.703118
        self.flag_lon, self.flag_lat = self.lon, self.lat
        self.z = 17
        self.step = 0.002
        self.lay = 'map'
        uic.loadUi('design.ui', self)

        self.lineEdit.setEnabled(False)
        self.pushButton.setEnabled(False)
        self.pushButton.clicked.connect(self.find_object)
        self.checkBox.stateChanged.connect(self.on_or_off)
        self.render_map()

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
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:
            self.lay = 'map'
            self.render_map()
        if event.key() == Qt.Key_2:
            self.lay = 'sat'
            self.render_map()
        if event.key() == Qt.Key_3:
            self.lay = 'sat,skl'
            self.render_map()
        if event.key() == Qt.Key_A:
            self.lon -= self.step * math.pow(2, 15 - self.z)
            self.render_map()
        if event.key() == Qt.Key_D:
            self.lon += self.step * math.pow(2, 15 - self.z)
            self.render_map()
        if event.key() == Qt.Key_S:
            self.lat -= self.step * math.pow(2, 15 - self.z)
            self.render_map()
        if event.key() == Qt.Key_W:
            self.lat += self.step * math.pow(2, 15 - self.z)
            self.render_map()

    def render_map(self):
        self.params = {
            'll': f'{self.lon},{self.lat}',
            'z': self.z,
            'l': self.lay,
            'pt': f'{self.flag_lon},{self.flag_lat},pm2rdm'
        }
        self.getImage()
        self.label.setPixmap(QPixmap('map.png'))

    def on_or_off(self):
        if self.sender().isChecked():
            self.lineEdit.setEnabled(True)
            self.pushButton.setEnabled(True)
        else:
            self.lineEdit.setEnabled(False)
            self.pushButton.setEnabled(False)

    def find_object(self):
        if self.lineEdit.text():
            el = self.lineEdit.text()
            req = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={el}&format=json"
            response = requests.get(req)
            if response:
                json_response = response.json()

                try:
                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                    toponym_coodrinates = toponym["Point"]["pos"]
                    print(toponym_address, "имеет координаты:", toponym_coodrinates)
                    toponym_coodrinates = toponym_coodrinates.split()
                    self.lon, self.lat = float(toponym_coodrinates[0]), float(toponym_coodrinates[1])
                    self.flag_lon, self.flag_lat = self.lon, self.lat
                    self.render_map()
                except Exception as ex:
                    print(ex)
                    self.label.setPixmap(QPixmap('error.jpg'))
            else:
                print("Ошибка выполнения запроса:")
                print(req)
                print("Http статус:", response.status_code, "(", response.reason, ")")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
