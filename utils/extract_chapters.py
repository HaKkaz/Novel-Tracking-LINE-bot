import requests
from bs4 import BeautifulSoup
from utils.classes import Chapter, Novel, novels

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
    
    
if __name__ == "__main__":
    for novel in novels:
        result = extract_chapters(novel)
        if result:
            print(result[-1])

