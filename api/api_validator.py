import validators

from collections import namedtuple

ErrorStruct = namedtuple('ErrorStruct', 'error_flag error_message')

def validate_user_mail(api_instance: 'CrossRefHandler'):
    error_flag = not validators.email(api_instance._payload)
    error_message = 'Not valid email.'
    return ErrorStruct(error_flag, error_message)

def validate_endpoint(api_instance: 'CrossRefHandler'):
    error_flag = not validators.url(api_instance._url)
    error_message = 'Not valid url.'
    return ErrorStruct(error_flag, error_message)