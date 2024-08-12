from src.utils.messaging import broadcast_message
from src.extractors.xyi6_com_extractor import xyi6_com_extractor
from src.extractors.novels_com_extractor import novels_com_extractor
from src.extractors.base_extractor import BaseExtractor as Extractors
from src.models.classes import Chapter, Novel
from src.models.novel_list import novels
from src.service.config import BROADCAST_INTERVAL
from src.utils.logger import service_logger
from src.utils.time import get_current_time

import time

extractors: dict[str, Extractors] = {
    "xyi6.com": xyi6_com_extractor(),
    "www.novels.com.tw": novels_com_extractor(),
}

def broadcast_updates():
    try:
        while True:
            for i in range(len(novels)):
                novel = novels[i]
                service_logger.info(f"Checking for updates for {novel.name}")
                if novel.website not in extractors:
                    service_logger.error(f"Extractor for {novel.website} not found")
                    continue
                chapters: list[Chapter] = extractors[novel.website].extract_chapters(novel)

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

                print(f"[{get_current_time()}] {novel.name} is checking for updates, updated {novel.lastest_chapter} to {new_chapters[-1].number}")
                
                novels[i].lastest_chapter = chapters[-1].number
                broadcast_message(message)

            time.sleep(BROADCAST_INTERVAL)
    except Exception as e:
        service_logger.error(f"Error in broadcast_updates: {e}")
        time.sleep(60)
        broadcast_updates()