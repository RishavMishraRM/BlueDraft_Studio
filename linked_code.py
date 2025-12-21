from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from groq import Groq
from dotenv import load_dotenv

from pathlib import Path

load_dotenv()

app = FastAPI()

# Get absolute path for Vercel compatibility
BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse(BASE_DIR / 'static/index.html')

class UserRequest(BaseModel):
    content: str
    mode: str = "linkedin"  # Default to linkedin

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

SYSTEM_PROMPTS = {
    "linkedin": "you are a helpful assistant who can generate a great linkedin post with a unique and engaging title, descriptions and hashtags.",
    "research": "you are a deep research assistant. provide comprehensive, fact-based, and detailed explanations. structure your answers with clear headings and bullet points."
}

@app.post("/chat")
async def chat(request: UserRequest):
    try:
        system_instruction = SYSTEM_PROMPTS.get(request.mode, SYSTEM_PROMPTS["linkedin"])
        
        # Combine user content with the specific system instruction
        final_content = f"{request.content}\n\nSystem Instruction: {system_instruction}"

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": final_content,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return {"response": chat_completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
