import json
from pathlib import Path
from mcp_config.weather_mcp import WeatherMCP
from mcp_config.news_mcp import NewsMCP

class ToolRegistry:
    def __init__(self):
        self.tools = {}

        self._register_tool("mcp_config/weather_schema.json", WeatherMCP)
        self._register_tool("mcp_config/news_schema.json", NewsMCP)

    def _register_tool(self, schema_path: str, tool_class):
        schema = json.loads(Path(schema_path).read_text())
        tool = tool_class(schema)
        self.tools[schema["intent"]] = tool

    def get_tool_by_intent(self, intent: str):
        return self.tools.get(intent)
