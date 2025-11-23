import reflex as rx
from app.components.layout import layout
from app.states.jersey_swap_state import JerseySwapState


def jersey_swap_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Jersey Swap", class_name="text-3xl font-bold text-gray-900 mb-2"
                ),
                rx.el.p(
                    "Visualize yourself in any team's kit using AI.",
                    class_name="text-gray-600",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "1. Upload Photo",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.upload.root(
                            rx.el.div(
                                rx.icon(
                                    "upload", class_name="w-8 h-8 text-sky-500 mb-2"
                                ),
                                rx.el.p(
                                    "Drag and drop or click to upload",
                                    class_name="text-sm text-gray-600",
                                ),
                                class_name="flex flex-col items-center justify-center p-6 border-2 border-dashed border-gray-300 rounded-xl bg-gray-50 hover:bg-sky-50 hover:border-sky-300 transition-colors cursor-pointer",
                            ),
                            accept={"image/*": [".png", ".jpg", ".jpeg", ".webp"]},
                            max_files=1,
                            on_drop=JerseySwapState.handle_upload,
                            class_name="w-full",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "2. Select Team",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.el.select(
                            rx.el.option(
                                "Select a team...",
                                value="",
                                disabled=True,
                                selected=True,
                            ),
                            rx.foreach(
                                JerseySwapState.teams,
                                lambda x: rx.el.option(x, value=x),
                            ),
                            value=JerseySwapState.selected_team,
                            on_change=JerseySwapState.set_selected_team,
                            class_name="w-full rounded-xl border-gray-300 shadow-sm focus:border-sky-500 focus:ring-sky-500",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        rx.cond(
                            JerseySwapState.is_processing,
                            rx.el.span(
                                rx.spinner(size="1", class_name="mr-2 inline-block"),
                                "Swapping Jerseys...",
                                class_name="flex items-center justify-center",
                            ),
                            rx.el.span(
                                rx.icon("shirt", class_name="w-4 h-4 mr-2"),
                                "Swap Jersey",
                                class_name="flex items-center justify-center",
                            ),
                        ),
                        on_click=JerseySwapState.generate_swap,
                        disabled=JerseySwapState.is_processing,
                        class_name="w-full py-3 px-4 bg-sky-600 hover:bg-sky-700 text-white font-medium rounded-xl shadow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed",
                    ),
                    rx.cond(
                        JerseySwapState.error_message,
                        rx.el.div(
                            rx.icon(
                                "badge_alert", class_name="w-5 h-5 text-red-500 mr-2"
                            ),
                            JerseySwapState.error_message,
                            class_name="mt-4 p-3 bg-red-50 text-red-700 rounded-lg flex items-center text-sm",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 h-fit",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Preview",
                            class_name="text-lg font-semibold text-gray-900 mb-4",
                        ),
                        rx.cond(
                            JerseySwapState.original_image,
                            rx.el.div(
                                rx.el.div(
                                    rx.el.span(
                                        "Original",
                                        class_name="absolute top-2 left-2 px-2 py-1 bg-black/50 text-white text-xs rounded-md backdrop-blur-sm",
                                    ),
                                    rx.image(
                                        src=rx.get_upload_url(
                                            JerseySwapState.original_image
                                        ),
                                        class_name="w-full h-64 object-cover rounded-xl border border-gray-200",
                                        alt="Original uploaded image",
                                    ),
                                    class_name="relative mb-4",
                                ),
                                rx.cond(
                                    JerseySwapState.swapped_image,
                                    rx.el.div(
                                        rx.el.span(
                                            "Swapped Result",
                                            class_name="absolute top-2 left-2 px-2 py-1 bg-sky-500/80 text-white text-xs rounded-md backdrop-blur-sm",
                                        ),
                                        rx.image(
                                            src=rx.get_upload_url(
                                                JerseySwapState.swapped_image
                                            ),
                                            class_name="w-full h-auto object-cover rounded-xl shadow-lg border border-gray-100",
                                            alt="Swapped jersey result",
                                        ),
                                        rx.el.a(
                                            rx.icon(
                                                "download", class_name="w-4 h-4 mr-2"
                                            ),
                                            "Download Result",
                                            href=rx.get_upload_url(
                                                JerseySwapState.swapped_image
                                            ),
                                            download=f"jersey_swap_{JerseySwapState.selected_team}.png",
                                            class_name="mt-4 inline-flex items-center justify-center w-full py-2 px-4 bg-white border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors",
                                        ),
                                        class_name="relative animate-in fade-in zoom-in duration-500",
                                    ),
                                    rx.cond(
                                        JerseySwapState.is_processing,
                                        rx.el.div(
                                            rx.spinner(
                                                size="3", class_name="text-sky-500 mb-4"
                                            ),
                                            rx.el.p(
                                                "AI is crafting your new look...",
                                                class_name="text-gray-500 font-medium animate-pulse",
                                            ),
                                            class_name="h-64 flex flex-col items-center justify-center bg-gray-50 rounded-xl border border-gray-200",
                                        ),
                                        rx.el.div(
                                            rx.icon(
                                                "shirt",
                                                class_name="w-12 h-12 text-gray-300 mb-2",
                                            ),
                                            rx.el.p(
                                                "Select a team and click swap to see the magic",
                                                class_name="text-gray-400 text-center text-sm",
                                            ),
                                            class_name="h-64 flex flex-col items-center justify-center bg-gray-50 rounded-xl border border-dashed border-gray-300",
                                        ),
                                    ),
                                ),
                            ),
                            rx.el.div(
                                rx.icon(
                                    "image", class_name="w-16 h-16 text-gray-300 mb-4"
                                ),
                                rx.el.p(
                                    "Upload a photo to get started",
                                    class_name="text-gray-500 font-medium",
                                ),
                                class_name="h-96 flex flex-col items-center justify-center bg-gray-50 rounded-2xl border border-dashed border-gray-300",
                            ),
                        ),
                        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 h-full",
                    )
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
            ),
            class_name="w-full",
        )
    )