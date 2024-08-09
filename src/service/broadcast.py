from src.utils.messaging import broadcast_message
from src.extractors import xyi6_com_extractor
from src.models.classes import Chapter, Novel
from service.config import BROADCAST_INTERVAL
import time
from datetime import datetime


def get_current_time() -> str:
    now = datetime.now()
    formatted_time = now.strftime("%Y/%m/%d %H:%M:%S")
    return formatted_time

def broadcast_updates():
    while True:
        print(f"[{get_current_time()}] Checking for updates...")
        for i in range(len(novels)):
            novel: Novel = novels[i]
            print(f'{novel.name} {novel.lastest_chapter}')
            chapters: list[Chapter] = extract_chapters(novel)

            message = f"{novel.name} 最新章節:\n"
            
            # find first chapter that is newer than the latest chapter
            new_chapters = []
            for i in range(len(chapters) - 1, -1, -1):
                chapter = chapters[i]
                if chapter.number > novel.lastest_chapter: # TODO: operator should be `>`
                    new_chapters.append(chapter)
            
            # if no new chapters, skip to next novel
            if not new_chapters:
                continue
            
            new_chapters = new_chapters[::-1]
            message += '\n'.join(map(str, new_chapters))
            
            novel.lastest_chapter = chapters[-1].number
            broadcast_message(message)

        time.sleep(BROADCAST_INTERVAL)
