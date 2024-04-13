import os 
import sys

from collections import namedtuple
from configparser import ConfigParser, ExtendedInterpolation

from ..utils import fetch_extension
from .stream_reader import StreamType

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('./config/config.ini')

ErrorStruct = namedtuple('ErrorStruct', 'error_flag error_message')


def validate_extension(stream_address: str) -> namedtuple:
    extension = fetch_extension(stream_address)
    accepted_extensions = config['VALID_EXTENSIONS']['EXTENSIONS']
    error_flag = extension not in accepted_extensions
    error_message = f'Expected: {accepted_extensions}. Received: {extension}'
    return ErrorStruct(error_flag, error_message)

def validate_availability(stream_address: str) -> namedtuple:
    error_flag = not os.path.exists(stream_address)
    error_message = f'File does not exist. {stream_address}'
    return ErrorStruct(error_flag, error_message)

