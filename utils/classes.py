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
    def __init__(self, href: str, text: str) -> None:
        self.url = f'https://www.mickpk.com{href}'
        self.title = text
        self.number = int(re.search(r'第(\d+)章', text).group(1))
    
    def __str__(self) -> str:
        return f'{self.title} {self.url}'

novels = [
    Novel(
        name='將門棄婦又震懾邊關了小說', 
        id='no3a28494c871d48c047dc09fda3a580b25e41f725991777b9df0a2174b3f7286e',
        url='https://www.novels.com.tw/novels/no3a28494c871d48c047dc09fda3a580b25e41f725991777b9df0a2174b3f7286e/',
        website='www.novels.com.tw',
        lastest_chapter=805,
    ),
]