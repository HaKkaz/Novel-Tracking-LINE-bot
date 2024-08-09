from src.models.classes import Chapter, Novel
from src.extractors.base_extractor import BaseExtractor
from requests.exceptions import RequestException
from src.extractors.logger import logger

import re
import requests
from bs4 import BeautifulSoup

class novels_com_extractor(BaseExtractor):
    def __init__(self) -> None:
        super().__init__()

    def extract_chapters(self, novel: Novel) -> list[Chapter]:
        print('extract_chapters START...') 
        try:
            if isinstance(novel, Novel) == False:
                raise TypeError('novel is not an instance of Novel')
            if novel.website != 'www.novels.com.tw':
                return []
            novel_id = novel.id
            novel_url = f'https://www.novels.com.tw/novels/{novel_id}/'
            response = requests.get(novel_url)
            response.raise_for_status()


            soup = BeautifulSoup(response.text, 'lxml')
            ul_all_chapters = soup.find('ul', id='ul_all_chapters')

            select_result = ul_all_chapters.find_all('a')

            chapters:list[Chapter] = []

            for a in select_result:
                if a.has_attr('href') and a.has_attr('title') and a.text[1:-1].isdigit():
                    url=a['href'], 
                    title=''.join(a['title'].split()[:-1]),
                    number=a.text[1:-1]

                    if isinstance(url[0], str) and \
                        isinstance(title[0], str) and \
                        isinstance(number[0], str):
                        chapters.append(Chapter(url=url[0], title=title[0], number=int(number)))
                else:
                    continue
            return chapters
        except RequestException as e:
            print(f"Network error while extracting chapters from {novel.name}: {e}")
            return []
        except TypeError as e:
            print(f"TypeError in novels_com_extractor.")
            print(e)
            return []
        except Exception as e:
            logger.error(f"Failed to extract chapters from {novel.name} with error: {e}")
            return []