# Novel-Tracking-LINE-bot

## Overview
Novel Tracking LINE Bot 是一個用於追蹤和管理小說更新的工具，為用戶提供即時的通知和關於他們喜愛小說的資訊。該機器人與各種小說網站互動，提取章節更新和其他相關細節，並將這些信息整合到 LINE 訊息平台中，方便用戶查看和接收通知。

## Features
- **小說追蹤**: 自動追蹤指定小說的更新。
- **LINE 集成**: 通過 LINE 訊息平台向用戶發送更新和通知。
- **可配置**: 支援使用者自行設定小說來源。


## Project Structure
- **`src/extractors/`**: 包含負責從不同小說網站的 html 提取章節資訊的模組，其中 `base_extractor.py` 定義了所有 `extractors` 的抽象類別。

- **`src/models/`**: 定義專案中使用的類別。
  - `classes.py`: 包含 `Chapter` 和 `Novel` 數據模型。

- **`src/service/`**: 包含與 LINE 機器人及其服務相關的模組。
  - `broadcast.py`: 向所有使用者廣播 LINE 聊天室訊息。
  - `command.py`: 使用者在聊天室向機器人發送的指令。
  - `config.py`: 管理服務的基本設定。

- **`src/utils/`**: 包含專案中使用的實用功能。
  - `messaging.py`: 包裝過後的函數，方便開發者使用。

```
.
├── README.md
├── app.py
├── requirements.txt
└── src
    ├── extractors
    ├── models
    ├── service
    ├── test
    └── utils
```