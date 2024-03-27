import re
import requests

from collections import namedtuple

ErrorStruct = namedtuple('ErrorStruct', 'error_flag error_message')

def validate_user_mail(api_instance: 'CrossRefHandler'):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    error_flag = not re.fullmatch(pattern, api_instance._payload)
    error_message = f'Not valid email.'
    return ErrorStruct(error_flag, error_message)

def validate_endpoint(api_instance: 'CrossRefHandler'):
    response = requests.get(f'{api_instance._url}{api_instance._payload}')
    error_flag = not (error_message:=response.status_code) == 200
    return ErrorStruct(error_flag, error_message)