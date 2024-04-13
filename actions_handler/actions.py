from typing import List, Dict

from doi_extractor import DoiExtractor
from cross_ref_api import CrossRefHandler

def validate_dois(dois: List | str) -> Dict:
    doi_extractor = DoiExtractor(dois)
    cross_ref_api_instance = CrossRefHandler()
    response_map = {doi: cross_ref_api_instance.fetch_single_work(doi)['message']['update-to'] for doi in doi_extractor.dois}
    return response_map

def extract_dois(stream: 'StreamReader') -> List:
    return stream.dois

def validate_file(stream: 'StreamReader') -> Dict:
    cross_ref_api_instance = CrossRefHandler()
    response_map = {doi: cross_ref_api_instance.fetch_single_work(doi)['message']['update-to'] for doi in stream.dois}
    return response_map

