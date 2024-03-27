import os

from configparser import ConfigParser, ExtendedInterpolation
from dotenv import load_dotenv

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('./config/config.ini')

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

def fetch_url() -> str:
    return config['API'].get('ENDPOINT')

def fetch_payload() -> str:
    return os.getenv('user_mail')