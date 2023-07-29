from dotenv import load_dotenv
from .utils.info import Info
from .utils.video import Video
from .utils.episode import Episode

load_dotenv()


class Main:
    def __init__(self) -> None:
        pass

    def get_info(self, slug):
        return Info(slug).to_json()

    def get_video_source(self, slug):
        return Video(slug).get_details()

    def get_episode(self, slug):
        return Episode(slug).get_details()


if __name__ == "__main__":
    main = Main()
    # info = main.get_info("battle-through-the-heavens-season-5/")
    video = main.get_video("perfect-world-episode-03-subtitle-indonesia")
    print(video)
