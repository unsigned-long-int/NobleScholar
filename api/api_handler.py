import requests 
import json

from enum import Enum
from dataclasses import dataclass, field

from ..utils import utils
from . import api_validator

class NotValidUrl(Exception):
    pass

class UrlException(Enum):
    INVALID_USER_MAIL = 'Invalid user mail'
    INVALID_ENDPOINT = 'Invalid endpoint'

@dataclass(slots=True)
class CrossRefHandler:
    """ CrossRef API handler responsible for handling the crossref api requests
    """
    _url = utils.fetch_url()
    _payload = utils.fetch_payload()

    @classmethod
    def validate_url(cls):
        validation_functions = (
            (UrlException.INVALID_USER_EMAIL, lambda api_class: api_validator.validate_user_mail(api_class)),
            (UrlException.INAVLID_ENDPOINT, lambda api_class: api_validator.validate_endpoint(api_class))
        )

        for exception, validation_func in validation_functions:
            error_flag, error_name = validation_func(cls)
            if error_flag:
                raise NotValidUrl('Exception: {}. ErrorMessage: {}'.format(
                    exception.value, 
                    error_name))

    def fetch_metadata(self):
        try:
            requests.get(self._url)

