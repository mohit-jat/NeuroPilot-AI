import os
import base64
import requests

from dotenv import load_dotenv

load_dotenv()


class VisionService:

    def understand_image(self, image_path, question):

        api_key = os.getenv("VISION_API_KEY")
        api_url = os.getenv("VISION_API_URL")
        model = os.getenv("VISION_MODEL")

        if (
            not api_key
            or not api_url
            or not model
            or api_key == "YOUR_VISION_API_KEY"
            or api_url == "YOUR_VISION_API_URL"
            or model == "YOUR_VISION_MODEL"
        ):
            return "Vision API configuration is pending. Please configure VISION_API_KEY, VISION_API_URL, and VISION_MODEL in your .env file."

        try:

            # Read image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(
                    image_file.read()
                ).decode("utf-8")

            # Prepare image format
            image_url = "data:image/jpeg;base64," + image_data

            # Send request to Vision API
            response = requests.post(
                api_url,
                headers={
                    "Authorization": "Bearer " + api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": question
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_url
                                    }
                                }
                            ]
                        }
                    ]
                },
                timeout=60
            )

            response.raise_for_status()

            result = response.json()

            return result["choices"][0]["message"]["content"]

        except Exception as error:

            return "Vision error: " + str(error)
