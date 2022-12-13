from flask import jsonify 

class WeatherData:
    def __init__(
        self,
        place,
        forecast,
        time_updated,
        next_time_updated,
        temp,
        feels_like,
        humidity,
    ):
        self.city = place
        self.weatherForecast = forecast
        self.time_updated = time_updated
        self.next_time_updated = next_time_updated
        self.humidityVal = humidity
        self.temperature = temp
        self.feels_likeVal = feels_like
        
    def create_weather_json(data):
        return jsonify(
        name=data.city,
        weather=data.weatherForecast,
        temp=data.temperature,
        feels_like=data.feels_likeVal,
        humidity=data.humidityVal,
        time_refreshed=data.time_updated,
        next_refresh=data.next_time_updated,
    )
        