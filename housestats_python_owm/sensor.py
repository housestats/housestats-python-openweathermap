import logging
import requests

from housestats.metric import Metric
from housestats.sensor.base import BaseSensor

LOG = logging.getLogger(__name__)


class OpenWeatherMapSensor(BaseSensor):
    sensor_type = 'owm'
    current_weather_url = ('http://api.openweathermap.org/data/2.5/weather?'
                           'id={city_id}&appid={api_key}&units=metric')

    def __init__(self, config):
        super().__init__(config)

    def sample(self):
        url = self.current_weather_url.format(
            city_id=self.config['id'],
            api_key=self.config['api_key'])
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        tags = dict(
            longitude=data['coord']['lon'],
            latitude=data['coord']['lat'],
            city_name=data['name'],
            city_id=data['id']
        )

        sample = {k: v for k, v in data['main'].items()}
        sample.update({'wind_{}'.format(k): v
                       for k, v in data['wind'].items()})

        return (tags, sample)

    def fetch(self):
        sample = self.sample()
        LOG.debug('sample = %s', sample)

        tags = sample[0]
        tags.update(self.config.get('tags', {}))

        return [Metric.load(dict(
            sensor_type=self.sensor_type,
            sensor_id=str(self.config['id']),
            tags=tags,
            fields=sample[1]
        ))]
