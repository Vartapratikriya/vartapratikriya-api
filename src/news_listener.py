import os
import json
import requests
import datetime

from dotenv import load_dotenv

from tqdm import tqdm
from typing import List, Dict


def load_config(config_file_path):
    try:
        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print(f"Config file not found at {config_file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON in {config_file_path}: {e}")
        return None


class NewsListener:
    def __init__(
        self,
        key: str,
        domains: List[str],
    ) -> None:
        self._key = key
        self.domains = domains
        self.keywords = [
            "sports",
            "healthcare",
            "business",
            "media",
            "laws",
            "entertainment",
            "weather",
            "policy",
        ]
        self.date = datetime.datetime.now().date().strftime("%y-%m-%d")
        self.url = (
            f"https://newsapi.org/v2/everything?from={self.date}&apiKey={self._key}"
        )

    def get_headlines(self) -> Dict:
        print("Getting headlines...")
        articles = []
        for domain in tqdm(self.domains):
            articles.extend(
                requests.get(self.url + f"&domains={domain}").json()["articles"]
            )
        return {
            "news_listener": "v0.1.0",
            "generated_at": str(datetime.datetime.now()),
            "articles": articles,
        }

    def get_keywords(self) -> Dict:
        print("Getting relevant articles...")
        articles = {}
        for keyword in tqdm(self.keywords):
            articles[keyword] = requests.get(
                self.url + f"&domains={','.join(self.domains)}" + f"&q={keyword}"
            ).json()["articles"]

        return {
            "news_listener": "v0.1.0",
            "scraped_at": str(datetime.datetime.now()),
            "articles": articles,
        }


if __name__ == "__main__":
    load_dotenv()
    config = load_config("./config.json")
    nL = NewsListener(key=os.getenv("NEWS_API_KEY"), domains=config["outlets"])

    with open("/data/dump_headlines.json", "w") as json_file:
        json.dump(nL.get_headlines(), json_file, indent=4, ensure_ascii=False)

    with open("/data/dump_categories.json", "w") as json_file:
        json.dump(nL.get_keywords(), json_file, indent=4, ensure_ascii=False)
