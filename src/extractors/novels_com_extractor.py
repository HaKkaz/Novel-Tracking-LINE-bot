import requests
from bs4 import BeautifulSoup
from src.models.classes import Chapter, Novel
from src.extractors.base_extractor import BaseExtractor

novels = [
    Novel(
        name='將門棄婦又震懾邊關了', 
        id='no3a28494c871d48c047dc09fda3a580b25e41f725991777b9df0a2174b3f7286e',
        url='https://www.novels.com.tw/novels/no3a28494c871d48c047dc09fda3a580b25e41f725991777b9df0a2174b3f7286e/',
        website='www.novels.com.tw',
        lastest_chapter=810,
    ),
]
class novels_com_extractor(BaseExtractor):
    def extract_chapters(novel: Novel) -> list[Chapter]:
        if novel.website != 'www.novels.com.tw':
            return []
        novel_id = novel.id
        novel_url = f'https://www.novels.com.tw/novels/{novel_id}/'
        response = requests.get(novel_url)

        soup = BeautifulSoup(response.text, 'lxml')
        ul_all_chapters = soup.find('ul', id='ul_all_chapters')

        chapters = [Chapter(a['href'], a.text) for a in ul_all_chapters.find_all('a')]
        return chapters