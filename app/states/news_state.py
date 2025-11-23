import reflex as rx
import os
from google import genai
from google.genai import types
import logging
import json


class NewsState(rx.State):
    """State for the Sports News feature."""

    news_items: list[dict[str, str]] = []
    selected_category: str = "All Sports"
    is_loading: bool = False
    error_message: str = ""
    categories: list[str] = [
        "All Sports",
        "Basketball",
        "Football",
        "Soccer",
        "Tennis",
        "Baseball",
        "Formula 1",
    ]

    @rx.event
    async def fetch_news(self):
        """Fetch news using Gemini with Search Grounding."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.error_message = "Google API Key not found."
            return
        self.is_loading = True
        self.error_message = ""
        self.news_items = []
        yield
        try:
            client = genai.Client(api_key=api_key)
            category_prompt = (
                f"for {self.selected_category}"
                if self.selected_category != "All Sports"
                else "for major global sports"
            )
            prompt = f'\n            Find the top 6 latest and most important news headlines {category_prompt} from the last 24 hours.\n            Return the results as a JSON array of objects. \n            Each object must have the following keys: \n            - "title": The headline\n            - "summary": A brief 1-sentence summary\n            - "source": The news source name (e.g. ESPN, BBC)\n            - "time": Relative time (e.g. "2 hours ago")\n            \n            Ensure the response is a valid JSON array. Do not include any text outside the JSON.\n            '
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                ),
            )
            if response.text:
                try:
                    text = response.text.strip()
                    if text.startswith(""):
                        text = text[7:]
                    elif text.startswith(""):
                        text = text[3:]
                    if text.endswith(""):
                        text = text[:-3]
                    text = text.strip()
                    data = json.loads(text)
                    if isinstance(data, list):
                        self.news_items = data
                    elif isinstance(data, dict):
                        items_found = False
                        for key, value in data.items():
                            if isinstance(value, list):
                                self.news_items = value
                                items_found = True
                                break
                        if not items_found and "news" in data:
                            self.news_items = data.get("news", [])
                    else:
                        logging.warning(f"Unexpected JSON format: {data}")
                        self.error_message = "Received unexpected news format."
                except json.JSONDecodeError:
                    logging.exception(f"Failed to parse JSON: {response.text}")
                    self.error_message = "Failed to format news data."
            else:
                self.error_message = "No news found."
        except Exception as e:
            logging.exception(f"News Fetch Error: {e}")
            self.error_message = f"Could not fetch news: {str(e)}"
        finally:
            self.is_loading = False

    @rx.event
    def set_category(self, category: str):
        self.selected_category = category
        return NewsState.fetch_news

    @rx.event
    def on_mount(self):
        """Load initial news."""
        return NewsState.fetch_news