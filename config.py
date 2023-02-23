# Copyright (c) 2023 EDM115
import os


class Config:
    APP_ID = int(17983098)
    API_HASH = "ee28199396e0925f1f44d945ac174f64"
    BOT_TOKEN = "5998737564:AAH19LlVDCRzXYv0T6UDgEDL36wwmwUxNGc"
    LOGS_CHANNEL = int(-1001694045459)
    MONGODB_URL = "mongodb+srv://Bala7a19871:Ibntaymya1.@cluster0.5mtsc.mongodb.net/?retryWrites=true&w=majority"
    BOT_OWNER = int(6234365091)
    DOWNLOAD_LOCATION = f"{os.path.dirname(__file__)}/Downloaded"
    THUMB_LOCATION = f"{os.path.dirname(__file__)}/Thumbnails"
    TG_MAX_SIZE = 2040108421
    # Default chunk size (0.005 MB → 1024*6) Increase if you need faster downloads
    CHUNK_SIZE = 1024 * 6
    BOT_THUMB = f"{os.path.dirname(__file__)}/bot_thumb.jpg"
