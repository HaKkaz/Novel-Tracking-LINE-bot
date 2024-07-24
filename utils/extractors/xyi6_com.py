import requests
from bs4 import BeautifulSoup
from utils.classes import Chapter, Novel

novels = [
    Novel(
        name='將門棄婦又震懾邊關了', 
        id='5502',
        url='https://xyi6.com/Book/Indexd3/bookshow/bookId/5502.html',
        website='xyi6.com',
        lastest_chapter=830,
    ),
]

def get_last_option_value(html_str):
    soup = BeautifulSoup(html_str, 'lxml')
    options = soup.find_all('option')
    if options:
        return options[-1]['value']
    else:
        return None

def parse_chapters(html_str):
    soup = BeautifulSoup(html_str, 'lxml')
    chapters = []
    li_tags = soup.select('div.mulukaishi ul.ddxx li')

    for li in li_tags:
        a_tag = li.find('a')
        if a_tag:
            chapter_info = a_tag.text.strip()
            href = a_tag['href']
            chapter_number, chapter_title = chapter_info.split(' ', 1)
            chapters.append(
                Chapter(
                    number=int(chapter_number), 
                    title=chapter_title.split()[1], 
                    url='https://xyi6.com/'+href
                )
            )
    
    return chapters

def extract_chapters(novel: Novel) -> list[Chapter]:
    print(type(novel))
    if novel.website != 'xyi6.com':
        return []
    
    url = novel.url

    response = requests.post(url)

    # 找到最後一個 option 的 value
    last_option_value = get_last_option_value(response.text)

    if last_option_value is None:
        return []
    url = 'https://xyi6.com/Book/Indexd3/bookcatalog/bookId/5502.html'
    payload = {'p': last_option_value}

    response = requests.post(url, data=payload)

    chapters = parse_chapters(response.text)

    return chapters

    
