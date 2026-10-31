import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather Report")
        self.city_label = QLabel("Enter City Name:")
        self.get_weather_button1 = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.city_input = QLineEdit(self)
        self.description_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button1)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.get_weather_button1.setObjectName("get_weather_button1")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.description_label.setObjectName("description_label")
        self.emoji_label.setObjectName("emoji_label")

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
                font-size: 40px;
                font-style: italic;
            }
            QLabel#emoji_label{
                font-size: 60px;
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

        except requests.exceptions.HTTPError as http_error:
            #print(response.status_code)
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nAccess denied")
                case 404:
                    self.display_error("Not Found\nCity not found")
                case 500:
                    self.display_error("Internal server error\nplease try again later")
                case 502:
                    self.display_error("Bad gateway\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable\nServer is down")
                case 400:
                    self.display_error("Gateway Timeout\nNo response from the server")
                case _:
                    self.display_error("HTTP error occured\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nThe request timed out")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setText(message)
        self.temperature_label.setStyleSheet("font-size: 35px;"
                                             "font-style: italic;")
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        #print(data)
        temperature_k = data["main"]["temp"]                                #data ke andar, main dict ke andar, temp key value
        temperature_c = temperature_k - 273.15
        weather_desc = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]                               #its gonna be number u can see in print(data)

        self.temperature_label.setText(f"{temperature_c:.1f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(f"{weather_desc}")

        self.temperature_label.setStyleSheet("font-size: 60px;"
                                             "font-weight: bold;")

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 771:
            return "-"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return "-"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherapp = WeatherApp()
    weatherapp.show()
    sys.exit(app.exec_())