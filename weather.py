import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather Report")
        self.city_label = QLabel("Enter the City")
        self.get_weather_button1 = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("70F", self)
        self.city_input = QLineEdit(self)
        self.description_label = QLabel("Sunny", self)
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button1)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.get_weather_button1.setObjectName("get_weather_button1")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button1{
            font-size: 30px;
            font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#description_label{
                font-size: 35px;
            }

        """)

        self.get_weather_button1.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = "90b191ab091006c24619aeb5650080fd"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"    

        try:
            response = requests.get(url)                                                            #when we ask it will giv response
            response.raise_for_status()
            data = response.json()                                                                  #converting response to json file

            if data['cod'] == 200:                                                                            #200 = ok, 404 = error
                self.display_weather(data)

        except requests.exceptions.HTTPError:
            #print(response.status_code)
            match response.status_code:
                case 400:
                    print("Bad Request\nPlease check your input")
                case 401:
                    print("Unauthorized\nInvalid API key")
                case 403:
                    print("Forbidden\nAccess denied")
                case 404:
                    print("Bad Request\nPlease check your input")
                case 500:
                    print("Bad Request\nPlease check your input")
                case 502:
                    print("Bad Request\nPlease check your input")
                case 503:
                    print("Bad Request\nPlease check your input")
                case 400:
                    print("Bad Request\nPlease check your input")

        except requests.exceptions.RequestException:
            pass

    def display_error(self, message):
        pass

    def display_weather(self, data):
        print(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherapp = WeatherApp()
    weatherapp.show()
    sys.exit(app.exec_())