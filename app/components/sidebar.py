import reflex as rx
from app.states.nav_state import NavState


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    """A single navigation item in the sidebar."""
    is_active = NavState.current_path == href
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="w-5 h-5"),
            rx.el.span(text, class_name="font-medium"),
            class_name=rx.cond(
                is_active,
                "flex items-center gap-3 px-3 py-2 rounded-lg bg-sky-50 text-sky-600 transition-all duration-200",
                "flex items-center gap-3 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-all duration-200",
            ),
        ),
        href=href,
        on_click=NavState.close_menu,
        class_name="block mb-1",
    )


def sidebar() -> rx.Component:
    """The main sidebar component."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("trophy", class_name="w-8 h-8 text-sky-500"),
                rx.el.span(
                    "JERSEYSWAP",
                    class_name="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-sky-500 to-blue-600",
                ),
                class_name="flex items-center gap-3 px-2",
            ),
            class_name="h-16 flex items-center mb-6",
        ),
        rx.el.nav(
            rx.el.div(
                rx.el.span(
                    "APP",
                    class_name="text-xs font-semibold text-gray-400 px-3 mb-2 block tracking-wider",
                ),
                sidebar_item("Dashboard", "layout-dashboard", "/"),
                sidebar_item("Jersey Swap", "shirt", "/jersey-swap"),
                sidebar_item("Image Generator", "image", "/image-gen"),
                sidebar_item("AI Coach", "bot", "/ai-coach"),
                sidebar_item("Photo Analysis", "scan-search", "/photo-analysis"),
                sidebar_item("Sports News", "newspaper", "/news"),
                class_name="space-y-1",
            ),
            class_name="flex-1 overflow-y-auto",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("user", class_name="w-5 h-5 text-gray-600"),
                    class_name="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center border border-gray-200",
                ),
                rx.el.div(
                    rx.el.p(
                        "Sports Fan", class_name="text-sm font-medium text-gray-900"
                    ),
                    rx.el.p("Pro Plan", class_name="text-xs text-sky-500 font-medium"),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="pt-4 mt-4 border-t border-gray-100",
        ),
        class_name="fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 px-4 py-4 flex flex-col transition-transform duration-300 lg:translate-x-0 lg:static lg:h-screen",
    )