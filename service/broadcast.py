from utils.messaging import broadcast_message
from utils.extractors.xyi6_com import extract_chapters, novels
from utils.classes import Chapter
from service.config import BROADCAST_INTERVAL
import time

def broadcast_updates():
    while True:
        for i in range(len(novels)):
            novel = novels[i]
            chapters: list[Chapter] = extract_chapters(novel)

            message = f"{novel.name} 最新章節:\n"
            
            # find first chapter that is newer than the latest chapter
            new_chapters = []
            for i in range(len(chapters) - 1, -1, -1):
                chapter = chapters[i]
                if chapter.number > novel.lastest_chapter: # TODO: operator should be `>`
                    new_chapters.append(chapter)
            
            new_chapters = new_chapters[::-1]
            message += '\n'.join(map(str, new_chapters))
            
            novel.lastest_chapter = chapters[-1].number
            broadcast_message(message)

        time.sleep(BROADCAST_INTERVAL)
