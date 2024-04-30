#29.02.24//se acualiza por cambios en la estructura del diccionario de la API
import sys, os
import requests
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QTimer
from PyQt5 import QtGui
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtGui import QFont

import datetime

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Variaciones del Dólar")
        self.setGeometry(200, 200, 550, 250)
        #self.setMinimumSize(640,400)

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.IconPath = os.path.join(scriptDir, 'icons')   
        self.setWindowIcon(QtGui.QIcon(self.IconPath + os.path.sep + 'dolar.png'))
        
        # Crear una instancia de QFont con el tipo y tamaño de letra deseado
        #qtfont = QFont("Bebas Neue", 18, QFont.Bold)
        qtfont = QFont("Roboto", 10, QFont.Bold)
        #qtfont = QFont("Ubuntu", 20, QFont.Bold)
        
        # Aplicar el tipo y tamaño de letra a la ventana principal y a los widgets deseados
        self.setFont(qtfont)
        
        self.setAutoFillBackground(True)
        # Configurar el estilo Fusion con un esquema oscuro
        self.set_style()
        #configurar color del grafico
        self.set_colorgraf()

        self.figure = Figure(facecolor="black")
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)

        self.labeltime = QLabel(self)
        self.labeltime.move(60, 18)
        self.labeltime.resize(640, 25)

        self.titulo = QLabel(self)
        self.titulo.move(60, 5)
        self.titulo.resize(640, 25)
        self.titulo.setText("Hola Aquí Tienes la Cotización del Dolar Ultimo Minuto...")

        self.timer = QTimer(self)
        self.timer.setInterval(60000)  # Intervalo de una hora (3600000 ms), un minuto (60000 ms)
        self.timer.timeout.connect(self.update_chart)
        self.timer.start()

        self.update_chart()

    def set_style(self):
        # Obtener el estilo Fusion y configurar el esquema oscuro
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Foreground, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.Background, QColor(25, 25, 25))
        app.setPalette(palette)

    def set_colorgraf(self):
        # Configurar colores específicos para el gráfico
        matplotlib.rcParams['font.family'] = 'Ubuntu'
        matplotlib.rcParams['font.weight'] = 'bold'
        matplotlib.rcParams['font.size'] = 14
        matplotlib.rcParams['text.color'] = 'black'
        matplotlib.rcParams['axes.labelcolor'] = 'grey'
        matplotlib.rcParams['xtick.color'] = 'grey'
        matplotlib.rcParams['ytick.color'] = 'lightgrey'
        matplotlib.rcParams['axes.facecolor'] = 'black'

    def transPanda(self, datos):
        #realiza la tranpuesta de un dataframe y lo retorna
        return datos.T

    def update_chart(self):
        response = requests.get("https://criptoya.com/api/dolar")
        data = json.loads(response.text)
        #print('type data: ',type(data))
                
        #usd_values = {key: value for key, value in data.items() if key in ['blue', 'mep', 'ccl', 'ccb']}
        usd_values = {key: value for key, value in data.items() if key in ['blue', 'cripto', 'mep', 'ccl']}
        #print('type usd_values: ',type(usd_values))
        #print("usd_values: ",usd_values)
        types = list(usd_values.keys())
        values = list(usd_values.values())
        """
        print("debug 19.02.24: la api me cambio el formato del diccionario de precios")
        print('types of usd_values: ', types)
        print('values[0]["ask"] of usd_values: ', values[0]['ask'])
        print('values[1]["ccb"]["ask"] of usd_values: ', values[1]['ccb']['ask'])
        print('values[2]["al30"]["48hs"]["price"] of usd_values: ', values[2]['al30']['48hs']['price'])
        print('values[3]["lede"]["ci"]["price"] of usd_values: ', values[3]['lede']['ci']['price'])
        """

        #old time metod:
        #self.labeltime.setText(f"Última actualización: {datetime.datetime.utcfromtimestamp(data['time'] - 10800)}")
        #print(datetime.datetime.utcfromtimestamp(data['time']))
        #new time direct from API
        timestamp = data['cripto']['usdt']['timestamp'] - 10800
        #timestamp = values[0]['timestamp'] - 10800
        self.labeltime.setText(f"Última actualización: {datetime.datetime.utcfromtimestamp(timestamp)}")

        #nuevo diccionario con los valores que me interesan        
        dixyDolar = {"blueX":[], "cripto":[], "mep48":[], "cclCI":[]}
        """
        print("datos en usd_values['blue']: ",data['blue'])
        print("datos en usd_values['cripto']['usdt']: ",usd_values['cripto']['usdt'])
        print("datos en usd_values['mep']['al30']: ",usd_values['mep']['al30']['48hs'])
        print("datos en usd_values['ccl']['lede']: ",usd_values['ccl']['lede']['ci'])
        """
        dixyDolar['blueX'].append(data['blue'])
        dixyDolar['cripto'].append(usd_values['cripto']['usdt'])
        dixyDolar['mep48'].append(usd_values['mep']['al30']['48hs'])
        dixyDolar['cclCI'].append(usd_values['ccl']['lede']['ci'])
        #print(dixyDolar)
        df=pd.DataFrame(dixyDolar)
        dft=self.transPanda(df)
        print(dft.to_string(index=True, col_space=5))

        newvalues = [values[0]['ask'],values[1]['ccb']['ask'],values[2]['al30']['48hs']['price'],values[3]['lede']['ci']['price']]
        #print('newvalues list: ', newvalues)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        colors = ['blue', '#FFFF00', '#00FF00', '#FF0000']  # azul, amarillo, verde, rojo
        bars= ax.barh(types, newvalues, color=colors) # Utilizamos barh en lugar de bar #newvalues 19.02.2024

        for i, bar in enumerate(bars):
            x = bar.get_width()
            y = bar.get_y() + bar.get_height() / 2
            ax.text((x-250), y, str(newvalues[i]), ha='left', va='center', weight='bold', size=14) #newvalues 19.02.2024

        self.canvas.draw()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
