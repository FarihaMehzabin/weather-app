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
        
    def create_weather_json(self):
        return jsonify(
        name=self.city,
        weather=self.weatherForecast,
        temp=self.temperature,
        feels_like=self.feels_likeVal,
        humidity=self.humidityVal,
        time_refreshed=self.time_updated,
        next_refresh=self.next_time_updated,
    )
        