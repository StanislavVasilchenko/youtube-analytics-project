from googleapiclient.discovery import build
import os
import json


class Video:
    api_key = os.getenv("YT_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id
        try:
            self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=video_id
                                                             ).execute()
            self.title = self.video_response["items"][0]["snippet"]["title"]
            self.url = f"https://youtu.be/{self.video_id}"
            self.viewCount = self.video_response["items"][0]["statistics"]["viewCount"]
            self.like_count = self.video_response["items"][0]["statistics"]["likeCount"]
        except:
            self.video_response = None
            self.title = None
            self.url = None
            self.viewCount = None
            self.like_count = None

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео."""
        video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.video_id
                                           ).execute()
        print(json.dumps(video, indent=2, ensure_ascii=False))

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id, play_list_id):
        super().__init__(video_id)
        self.play_list_id = play_list_id
        self.url = f"https://www.youtube.com/playlist?list={self.play_list_id}"
