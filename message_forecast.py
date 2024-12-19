import datetime

def message_inf(data_day):
    """
    Формирование сообщения о прогнозе погоды на 1 день
    :param data_day: датафрейм с необходимой информацией
    :return: сообщение с прогнозом погоды
    """
    data_day = data_day.to_dict('list')
    return (f"\n"
            f"🗓{data_day['date'][0]}:\n"
            f"🌡️Температура: {data_day["temperature (max)"][0]}C˚\n"
            f"💦Влажность: {data_day["humidity"][0]}%\n"
            f"💨Скорость ветра: {data_day["wind_speed"][0]} м/с\n"
            f"🌧Вероятность осадков: {data_day["precipitation_probability"][0]}%\n")

def forecasts(city, data, days):
    """
    Формирование общего прогноза погоды для 1 города
    :param city: город для прогноза
    :param data: датафрейм с погодными условиями
    :param days: кол-во дней для прогноза
    :return: Прогноз для одного города
    """
    forecast = (f"----------"
                f"\n"
                f"Город {city}\n")
    for i in range(days+1):
        day = datetime.datetime.now().date() + datetime.timedelta(days=i)
        data_day = data[(data['date'] == day) & (data['city'] == city)]
        forecast += message_inf(data_day)
    return forecast



