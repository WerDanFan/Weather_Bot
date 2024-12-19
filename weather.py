import pandas as pd
import requests
import datetime

def check_bad_weather(temperature_min, temperature_max, humidity, wind_speed, precipitation_probability):
    """
    Логика для проверки погоды на благоприятность
    :param temperature_min: Минимальная температура
    :param temperature_max: Максимальная температура
    :param humidity: Влажность
    :param wind_speed: Скорость ветра
    :param precipitation_probability: Вероятность осадков
    :return: Благоприятные\Неблагоприятные погодные условия
    """
    flag = True
    if temperature_max > 35 or temperature_min < -15:
        flag = False
    if humidity > 90:
        flag = False
    if wind_speed > 15:
        flag = False
    if precipitation_probability > 70:
        flag = False

    if flag:
        return "Благоприятные погодные условия"
    else:
        return "Неблагоприятные погодные условия"


def date_parser(date):
    """
    Изменяет формат даты
    :param date: дата в исходном формате
    :return: дату вида YYYY-MM-DD типа datetime
    """
    dt_object = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
    date_only = dt_object.date()
    return date_only

class Weather:

    api_key = 'l3LC5vveUNQo1Y0hCGjZwIxTpiGVoxLw' #Ключ для AccuWeather


    def __init__(self):
        self.all_forecasts = pd.DataFrame(columns=['city', 'date', 'temperature (max)','temperature (min)', 'humidity', 'wind_speed', 'precipitation_probability', 'good/bad', 'lat', 'lon'])
        self.all_cords = {}
        self.all_keys = {}

    def get_keys_and_cords(self, cities):
        """
        Получение ключей и координат для каждого города
        :param cities:
        """
        for city in cities:
            if city in self.all_keys:
                pass

            else:
                location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={self.api_key}&q={city}"
                response = requests.get(location_url)
                data = response.json()

                if data:
                    if response.status_code == 200:
                        key = data[0]["Key"]
                        lat = data[0]["GeoPosition"]["Latitude"]
                        lon = data[0]["GeoPosition"]["Longitude"]

                        self.all_keys[city] = key
                        self.all_cords[city] = [lat,lon]

                    elif response.status_code == 403:
                        raise Exception("Упс. Неверный API key")
                    elif response.status_code == 503:
                        raise Exception("Упс. Закончились запросы API. Попробуйте позже.")
                    else:
                        raise Exception(f"Произошла ошибка на сервере {response.status_code}")

                else:
                    raise Exception(f"Упс. Неверно введён один из городов: {city}\n"
                                    f"Пожалуйста повторите ввод.")


    def add_forecasts_in_all_forecasts(self, cities):
        """
        Добавляет прогноз в общий датафрейм для последующего анализа
        :param cities: Города для прогноза погоды
        """
        for city in cities:
            if city in self.all_forecasts['city'].unique():
                pass

            else:
                weather_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{self.all_keys[city]}?apikey={self.api_key}&details=true&metric=true"
                response = requests.get(weather_url)
                data = response.json()

                if data:
                    if response.status_code == 200:

                        for i in range(5):
                            date = date_parser(data["DailyForecasts"][i]["Date"])
                            temperature_min = data["DailyForecasts"][i]["Temperature"]["Minimum"]["Value"]
                            temperature_max = data["DailyForecasts"][i]["Temperature"]["Maximum"]["Value"]
                            humidity = data["DailyForecasts"][i]["Day"]["RelativeHumidity"]["Average"]
                            wind_speed = data["DailyForecasts"][i]["Day"]["Wind"]["Speed"]["Value"]
                            precipitation_probability = data["DailyForecasts"][i]["Day"]["PrecipitationProbability"]
                            lat = self.all_cords[city][0]
                            lon = self.all_cords[city][1]

                            row = {'city': city,
                                   'date': date,
                                   'temperature (max)': temperature_min,
                                   'temperature (min)': temperature_max,
                                   'humidity': humidity,
                                   'wind_speed': wind_speed,
                                   'precipitation_probability': precipitation_probability,
                                   'good/bad': check_bad_weather(temperature_min,
                                                                 temperature_max,
                                                                 humidity,
                                                                 wind_speed,
                                                                 precipitation_probability),
                                   'lat': lat,
                                   'lon': lon}

                            self.all_forecasts.loc[len(self.all_forecasts)] = row


                    elif response.status_code == 403:
                        raise Exception("Упс. Неверный API key")
                    elif response.status_code == 503:
                        raise Exception("Упс. Закончились запросы API. Попробуйте позже.")
                    else:
                        raise Exception(f"Произошла ошибка на сервере {response.status_code}")
                else:
                    raise Exception("Пустая data при вызове погоды")


    def filter(self,cities):
        """
        Фильтр для выделения из датафрейма необходимых строк
        :param cities: Города для которых нужен прогноз
        :return: Датафрейм с необходимыми городами
        """
        df = self.all_forecasts[self.all_forecasts['city'].isin(cities)]
        return df

    def get_df(self,cities):
        """
        Основной код, для получения датафрейма
        :param cities:
        :return: Есть ли ошибка, Датафрейм(или Сущность ошибки)
        """
        error_bool = False
        try:
            self.get_keys_and_cords(cities)
            self.add_forecasts_in_all_forecasts(cities)
            df = self.filter(cities)
            return error_bool, df

        except Exception as e:
            error_bool = True
            return error_bool, str(e)