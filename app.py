from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import openai
import re
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class ColorPrompt(BaseModel):
    prompt: str

def get_color_palette(prompt):
    try:
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
        return colors
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON response from API: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating color palette: {str(e)}")
@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/palette')
async def prompt_to_palette(color_prompt: ColorPrompt):
    try:
        colors = get_color_palette(color_prompt.prompt)
        return JSONResponse(content={"colors": colors})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)