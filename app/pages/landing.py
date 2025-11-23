import reflex as rx
from app.components.layout import layout


def feature_card(
    title: str, description: str, icon: str, href: str, color_class: str
) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"w-8 h-8 {color_class}"),
                class_name="mb-4 p-3 rounded-xl bg-gray-50 w-fit",
            ),
            rx.el.h3(title, class_name="text-lg font-bold text-gray-900 mb-2"),
            rx.el.p(description, class_name="text-sm text-gray-600 leading-relaxed"),
            rx.el.div(
                rx.el.span("Try Now", class_name="text-sm font-medium text-gray-900"),
                rx.icon(
                    "arrow-right",
                    class_name="w-4 h-4 ml-2 text-gray-400 group-hover:text-gray-900 transition-colors",
                ),
                class_name="mt-6 flex items-center opacity-60 group-hover:opacity-100 transition-opacity",
            ),
            class_name="h-full p-6 rounded-2xl bg-white border border-gray-200 shadow-sm hover:shadow-md transition-all duration-300 group hover:-translate-y-1",
        ),
        href=href,
    )


def landing_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "POWERED BY GEMINI AI",
                        class_name="text-xs font-bold tracking-widest text-sky-500 mb-4 block",
                    ),
                    rx.el.h1(
                        "The Ultimate AI Sports Companion",
                        class_name="text-4xl md:text-5xl font-bold text-gray-900 mb-6 tracking-tight",
                    ),
                    rx.el.p(
                        "Create, Analyze, and Improve. Your all-in-one platform for jersey swaps, AI coaching, and deep sports analytics.",
                        class_name="text-lg text-gray-600 max-w-2xl mb-8",
                    ),
                    class_name="mb-12",
                ),
                class_name="py-8",
            ),
            rx.el.div(
                feature_card(
                    "Jersey Swap",
                    "Visualize yourself in any team's jersey instantly using advanced AI image manipulation.",
                    "shirt",
                    "/jersey-swap",
                    "text-blue-500",
                ),
                feature_card(
                    "Image Generator",
                    "Create unique, high-quality sports imagery and artwork from simple text prompts.",
                    "image",
                    "/image-gen",
                    "text-purple-500",
                ),
                feature_card(
                    "AI Coach",
                    "Get personalized training advice, strategy breakdowns, and expert mentorship.",
                    "bot",
                    "/ai-coach",
                    "text-green-500",
                ),
                feature_card(
                    "Photo Analysis",
                    "Upload game photos for instant tactical analysis and performance insights.",
                    "scan-search",
                    "/photo-analysis",
                    "text-orange-500",
                ),
                feature_card(
                    "Sports News",
                    "Stay updated with the latest scores, trades, and headlines from around the world.",
                    "newspaper",
                    "/news",
                    "text-red-500",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            class_name="w-full",
        )
    )