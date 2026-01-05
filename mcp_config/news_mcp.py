import requests
from mcp_config.base_mcp import BaseMCPTool

class NewsMCP(BaseMCPTool):
    def execute(self, params: dict) -> dict:
        response = requests.get(
            "https://api.thenewsapi.com/v1/news/top",
            params={
                "locale": "us",
                "limit": 5,
                "search": params.get("topic"),
                "api_token": "XMzBMjX2d9rQU19vWxOhBZkMyKEqqHOjwXsiWjFO"
            },
            timeout=10
        )
        response.raise_for_status()

        articles = response.json().get("data", [])
        return {
            "articles": [
                {"title": a["title"], "url": a["url"] + "\n"}
                for a in articles
            ]
        }
