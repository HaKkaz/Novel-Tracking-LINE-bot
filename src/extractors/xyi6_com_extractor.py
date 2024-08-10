import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from src.models.classes import Chapter, Novel
from src.extractors.base_extractor import BaseExtractor
from src.utils.logger import service_logger

class xyi6_com_extractor(BaseExtractor):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_last_option_value(html: str):
        soup = BeautifulSoup(html, 'lxml')
        options = soup.find_all('option')
        if options:
            return options[-1]['value']
        else:
            return None

    @staticmethod
    def html_parser(html: str) -> list[Chapter]:
        soup = BeautifulSoup(html, 'lxml')
        chapters = []
        li_tags = soup.select('div.mulukaishi ul.ddxx li')

        for li in li_tags:
            a_tag = li.find('a')
            if a_tag:
                chapter_info = a_tag.text.strip()
                href = a_tag['href']
                chapter_info = chapter_info.split(' ', 1)

                
                chapter_number = chapter_info[0] if chapter_info else 0
                chapter_title = chapter_info[1] if len(chapter_info) > 1 else ''

                chapters.append(
                    Chapter(
                        number=int(chapter_number), 
                        title=chapter_title,
                        url='https://xyi6.com'+ href
                    )
                )
        
        return chapters

    def extract_chapters(self, novel: Novel) -> list[Chapter]:
        try:
            if not isinstance(novel, Novel):
                raise TypeError(f"Expected novel to be of type Novel, got {type(novel).__name__} instead.")
            if novel.website != 'xyi6.com':
                raise ValueError(f"Expected novel website to be 'xyi6.com', got {novel.website} instead.")
            response = requests.post(novel.url)
            response.raise_for_status()  # Raise HTTPError for bad responses

            # 找到最後一個 option 的 value
            last_option_value = self.get_last_option_value(response.text)

            if last_option_value is None:
                raise ValueError(f"Failed to extract last option value from {novel.name}")
            
            url = f'https://xyi6.com/Book/Indexd3/bookcatalog/bookId/{novel.id}.html'
            payload = {'p': last_option_value}
            response = requests.post(url, data=payload)
            response.raise_for_status()  # Raise HTTPError for bad responses
            
            chapters = self.html_parser(response.text)

            return chapters
        except RequestException as e:
            service_logger.error(f"Network error while extracting chapters from {novel.name}: {e}")
            return []
        except TypeError as e:
            service_logger.error(f"TypeError in xyi6_com_extractor.")
            return []
        except Exception as e:
            service_logger.error(f"Failed to extract chapters from {novel.name} with error: {e}")
            return []