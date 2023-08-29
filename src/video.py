from googleapiclient.discovery import build
import os
import json


class Video:
    api_key = os.getenv("YT_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=video_id
                                                         ).execute()
        self.title = self.video_response["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.viewCount = self.video_response["items"][0]["statistics"]["viewCount"]
        self.viewCount = self.video_response["items"][0]["statistics"]["likeCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео."""
        video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                             id=self.video_id
                                             ).execute()
        print(json.dumps(video, indent=2, ensure_ascii=False))

    def __str__(self):
        return f"{self.title}"


video1 = Video('AWX4JnAnjBE')
video1.print_info()
