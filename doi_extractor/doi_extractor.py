import re

from dataclasses import dataclass, field
from typing import ClassVar, Pattern

@dataclass(slots=True)
class DoiExtractor:
    """ Extracting dois through regex from datachunk 
        Attributes: data_chunk: str - text stream with text from which dois will be extracted 
                    dois: tuple - extracted dois from text
    """
    regex_pattern: ClassVar[Pattern] = re.compile(r'(10.\d{4,9}/[-._;()/:A-Z0-9]+)', re.IGNORECASE)
    data_chunk: str
    dois: tuple = field(default_factory=tuple, init=False)

    def __post_init__(self):
        self.dois = self.extract_dois()

    def extract_dois(self) -> tuple:
        return tuple(re.findall(DoiExtractor.regex_pattern, self.data_chunk))
    
    def __hash__(self):
        return hash(self.dois)
    
    def __eq__(self, other):
        if not isinstance(other, DoiExtractor):
            return NotImplemented 
        
        return self.dois == other.dois




