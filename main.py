from cross_ref_api.api_handler import CrossRefHandler 


if __name__ == '__main__':
    api_instance = CrossRefHandler()
    print(api_instance._url)
    print(api_instance.fetch_metadata())