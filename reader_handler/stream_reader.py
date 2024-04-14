import os

from functools import singledispatchmethod
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Any
from configparser import ConfigParser, ExtendedInterpolation
from enum import Enum, auto


from doi_extractor import DoiExtractor
from .file import File

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('./config/config.ini')

class StreamType(Enum):
    """ Types of data streams supported
    """
    DOC = auto()
    PDF = auto()
    PPT = auto()
    TXT = auto()

class StreamExceptions(Enum):
    """ Stream exceptions
    """
    INVALID_EXTENSION = 'Extension is not valid.'
    MISSING_FILE = 'File is missing.'

class InvalidStream(Exception):
    pass

class StreamReader(ABC):
    """ Reader interface responsible for reading stream and fetching DocExtractor instances
        Attributes: file: File - file object
                    _doi_extractors: list[DoiExtractor] - list of doc extractors 
    """
    __slots__ = ('file', '_doi_extractors')
    def __init__(self, file: File):
        self.file: File = file
        self._doi_extractors: list[DoiExtractor] = []

    @abstractmethod
    def fetch_doi_extractors(self, file: File):
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

    def fetch_doi_extractors(self):
        data = self.file.read_file()
        self._doi_extractors.append(DoiExtractor(data_chunk=data))

class StreamReaderGen(StreamReader):
    """ Polymorphic implementation inheriting from StreamReader interface. 
        Responsible for sequential generator reading streams. 
        Attributes: (see StreamReader) 
    """
    __slots__ = ()

    def fetch_doi_extractors(self):
        self._doi_extractors = [DoiExtractor(data_chunk=data) for data in self.file.gen_read_binary()]

@dataclass(slots=True)
class StreamManager:
    max_chunk_size: ClassVar[int] = config['READER']['MAX_CHUNK_SIZE']
    file: File
    _stream_size: int = field(default=None, repr=False, init=False)
    stream_reader_instance: StreamReaderGen | StreamReaderBulk = field(default=None)

    def __post_init__(self):
        self._stream_size = self._fetch_stream_size()
        stream_reader_ptr = self._fetch_stream_reader()
        self.stream_reader_instance = stream_reader_ptr(self.file)
            
    def _fetch_stream_size(self):
        return os.path.getsize(self.file.file_address)
        
    def _fetch_stream_reader(self):
        if self._stream_size > StreamManager.max_chunk_size:
            return StreamReaderGen 
        return StreamReaderBulk


