from dataclasses import dataclass, field

@dataclass(frozen=True)
class DoiExtractor:
    __slots__ = ('data_chunk', 'dois')

    def __init__(self, data_chunk):
        self.data_chunk: str = data_chunk
        self.dois: set = self.extract_dois()

    def extract_dois(self):
        return set()

    def __hash__(self):
        return hash({doi for doi in self.dois})
    
    def __eq__(self, other):
        if not isinstance(other, DoiExtractor):
            return NotImplemented

        return {doi for doi in self.dois} == {doi for doi in other.dois}

    def __iter__(self):
        return (doi for doi in self.dois)

    def __repr__(self):
        return f'DoiExtractor(dois: {self.dois})'


@dataclass(slots=True)
class DoiManager:
    _doi_extractors: list[DoiExtractor] = field(default_factory=list, init=False, repr=False)

    @property 
    def doi_extractors(self):
        return set(self._doi_extractors)
    
    @doi_extractors.setter
    def doi_extractors(self, doi_extractor):
        if not isinstance(doi_extractor, DoiExtractor):
            raise TypeError(f'Value of wrong type. Expected: DoiExtractor. Received: {type(doi_extractor.__name__)}')
        self._doi_extractors.append(doi_extractor)






