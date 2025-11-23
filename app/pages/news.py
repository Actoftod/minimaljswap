import reflex as rx
from app.components.layout import layout
from app.states.news_state import NewsState


def news_card(item: dict[str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                item["source"],
                class_name="text-xs font-bold text-red-500 tracking-wider uppercase",
            ),
            rx.el.span(item["time"], class_name="text-xs text-gray-400"),
            class_name="flex justify-between items-center mb-3",
        ),
        rx.el.h3(
            item["title"],
            class_name="text-lg font-bold text-gray-900 mb-2 leading-tight hover:text-red-600 transition-colors cursor-pointer",
        ),
        rx.el.p(
            item["summary"],
            class_name="text-sm text-gray-600 leading-relaxed line-clamp-3",
        ),
        rx.el.div(
            rx.el.button(
                "Read Story",
                rx.icon("arrow-up-right", class_name="w-3 h-3 ml-1"),
                class_name="text-xs font-semibold text-gray-900 flex items-center mt-4 hover:underline",
            )
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200 flex flex-col h-full",
    )


def news_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Sports News", class_name="text-3xl font-bold text-gray-900"
                    ),
                    rx.el.p(
                        "Latest headlines powered by AI & Google Search.",
                        class_name="text-gray-600 mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.button(
                    rx.icon(
                        "refresh-ccw",
                        class_name=rx.cond(
                            NewsState.is_loading, "w-4 h-4 animate-spin", "w-4 h-4"
                        ),
                    ),
                    on_click=NewsState.fetch_news,
                    disabled=NewsState.is_loading,
                    class_name="p-2 rounded-full hover:bg-gray-100 text-gray-600 transition-colors",
                ),
                class_name="flex justify-between items-start mb-8",
            ),
            rx.el.div(
                rx.foreach(
                    NewsState.categories,
                    lambda cat: rx.el.button(
                        cat,
                        on_click=lambda: NewsState.set_category(cat),
                        class_name=rx.cond(
                            NewsState.selected_category == cat,
                            "px-4 py-2 rounded-full text-sm font-medium bg-red-50 text-red-600 border border-red-100 transition-colors",
                            "px-4 py-2 rounded-full text-sm font-medium bg-white text-gray-600 border border-gray-200 hover:bg-gray-50 transition-colors",
                        ),
                    ),
                ),
                class_name="flex flex-wrap gap-2 mb-8",
            ),
            rx.cond(
                NewsState.is_loading,
                rx.el.div(
                    rx.foreach(
                        rx.Var.range(6),
                        lambda i: rx.el.div(
                            rx.el.div(
                                class_name="h-4 w-20 bg-gray-200 rounded mb-4 animate-pulse"
                            ),
                            rx.el.div(
                                class_name="h-6 w-full bg-gray-200 rounded mb-2 animate-pulse"
                            ),
                            rx.el.div(
                                class_name="h-6 w-3/4 bg-gray-200 rounded mb-4 animate-pulse"
                            ),
                            rx.el.div(
                                class_name="h-16 w-full bg-gray-200 rounded animate-pulse"
                            ),
                            class_name="bg-white p-6 rounded-xl border border-gray-200 h-64",
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                rx.cond(
                    NewsState.news_items.length() > 0,
                    rx.el.div(
                        rx.foreach(NewsState.news_items, news_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                    rx.el.div(
                        rx.icon("newspaper", class_name="w-16 h-16 text-gray-200 mb-4"),
                        rx.el.p(
                            "No news found. Try refreshing or changing category.",
                            class_name="text-gray-400",
                        ),
                        class_name="flex flex-col items-center justify-center py-20",
                    ),
                ),
            ),
            rx.cond(
                NewsState.error_message,
                rx.el.div(
                    rx.icon("badge_alert", class_name="w-5 h-5 mr-2"),
                    NewsState.error_message,
                    class_name="fixed bottom-8 right-8 bg-red-600 text-white px-4 py-3 rounded-xl shadow-lg flex items-center animate-in fade-in slide-in-from-bottom-4",
                ),
            ),
            class_name="w-full",
        )
    )