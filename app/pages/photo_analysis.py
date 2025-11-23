import reflex as rx
from app.components.layout import layout
from app.states.photo_analysis_state import PhotoAnalysisState


def photo_analysis_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Photo Analysis", class_name="text-3xl font-bold text-gray-900 mb-2"
                ),
                rx.el.p(
                    "Upload game photos for instant AI tactical insights.",
                    class_name="text-gray-600",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Upload Game Photo",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.upload.root(
                            rx.el.div(
                                rx.icon(
                                    "scan-search",
                                    class_name="w-8 h-8 text-orange-500 mb-2",
                                ),
                                rx.el.p(
                                    "Click or drop image to analyze",
                                    class_name="text-sm text-gray-600",
                                ),
                                class_name="flex flex-col items-center justify-center p-6 border-2 border-dashed border-gray-300 rounded-xl bg-gray-50 hover:bg-orange-50 hover:border-orange-300 transition-colors cursor-pointer",
                            ),
                            accept={"image/*": [".png", ".jpg", ".jpeg", ".webp"]},
                            max_files=1,
                            on_drop=PhotoAnalysisState.handle_upload,
                            class_name="w-full",
                        ),
                        class_name="mb-6",
                    ),
                    rx.cond(
                        PhotoAnalysisState.uploaded_image,
                        rx.el.div(
                            rx.image(
                                src=rx.get_upload_url(
                                    PhotoAnalysisState.uploaded_image
                                ),
                                class_name="w-full h-auto rounded-xl shadow-sm border border-gray-200 mb-6",
                                alt="Uploaded analysis image",
                            ),
                            rx.el.button(
                                rx.cond(
                                    PhotoAnalysisState.is_analyzing,
                                    rx.el.span(
                                        rx.spinner(
                                            size="1", class_name="mr-2 inline-block"
                                        ),
                                        "Analyzing...",
                                        class_name="flex items-center justify-center",
                                    ),
                                    rx.el.span(
                                        rx.icon("sparkles", class_name="w-4 h-4 mr-2"),
                                        "Analyze Photo",
                                        class_name="flex items-center justify-center",
                                    ),
                                ),
                                on_click=PhotoAnalysisState.analyze_photo,
                                disabled=PhotoAnalysisState.is_analyzing,
                                class_name="w-full py-3 px-4 bg-orange-500 hover:bg-orange-600 text-white font-medium rounded-xl shadow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed",
                            ),
                        ),
                    ),
                    rx.cond(
                        PhotoAnalysisState.error_message,
                        rx.el.div(
                            rx.icon(
                                "badge_alert", class_name="w-5 h-5 text-red-500 mr-2"
                            ),
                            PhotoAnalysisState.error_message,
                            class_name="mt-4 p-3 bg-red-50 text-red-700 rounded-lg flex items-center text-sm",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 h-fit",
                ),
                rx.el.div(
                    rx.cond(
                        PhotoAnalysisState.analysis_result,
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "Analysis Report",
                                    class_name="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2",
                                ),
                                rx.markdown(
                                    PhotoAnalysisState.analysis_result,
                                    class_name="prose prose-sm prose-slate max-w-none prose-headings:font-bold prose-headings:text-gray-800 prose-p:text-gray-600 prose-li:text-gray-600",
                                ),
                                class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 animate-in fade-in slide-in-from-bottom-4",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    rx.icon("download", class_name="w-4 h-4 mr-2"),
                                    "Export Report",
                                    class_name="text-sm text-gray-600 hover:text-gray-900 flex items-center",
                                    disabled=True,
                                    title="Export coming soon",
                                ),
                                class_name="mt-4 flex justify-end",
                            ),
                        ),
                        rx.el.div(
                            rx.cond(
                                PhotoAnalysisState.is_analyzing,
                                rx.el.div(
                                    rx.spinner(
                                        size="3", class_name="text-orange-500 mb-4"
                                    ),
                                    rx.el.p(
                                        "Processing image details...",
                                        class_name="text-gray-500 font-medium animate-pulse",
                                    ),
                                    class_name="flex flex-col items-center justify-center h-full",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "file-text",
                                        class_name="w-16 h-16 text-gray-200 mb-4",
                                    ),
                                    rx.el.p(
                                        "Upload an image and click analyze to see the report",
                                        class_name="text-gray-400 text-center max-w-xs",
                                    ),
                                    class_name="flex flex-col items-center justify-center h-full",
                                ),
                            ),
                            class_name="bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 min-h-[400px] flex items-center justify-center",
                        ),
                    )
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
            ),
            class_name="w-full",
        )
    )