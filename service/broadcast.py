from utils.messaging import broadcast_message
from utils.extract_chapters import extract_chapters
from utils.classes import novels
from service.config import BROADCAST_INTERVAL
import time

def broadcast_updates():
    while True:
        for i in range(len(novels)):
            novel = novels[i]
            if novel.website != 'www.novels.com.tw':
                continue
            chapters = extract_chapters(novel)

            message = f"{novel.name} 最新章節:\n"
            
            # find first chapter that is newer than the latest chapter
            j = 0
            for i in range(len(chapters) - 1, -1, -1):
                chapter = chapters[i]
                if chapter.number > novel.lastest_chapter: # TODO: operator should be `>`
                    j = i
            
            for i in range(j, len(chapters)):
                message += f'{chapters[i]}\n'
            
            novel.lastest_chapter = chapters[-1].number
            broadcast_message(message)

        time.sleep(BROADCAST_INTERVAL)
