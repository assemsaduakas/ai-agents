def detect_intent(user_input: str):
    text = user_input.lower()

    weather_keywords = ["weather", "temperature", "rain", "forecast"]
    news_keywords = ["news", "headline", "latest", "happening"]

    is_weather = any(k in text for k in weather_keywords)
    is_news = any(k in text for k in news_keywords)

    if is_weather and is_news:
        return "both"
    if is_weather:
        return "weather"
    if is_news:
        return "news"

    return "unknown"
