from src.utils.messaging import broadcast_message
from src.extractors.xyi6_com_extractor import xyi6_com_extractor
from src.extractors.novels_com_extractor import novels_com_extractor
from src.extractors.base_extractor import BaseExtractor as Extractors
from src.models.classes import Chapter, Novel
from src.models.novel_list import novels
from src.service.config import BROADCAST_INTERVAL
from src.service.logger import logger

import time
from datetime import datetime

extractors: dict[str, Extractors] = {
    "xyi6.com": xyi6_com_extractor(),
    "www.novels.com.tw": novels_com_extractor(),
}

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

            if novel.website not in extractors:
                logger.error(f"Extractor for {novel.website} not found")
                continue
            chapters: list[Chapter] = extractors[novel.url].extract_chapters(novel)

            message = f"{novel.name} 最新章節:\n"
            
            # find first chapter that is newer than the latest chapter
            new_chapters = []
            for i in range(len(chapters) - 1, -1, -1):
                chapter = chapters[i]
                if chapter.number > novel.lastest_chapter:
                    new_chapters.append(chapter)
            
            # if no new chapters, skip to next novel
            if not new_chapters:
                continue
            
            new_chapters = new_chapters[::-1]
            message += '\n'.join(map(str, new_chapters))
            
            novel.lastest_chapter = chapters[-1].number
            broadcast_message(message)

        time.sleep(BROADCAST_INTERVAL)
