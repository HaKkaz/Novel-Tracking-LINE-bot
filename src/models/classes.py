from dataclasses import dataclass

@dataclass
class Novel:
    name: str
    id: str
    url: str
    website: str
    lastest_chapter: int = 0

@dataclass
class Chapter:
    url: str
    title: str
    number: int
    
    def __str__(self) -> str:
        return f'第{self.number}章 {self.title} {self.url}'

