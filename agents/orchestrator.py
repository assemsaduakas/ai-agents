from agents.tool_registry import ToolRegistry
from agents.llm_client import LLMClient

CITY_COORDS = {
    "london": (51.5072, -0.1276),
    "paris": (48.8566, 2.3522),
    "new york": (40.7128, -74.0060),
    "almaty": (43.2389, 76.8897),
    "astana": (51.1694, 71.4491),
    "amsterdam": (52.3676, 4.9041),
}


class AgentOrchestrator:
    def __init__(self, memory):
        self.memory = memory
        self.registry = ToolRegistry()
        self.llm = LLMClient()

    def handle_query(self, user_input: str) -> str:
        # 1️⃣ Ask OpenAI to understand the user
        llm_data = self.llm.parse_user_query(user_input)

        intent = llm_data.get("intent")
        if intent == "unknown":
            return "I can help with weather or news."

        # 2️⃣ Get MCP tool
        tool = self.registry.get_tool_by_intent(intent)
        if not tool:
            return f"No MCP tool available for intent: {intent}"

        # 3️⃣ Build params from LLM output
        try:
            params = self._build_params(intent, llm_data)
            result = tool.execute(params)
        except Exception as e:
            return f"Tool execution failed: {e}"

        # 4️⃣ Format response
        return self._format_response(intent, result)

    def _build_params(self, intent: str, llm_data: dict) -> dict:
        if intent == "weather":
            city = llm_data.get("city") or self.memory.last_location
            if not city:
                raise ValueError("City required for weather")

            self.memory.last_location = city
            lat, lon = CITY_COORDS[city]
            return {"latitude": lat, "longitude": lon}

        if intent == "news":
            topic = llm_data.get("topic") or self.memory.last_topic
            self.memory.last_topic = topic
            return {"topic": topic}

        return {}

    def _format_response(self, intent: str, data: dict) -> str:
        if intent == "weather":
            return (
                f"🌤 Temperature: {data['temperature']}°C\n"
                f"💨 Wind speed: {data['windspeed']} km/h"
            )

        if intent == "news":
            return "\n".join(
                f"📰 {a['title']}" for a in data["articles"]
            )
