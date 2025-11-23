import reflex as rx
from app.components.layout import layout
from app.states.image_gen_state import ImageGenState


def image_gen_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "AI Image Generator",
                    class_name="text-3xl font-bold text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Create stunning sports visuals from text prompts.",
                    class_name="text-gray-600",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Prompt",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.el.textarea(
                            placeholder="Describe the image you want to create... (e.g., 'A futuristic basketball court on Mars with neon lights')",
                            on_change=ImageGenState.set_prompt,
                            class_name="w-full h-32 rounded-xl border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500 resize-none p-4",
                            default_value=ImageGenState.prompt,
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Style",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.el.div(
                            rx.foreach(
                                ImageGenState.styles,
                                lambda style: rx.el.button(
                                    style,
                                    on_click=lambda: ImageGenState.set_style(style),
                                    class_name=rx.cond(
                                        ImageGenState.style == style,
                                        "px-4 py-2 rounded-full text-sm font-medium bg-purple-100 text-purple-700 border border-purple-200 transition-colors",
                                        "px-4 py-2 rounded-full text-sm font-medium bg-white text-gray-600 border border-gray-200 hover:bg-gray-50 transition-colors",
                                    ),
                                ),
                            ),
                            class_name="flex flex-wrap gap-3",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        rx.cond(
                            ImageGenState.is_generating,
                            rx.el.span(
                                rx.spinner(size="1", class_name="mr-2 inline-block"),
                                "Generating Artwork...",
                                class_name="flex items-center justify-center",
                            ),
                            rx.el.span(
                                rx.icon("sparkles", class_name="w-4 h-4 mr-2"),
                                "Generate Image",
                                class_name="flex items-center justify-center",
                            ),
                        ),
                        on_click=ImageGenState.generate_image,
                        disabled=ImageGenState.is_generating,
                        class_name="w-full py-3 px-4 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-xl shadow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed",
                    ),
                    rx.cond(
                        ImageGenState.error_message,
                        rx.el.div(
                            rx.icon(
                                "badge_alert", class_name="w-5 h-5 text-red-500 mr-2"
                            ),
                            ImageGenState.error_message,
                            class_name="mt-4 p-3 bg-red-50 text-red-700 rounded-lg flex items-center text-sm",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 h-fit",
                ),
                rx.el.div(
                    rx.cond(
                        ImageGenState.generated_image,
                        rx.el.div(
                            rx.image(
                                src=rx.get_upload_url(ImageGenState.generated_image),
                                class_name="w-full h-auto rounded-xl shadow-lg border border-gray-100",
                                alt="Generated AI Image",
                            ),
                            rx.el.div(
                                rx.el.a(
                                    rx.icon("download", class_name="w-4 h-4 mr-2"),
                                    "Download Image",
                                    href=rx.get_upload_url(
                                        ImageGenState.generated_image
                                    ),
                                    download="generated_sport_art.png",
                                    class_name="inline-flex items-center justify-center py-2 px-4 bg-white border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors shadow-sm",
                                ),
                                class_name="mt-4 flex justify-end",
                            ),
                            class_name="animate-in fade-in zoom-in duration-500",
                        ),
                        rx.el.div(
                            rx.cond(
                                ImageGenState.is_generating,
                                rx.el.div(
                                    rx.spinner(
                                        size="3", class_name="text-purple-500 mb-4"
                                    ),
                                    rx.el.p(
                                        "Creating your masterpiece...",
                                        class_name="text-gray-500 font-medium animate-pulse",
                                    ),
                                    class_name="flex flex-col items-center justify-center h-full",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "image",
                                        class_name="w-16 h-16 text-gray-200 mb-4",
                                    ),
                                    rx.el.p(
                                        "Your generated image will appear here",
                                        class_name="text-gray-400 text-center",
                                    ),
                                    class_name="flex flex-col items-center justify-center h-full",
                                ),
                            ),
                            class_name="h-[500px] bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 flex items-center justify-center",
                        ),
                    ),
                    class_name="lg:col-span-2",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
            ),
            class_name="w-full",
        )
    )