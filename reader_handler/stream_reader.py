import os

from functools import singledispatchmethod
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar
from configparser import ConfigParser, ExtendedInterpolation
from enum import Enum, auto


from ..doi_extractor import DoiExtractor
from .content_streamer_bulk import (
    read_doc, 
    read_pdf, 
    read_ppt, 
    read_txt
    )
from .binary_streamer_gen import read_file
import stream_validator

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('./config/config.ini')

class StreamType(Enum):
    """ Types of data streams supported
    """
    DOC = ('doc', 'docx')
    PDF = ('pdf',)
    PPT = ('ppt', 'pptx')
    TXT = ('txt',)

class StreamExceptions(Enum):
    """ Stream exceptions
    """
    INVALID_EXTENSION = 'Extension is not valid.'
    MISSING_FILE = 'File is missing.'

class InvalidStream(Exception):
    pass

class StreamReader(ABC):
    """ Reader interface responsible for reading stream and fetching DocExtractor instances
        Attributes: stream_address: str - address of the file endpoint for which doc extractors should be fetched
                    _doi_extractors: list[DoiExtractor] - list of doc extractors 
    """
    __slots__ = ('stream_address', '_doi_extractors')
    def __init__(self, stream_address):
        self.stream_address: str = stream_address
        self._doi_extractors: list[DoiExtractor] = []

    @abstractmethod
    def fetch_doi_extractors(self, stream_type):
        raise NotImplementedError
    
    @property 
    def dois(self):
        return {doi for doi_extractor in self._doi_extractors for doi in doi_extractor.dois}
    
class StreamReaderBulk(StreamReader):
    """ Polymorphic implementation inheriting from StreamReader interface. 
        Responsible for bulk reading streams. 
        Attributes: (see StreamReader) 
    """
    __slots__ = ()
    @singledispatchmethod
    def fetch_doi_extractors(self, stream_type):
        raise NotImplementedError
    
    @fetch_doi_extractors.register 
    def _(self, stream_type: StreamType.DOC):
        data = read_doc(self.stream_address)
        self._doi_extractors.append(DoiExtractor(data_chunk=data))

    @fetch_doi_extractors.register
    def _(self, stream_type: StreamType.PDF):
        data = read_pdf(self.stream_address)
        self._doi_extractors.append(DoiExtractor(data_chunk=data))

    @fetch_doi_extractors.register 
    def _(self, stream_type: StreamType.PPT):
        data = read_ppt(self.stream_address)
        self._doi_extractors.append(DoiExtractor(data_chunk=data))

    @fetch_doi_extractors.register
    def _(self, stream_type: StreamType.TXT):
        data = read_txt(self.stream_address)
        self._doi_extractors.append(DoiExtractor(data_chunk=data))

class StreamReaderGen(StreamReader):
    """ Polymorphic implementation inheriting from StreamReader interface. 
        Responsible for sequential generator reading streams. 
        Attributes: (see StreamReader) 
    """
    __slots__ = ()
    @singledispatchmethod
    def fetch_doi_extractors(self, stream_type):
        raise NotImplementedError
    
    @fetch_doi_extractors.register 
    def _(self, stream_type: StreamType.DOC | StreamType.PDF | StreamType.PPT | StreamType.TXT):
        self._doi_extractors = [DoiExtractor(data_chunk=data) for data in read_file(self.stream_address)]

@dataclass(slots=True)
class StreamManager:
    max_chunk_size: ClassVar[int] = config['READER']['MAX_CHUNK_SIZE']
    stream_address: str
    _stream_size: int = field(default=None, repr=False, init=False)
    stream_reader_instance: StreamReaderGen | StreamReaderBulk = field(default=None)

    def __post_init__(self):
        self._validate_stream()
        self._stream_size = self._fetch_stream_size()
        stream_reader_ptr = self._fetch_stream_reader()
        self.stream_reader_instance = stream_reader_ptr(self.stream_address)

    def _validate_stream(self):
        validation_functions = (
            (StreamExceptions.INVALID_EXTENSION, lambda stream_address: stream_validator.validate_extension(stream_address)),
            (StreamExceptions.MISSING_FILE, lambda stream_address: stream_validator.validate_availability(stream_address))
            )
        for exception, validation_func in validation_functions:
            error_flag, error_message = validation_func(self.stream_address)
            if error_flag:
                raise InvalidStream('Exception: {}. ErrorMessage: {}'.format(
                    exception.value, 
                    error_message))
            
    def _fetch_stream_size(self):
        return os.path.getsize(self.stream_address)
        
    def _fetch_stream_reader(self):
        if self._stream_size > StreamManager.max_chunk_size:
            return StreamReaderGen 
        return StreamReaderBulk


