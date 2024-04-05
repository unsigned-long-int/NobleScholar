from functools import singledispatchmethod
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar
from configparser import ConfigParser, ExtendedInterpolation
from enum import Enum, auto

from ..doi_extractor import DoiExtractor

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('./config/config.ini')

class StreamType(Enum):
    """ Types of data streams supported
    """
    DOC = auto()
    PDF = auto()
    PPT = auto()

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
    def fetch_doi_extractor(self, stream_type):
        raise NotImplementedError
    
    @property 
    def doi_extractors(self):
        return {doi for doi_extractor in self._doi_extractors for doi in doi_extractor.dois}
    
class StreamReaderBulk(StreamReader):
    """ Polymorphic implementation inheriting from StreamReader interface. 
        Responsible for bulk reading streams. 
        Attributes: (see StreamReader) 
    """
    @singledispatchmethod
    def fetch_doi_extractor(self, stream_type):
        raise NotImplementedError
    
    @fetch_doi_extractor.register 
    def _(self, stream_type: StreamType.DOC):
        data = read_doc(self.stream_address)
        self._doi_extractors.append(DoiExtractor(data_chunk=data))

    @fetch_doi_extractor.register
    def _(self, stream_type: StreamType.PDF):
        data = read_pdf(self.stream_address)
        self._doi_extractors.append(DoiExtractor(data_chunk=data))

    @fetch_doi_extractor.register 
    def _(self, stream_type: StreamType.PPT):
        data = read_ppt(self.stream_address)
        self._doi_extractors.append(DoiExtractor(data_chunk=data))

class StreamReaderGen(StreamReader):
    """ Polymorphic implementation inheriting from StreamReader interface. 
        Responsible for sequential generator reading streams. 
        Attributes: (see StreamReader) 
    """
    @singledispatchmethod
    def fetch_doi_extractor(self, stream_type):
        raise NotImplementedError
    
    @fetch_doi_extractor.register 
    def _(self, stream_type: StreamType.DOC):
        pass 

    @fetch_doi_extractor.register
    def _(self, stream_type: StreamType.PDF):
        pass 

    @fetch_doi_extractor.register 
    def _(self, stream_type: StreamType.PPT):
        pass


@dataclass(slots=True)
class StreamManager:
    max_chunk_size: ClassVar[int] = config['READER']['MAX_CHUNK_SIZE']
    chunk_size: int 
    stream_address: str
    stream_instance: StreamReaderGen | StreamReaderBulk = field(default=None)

    def __post_init__(self):
        stream_reader_ptr = self._fetch_stream_reader()
        self.stream_instance = stream_reader_ptr(self.stream_address)
        
    def _fetch_stream_reader(self):
        if self.chunk_size > StreamManager.max_chunk_size:
            return StreamReaderGen 
        return StreamReaderBulk


