from dataclasses import dataclass
import re

@dataclass
class Novel:
    name: str
    id: str
    url: str
    website: str
    lastest_chapter: int = 0

class Chapter:
    def __init__(self, url: str, title: str, number: int) -> None:
        self.url = url
        self.title = title
        self.number = number
    
    def __str__(self) -> str:
        return f'第{self.number}章 {self.title} {self.url}'

