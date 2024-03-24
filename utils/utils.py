from configparser import ConfigParser, ExtendedInterpolation

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('../config/config.ini')

def fetch_url(endpoint: str):
    pass

def fetch_payload():
    pass