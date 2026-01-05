import requests
from mcp_config.base_mcp import BaseMCPTool

class WeatherMCP(BaseMCPTool):
    def execute(self, params: dict) -> dict:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": params["latitude"],
                "longitude": params["longitude"],
                "current_weather": True
            },
            timeout=10
        )
        response.raise_for_status()

        weather = response.json()["current_weather"]
        return {
            "temperature": weather["temperature"],
            "windspeed": weather["windspeed"]
        }
