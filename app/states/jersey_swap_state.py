import reflex as rx
import os
import base64
from google import genai
from google.genai import types
import random
import string
import logging


class JerseySwapState(rx.State):
    """State for the Jersey Swap feature."""

    original_image: str = ""
    swapped_image: str = ""
    selected_team: str = ""
    is_processing: bool = False
    error_message: str = ""
    teams: list[str] = [
        "AC Milan",
        "AS Monaco",
        "AS Roma",
        "Ajax",
        "Anaheim Ducks",
        "Arizona Cardinals",
        "Arizona Diamondbacks",
        "Arsenal",
        "Aston Villa",
        "Atlanta Braves",
        "Atlanta Falcons",
        "Atlanta Hawks",
        "Atletico Madrid",
        "Baltimore Orioles",
        "Baltimore Ravens",
        "Bayer Leverkusen",
        "Bayern Munich",
        "Benfica",
        "Boca Juniors",
        "Borussia Dortmund",
        "Boston Bruins",
        "Boston Celtics",
        "Boston Red Sox",
        "Brooklyn Nets",
        "Buffalo Bills",
        "Buffalo Sabres",
        "Calgary Flames",
        "Carolina Hurricanes",
        "Carolina Panthers",
        "Celtic",
        "Charlotte Hornets",
        "Chelsea",
        "Chicago Bears",
        "Chicago Blackhawks",
        "Chicago Bulls",
        "Chicago Cubs",
        "Chicago White Sox",
        "Cincinnati Bengals",
        "Cincinnati Reds",
        "Cleveland Browns",
        "Cleveland Cavaliers",
        "Cleveland Guardians",
        "Colorado Avalanche",
        "Colorado Rockies",
        "Columbus Blue Jackets",
        "Dallas Cowboys",
        "Dallas Mavericks",
        "Dallas Stars",
        "Denver Broncos",
        "Denver Nuggets",
        "Detroit Lions",
        "Detroit Pistons",
        "Detroit Red Wings",
        "Detroit Tigers",
        "Edmonton Oilers",
        "FC Barcelona",
        "Flamengo",
        "Florida Panthers",
        "Galatasaray",
        "Golden State Warriors",
        "Green Bay Packers",
        "Houston Astros",
        "Houston Rockets",
        "Houston Texans",
        "Indiana Pacers",
        "Indianapolis Colts",
        "Inter Milan",
        "Jacksonville Jaguars",
        "Juventus",
        "Kansas City Chiefs",
        "Kansas City Royals",
        "Las Vegas Raiders",
        "Liverpool",
        "Los Angeles Angels",
        "Los Angeles Chargers",
        "Los Angeles Clippers",
        "Los Angeles Dodgers",
        "Los Angeles Kings",
        "Los Angeles Lakers",
        "Los Angeles Rams",
        "Manchester City",
        "Manchester United",
        "Memphis Grizzlies",
        "Miami Dolphins",
        "Miami Heat",
        "Miami Marlins",
        "Milwaukee Brewers",
        "Milwaukee Bucks",
        "Minnesota Timberwolves",
        "Minnesota Twins",
        "Minnesota Vikings",
        "Montreal Canadiens",
        "Napoli",
        "Nashville Predators",
        "New England Patriots",
        "New Jersey Devils",
        "New Orleans Pelicans",
        "New Orleans Saints",
        "New York Giants",
        "New York Islanders",
        "New York Jets",
        "New York Knicks",
        "New York Mets",
        "New York Rangers",
        "New York Yankees",
        "Newcastle United",
        "Oakland Athletics",
        "Oklahoma City Thunder",
        "Olympique Lyonnais",
        "Olympique Marseille",
        "Orlando Magic",
        "Ottawa Senators",
        "Paris Saint-Germain (PSG)",
        "Philadelphia 76ers",
        "Philadelphia Eagles",
        "Philadelphia Flyers",
        "Philadelphia Phillies",
        "Phoenix Suns",
        "Pittsburgh Penguins",
        "Pittsburgh Pirates",
        "Pittsburgh Steelers",
        "Porto",
        "Portland Trail Blazers",
        "RB Leipzig",
        "Rangers",
        "Real Madrid",
        "River Plate",
        "Sacramento Kings",
        "San Antonio Spurs",
        "San Diego Padres",
        "San Francisco 49ers",
        "San Francisco Giants",
        "San Jose Sharks",
        "Santos",
        "Seattle Kraken",
        "Seattle Mariners",
        "Seattle Seahawks",
        "Sevilla",
        "St. Louis Blues",
        "St. Louis Cardinals",
        "Tampa Bay Buccaneers",
        "Tampa Bay Lightning",
        "Tampa Bay Rays",
        "Tennessee Titans",
        "Texas Rangers",
        "Toronto Blue Jays",
        "Toronto Maple Leafs",
        "Toronto Raptors",
        "Tottenham Hotspur",
        "Utah Hockey Club",
        "Utah Jazz",
        "Valencia",
        "Vancouver Canucks",
        "Vegas Golden Knights",
        "Washington Capitals",
        "Washington Commanders",
        "Washington Nationals",
        "Washington Wizards",
        "West Ham United",
        "Winnipeg Jets",
    ]

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of the user's photo."""
        if not files:
            return
        self.error_message = ""
        self.swapped_image = ""
        try:
            file = files[0]
            upload_data = await file.read()
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
            filename = f"original_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}.{ext}"
            file_path = upload_dir / filename
            with open(file_path, "wb") as f:
                f.write(upload_data)
            self.original_image = filename
        except Exception as e:
            logging.exception(f"Error uploading file: {e}")
            self.error_message = f"Error uploading file: {str(e)}"

    @rx.event
    async def generate_swap(self):
        """Call Gemini API to swap the jersey."""
        if not self.original_image:
            self.error_message = "Please upload an image first."
            return
        if not self.selected_team:
            self.error_message = "Please select a team."
            return
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.error_message = "Google API Key not found. Please set GOOGLE_API_KEY environment variable."
            return
        self.is_processing = True
        self.error_message = ""
        self.swapped_image = ""
        yield
        try:
            client = genai.Client(api_key=api_key)
            upload_dir = rx.get_upload_dir()
            file_path = upload_dir / self.original_image
            with open(file_path, "rb") as f:
                image_bytes = f.read()
            prompt = f"Swap the clothes of the person in this photo to a {self.selected_team} sports jersey. Keep the face, pose, and background exactly the same. High quality, photorealistic."
            response = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                    prompt,
                ],
                config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
            )
            generated_image_data = None
            if response.parts:
                for part in response.parts:
                    if part.inline_data:
                        generated_image_data = part.inline_data.data
                        break
            if generated_image_data:
                output_filename = f"swapped_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}.png"
                output_path = upload_dir / output_filename
                with open(output_path, "wb") as f:
                    f.write(generated_image_data)
                self.swapped_image = output_filename
            else:
                self.error_message = "No image generated by the model."
        except Exception as e:
            logging.exception(f"AI Processing Error: {e}")
            self.error_message = f"AI Processing Error: {str(e)}"
        finally:
            self.is_processing = False