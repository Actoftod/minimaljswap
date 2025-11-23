import reflex as rx
from app.pages.landing import landing_page
from app.pages.jersey_swap import jersey_swap_page
from app.pages.image_gen import image_gen_page
from app.pages.ai_coach import ai_coach_page
from app.pages.photo_analysis import photo_analysis_page
from app.pages.news import news_page
from app.states.news_state import NewsState

app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap"
    ],
)
app.add_page(landing_page, route="/")
app.add_page(jersey_swap_page, route="/jersey-swap")
app.add_page(image_gen_page, route="/image-gen")
app.add_page(ai_coach_page, route="/ai-coach")
app.add_page(photo_analysis_page, route="/photo-analysis")
app.add_page(news_page, route="/news", on_load=NewsState.on_mount)