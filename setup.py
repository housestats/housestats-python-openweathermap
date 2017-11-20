from setuptools import setup, find_packages

setup(
    name='housestats-python-owm',
    version='0.1',
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    description='sensor for owm',
    license='GPLv3',
    url='https://github.com/larsks/housestats-python-owm',
    packages=find_packages(),
    entry_points={
        'housestats.sensor': [
            'owm=housestats_python_owm.sensor:OpenWeatherMapSensor',
        ],
    }
)
