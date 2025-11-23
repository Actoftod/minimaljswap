import reflex as rx
from app.components.layout import layout


def placeholder_content(title: str, icon: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="w-12 h-12 text-sky-500 mb-6"),
            rx.el.h1(title, class_name="text-3xl font-bold text-gray-900 mb-4"),
            rx.el.p(
                description,
                class_name="text-lg text-gray-600 max-w-xl text-center mb-8",
            ),
            rx.el.div(
                "Coming Soon in Phase 2",
                class_name="px-4 py-2 rounded-full bg-sky-50 text-sky-600 text-sm font-medium border border-sky-100",
            ),
            class_name="flex flex-col items-center justify-center min-h-[60vh] text-center",
        )
    )


def jersey_swap_page() -> rx.Component:
    return layout(
        placeholder_content(
            "Jersey Swap",
            "shirt",
            "Upload your photo and swap jerseys with your favorite players instantly.",
        )
    )


def image_gen_page() -> rx.Component:
    return layout(
        placeholder_content(
            "Image Generator",
            "image",
            "Generate stunning sports visuals and concepts with AI power.",
        )
    )


def ai_coach_page() -> rx.Component:
    return layout(
        placeholder_content(
            "AI Coach",
            "bot",
            "Your personal expert coach for strategy, training, and analysis.",
        )
    )


def photo_analysis_page() -> rx.Component:
    return layout(
        placeholder_content(
            "Photo Analysis",
            "scan-search",
            "Deep tactical insights from your game photos and screenshots.",
        )
    )


def news_page() -> rx.Component:
    return layout(
        placeholder_content(
            "Sports News",
            "newspaper",
            "Real-time updates and curated news from the sports world.",
        )
    )