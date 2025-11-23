import reflex as rx
import os
from google import genai
from google.genai import types
import logging
import random
import string


class PhotoAnalysisState(rx.State):
    """State for the Photo Analysis feature."""

    uploaded_image: str = ""
    analysis_result: str = ""
    is_analyzing: bool = False
    error_message: str = ""

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of the photo to analyze."""
        if not files:
            return
        self.error_message = ""
        self.analysis_result = ""
        try:
            file = files[0]
            upload_data = await file.read()
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
            filename = f"analysis_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}.{ext}"
            file_path = upload_dir / filename
            with open(file_path, "wb") as f:
                f.write(upload_data)
            self.uploaded_image = filename
        except Exception as e:
            logging.exception(f"Upload Error: {e}")
            self.error_message = f"Upload Error: {str(e)}"

    @rx.event
    async def analyze_photo(self):
        """Call Gemini API to analyze the uploaded photo."""
        if not self.uploaded_image:
            self.error_message = "Please upload a photo first."
            return
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.error_message = "Google API Key not found."
            return
        self.is_analyzing = True
        self.error_message = ""
        self.analysis_result = ""
        yield
        try:
            client = genai.Client(api_key=api_key)
            upload_dir = rx.get_upload_dir()
            file_path = upload_dir / self.uploaded_image
            with open(file_path, "rb") as f:
                image_bytes = f.read()
            prompt = """
            Analyze this sports image. Provide a detailed breakdown including:
            1. Detected Sport & Context
            2. Form & Technique Analysis (if players are visible)
            3. Tactical Setup (if applicable)
            4. Equipment & Conditions
            5. Key Strengths & Areas for Improvement

            Format the output with Markdown headings and bullet points. Keep it professional and insightful.
            """
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                    prompt,
                ],
            )
            if response.text:
                self.analysis_result = response.text
            else:
                self.error_message = "Could not generate analysis."
        except Exception as e:
            logging.exception(f"Analysis Error: {e}")
            self.error_message = f"Analysis Error: {str(e)}"
        finally:
            self.is_analyzing = False