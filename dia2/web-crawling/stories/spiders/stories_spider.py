import scrapy
import json
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

NY_API_KEY = ""

class StoriesSpider(scrapy.Spider):
    name = "stories"
    allowed_domains = ["api.nytimes.com"]

    def start_requests(self):
        urls = [
            f"https://api.nytimes.com/svc/topstories/v2/arts.json?api-key={NY_API_KEY}",
            f"https://api.nytimes.com/svc/topstories/v2/home.json?api-key={NY_API_KEY}",
            f"https://api.nytimes.com/svc/topstories/v2/science.json?api-key={NY_API_KEY}",
            f"https://api.nytimes.com/svc/topstories/v2/us.json?api-key={NY_API_KEY}",
            f"https://api.nytimes.com/svc/topstories/v2/world.json?api-key={NY_API_KEY}",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Extrai o último trecho da URL (ex: arts.json, science.json)
        endpoint = response.url.split("/")[-1].split("?")[0] or "index"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{endpoint}_{timestamp}.json"

        try:
            # Converte para dict Python
            data = json.loads(response.text)
        except Exception as e:
            self.logger.error(f"Erro ao decodificar JSON de {response.url}: {e}")
            return

        # Salva arquivo local
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.logger.info(f"✅ Dados salvos em {filename}")