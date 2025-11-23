import reflex as rx
from app.components.sidebar import sidebar
from app.states.nav_state import NavState


def layout(content: rx.Component) -> rx.Component:
    """The main application layout with sidebar and content area."""
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.button(
                    rx.icon("menu", class_name="w-6 h-6 text-gray-600"),
                    on_click=NavState.toggle_menu,
                    class_name="p-2 rounded-md hover:bg-gray-100 lg:hidden",
                ),
                rx.el.span(
                    "JERSEYSWAP",
                    class_name="text-lg font-bold text-gray-900 ml-2 lg:hidden",
                ),
                class_name="flex items-center h-16 px-4 border-b border-gray-200 bg-white lg:hidden",
            )
        ),
        rx.el.div(
            rx.cond(
                NavState.is_menu_open,
                rx.el.div(
                    class_name="fixed inset-0 bg-gray-900/50 z-40 lg:hidden",
                    on_click=NavState.close_menu,
                ),
            ),
            rx.cond(
                NavState.is_menu_open,
                rx.el.div(sidebar(), class_name="fixed inset-y-0 left-0 z-50"),
                rx.el.div(sidebar(), class_name="hidden lg:block"),
            ),
            rx.el.main(
                rx.el.div(content, class_name="max-w-6xl mx-auto"),
                class_name="flex-1 min-h-screen bg-gray-50/50 p-6 lg:p-8 overflow-y-auto font-mono",
            ),
            class_name="flex flex-1",
        ),
        class_name="min-h-screen flex flex-col lg:flex-row bg-white text-gray-900 font-['JetBrains_Mono']",
    )