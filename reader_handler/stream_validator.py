from collections import namedtuple

from ..utils import fetch_extension
from .stream_reader import StreamType


ErrorStruct = namedtuple('ErrorStruct', 'error_flag error_message')

def validate_extension(stream_address):
    extension = fetch_extension(stream_address)
    accepted_extensions = [extension for member in StreamType for extension in member.value]
    error_flag = extension not in accepted_extensions
    error_message = f'Expected: {accepted_extensions}. Received: {extension}'
    return ErrorStruct(error_flag, error_message)

def validate_availability(stream_address):
    return True

