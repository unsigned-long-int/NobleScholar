from typing import List 

from doi_extractor import DoiExtractor
from cross_ref_api import CrossRefHandler

def validate_dois(dois: List | str):
    doi_extractor = DoiExtractor(dois)
    cross_ref_api_instance = CrossRefHandler()
    response_map = {doi: cross_ref_api_instance.fetch_single_work(doi) for doi in doi_extractor.dois}
    print(response_map)
    return response_map