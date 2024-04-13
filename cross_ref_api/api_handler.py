import requests 

from functools import singledispatch
from typing import Dict, List
from enum import Enum
from dataclasses import dataclass, field

from utils import utils
from doi_extractor import DoiExtractor
from . import api_validator

class NotValidUrl(Exception):
    pass

class FailedAPIRequest(Exception):
    pass

class UrlException(Enum):
    INVALID_USER_MAIL = 'Invalid user mail'
    INVALID_ENDPOINT = 'Invalid endpoint'
    NETWORK_ERROR = 'Failed API request'

@dataclass(slots=True)
class CrossRefHandler:
    """ CrossRef API handler responsible for handling the crossref api requests
    """
    _url: str = field(default_factory=utils.fetch_url, init=False, repr=False)
    _payload: str  = field(default_factory=utils.fetch_payload, init=False, repr=False)

    def __post_init__(self) -> None:
        self._validate_url()

    def _validate_url(self) -> None:
        validation_functions = (
            (UrlException.INVALID_USER_MAIL, lambda api_instance: api_validator.validate_user_mail(api_instance)),
            (UrlException.INVALID_ENDPOINT, lambda api_instance: api_validator.validate_endpoint(api_instance))
        )

        for exception, validation_func in validation_functions:
            error_flag, error_message = validation_func(self)
            if error_flag:
                raise NotValidUrl('Exception: {}. ErrorMessage: {}'.format(
                    exception.value, 
                    error_message))

    
    def fetch_metadata(self, filter_payload: Dict) -> str:
        response = requests.get(f'{self._url}?mailto={self._payload}', params=filter_payload)
        error_flag = not (error_message:=response.status_code) == 200
        if error_flag:
            raise FailedAPIRequest('Exception: {}. ErrorMessage: {}'.format(
                UrlException.NETWORK_ERROR.value, 
                f'API response:{error_message}'))
        return response.text

    def fetch_single_work(self, doi: str) -> str:
        response = requests.get(f'{self._url}/{doi}')
        error_flag = not (error_message:=response.status_code) == 200
        if error_flag:
            raise FailedAPIRequest('Exception: {}. ErrorMessage: {}'.format(
                UrlException.NETWORK_ERROR.value, 
                f'API response:{error_message}'))
        return response.text



def validate_dois(dois: List | str):
    doi_extractor = DoiExtractor(dois)
    cross_ref_api_instance = CrossRefHandler()
    response_map = {doi: cross_ref_api_instance.fetch_single_work(doi) for doi in doi_extractor.dois}
    print(response_map)
    return response_map