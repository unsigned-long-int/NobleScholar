from ..reader_handler import StreamManager


def extract_doi(file_path, **kwargs):
    stream_manager_instance = StreamManager(stream_address=file_path)
    stream_reader_instance = stream_manager_instance.stream_instance
    stream_reader_instance.fetch_doi_extractors()
    return stream_reader_instance.dois

def validate_doi(file_path, **kwargs):
    stream_manager_instance = StreamManager(stream_address=file_path)
    stream_reader_instance = stream_manager_instance.stream_instance
    stream_reader_instance.fetch_doi_extractors()
    
    return stream_reader_instance.dois
