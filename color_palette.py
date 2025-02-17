import openai
from dotenv import dotenv_values
import json 
import re

config= dotenv_values(".env")


openai.api_key = config["OPENAI_API_KEY"]

def get_color_palette(prompt):
    completion = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": f"""
    You are a color palette generating assistant that responds to text prompts for color palettes.
    You should generate a color palette based on the text prompt. The color palette should be between 2 and 8.

    Q: Convert the following text prompt of a color paletter into a list of colors: The italy
    A: ["#008C45", "#CD212A", "#F1BF00", "#009F4D", "#C8102E", "#000000", "#FFFFFF", "#00A3E0"]
        
    Q: Convert the following text prompt of a color paletter into a list of colors: The nature
    A: ["#A8D8B9", "#F2E2A2", "#F2B880", "#D96459", "#8A3B12", "#000000", "#FFFFFF", "#00A3E0"]

    Desired Format: a JSON array of hexadecimals          
    Q: Convert the following text prompt of a color paletter into a list of colors: {prompt}
    A:
    """},
    ],
    max_tokens=100,
    )

    response_text = completion.choices[0].message.content.strip()

    # Remove Markdown code block formatting if present
    response_text = re.sub(r"```json|```", "", response_text).strip()

    colors = json.loads(response_text) 

    def display_colors(colors):
        for color in colors:
            print(f"\033[48;2;{int(color[1:3], 16)};{int(color[3:5], 16)};{int(color[5:7], 16)}m    \033[0m {color}")

    # Example usage
    display_colors(colors)
    
get_color_palette("4 google brand colors")