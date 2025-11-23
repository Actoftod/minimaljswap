import reflex as rx
from app.components.layout import layout
from app.states.ai_coach_state import AiCoachState, Message


def chat_bubble(message: Message) -> rx.Component:
    is_user = message.role == "user"
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                message.content,
                class_name=rx.cond(
                    is_user,
                    "bg-sky-600 text-white rounded-2xl rounded-tr-none px-4 py-3 shadow-sm",
                    "bg-white text-gray-800 rounded-2xl rounded-tl-none px-4 py-3 shadow-sm border border-gray-100",
                ),
            ),
            rx.el.div(message.timestamp, class_name="text-xs text-gray-400 mt-1 px-1"),
            class_name=rx.cond(
                is_user,
                "flex flex-col items-end max-w-[80%]",
                "flex flex-col items-start max-w-[80%]",
            ),
        ),
        class_name=rx.cond(is_user, "flex justify-end mb-4", "flex justify-start mb-4"),
    )


def ai_coach_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "AI Coach", class_name="text-3xl font-bold text-gray-900 mb-2"
                ),
                rx.el.p(
                    "Your personal expert for strategy and training advice.",
                    class_name="text-gray-600",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.foreach(AiCoachState.messages, chat_bubble),
                    rx.cond(
                        AiCoachState.is_typing,
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    class_name="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                                ),
                                rx.el.div(
                                    class_name="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"
                                ),
                                rx.el.div(
                                    class_name="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"
                                ),
                                class_name="flex space-x-1 bg-gray-100 p-3 rounded-2xl rounded-tl-none w-fit",
                            ),
                            class_name="flex justify-start mb-4 animate-in fade-in slide-in-from-bottom-2",
                        ),
                    ),
                    class_name="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/50",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.input(
                            placeholder="Ask about training drills, game strategy, or fitness...",
                            on_change=AiCoachState.set_input_text,
                            on_key_down=AiCoachState.handle_key_down,
                            class_name="flex-1 bg-gray-50 border-0 focus:ring-0 rounded-xl px-4 py-3 text-gray-900 placeholder:text-gray-400",
                            default_value=AiCoachState.input_text,
                        ),
                        rx.el.button(
                            rx.icon("send", class_name="w-5 h-5"),
                            on_click=AiCoachState.send_message,
                            disabled=AiCoachState.is_typing,
                            class_name="bg-sky-600 hover:bg-sky-700 text-white p-3 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed ml-2",
                        ),
                        class_name="flex items-center p-2 bg-white border-t border-gray-100",
                    ),
                    class_name="sticky bottom-0 z-10",
                ),
                class_name="bg-white rounded-2xl shadow-sm border border-gray-200 h-[600px] flex flex-col overflow-hidden",
            ),
            rx.cond(
                AiCoachState.error_message,
                rx.el.div(
                    AiCoachState.error_message,
                    class_name="mt-4 text-sm text-red-500 text-center",
                ),
            ),
            class_name="w-full max-w-4xl mx-auto",
        )
    )