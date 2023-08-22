import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv("YT_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.subscribers = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return cls.youtube

    def to_json(self, file_name: str) -> None:
        """
        Сохраняет в файл значения атрибутов экземпляра `Channel`
        """
        data = {"channel_id": self.channel_id,
                "title": self.title,
                "description": self.description,
                "video_count": self.video_count,
                "subscribers": self.subscribers,
                "url": self.url

                }
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        if channel_id != self.__channel_id:
            print("Нельзя изменить атрибут")

    def __str__(self):
        return f"{self.title} ({self.url})"
