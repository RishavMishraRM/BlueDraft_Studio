from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from groq import Groq
from dotenv import load_dotenv
# from pypdf import PdfReader (Moved to local scope)
# from io import BytesIO (Moved to local scope)

def extract_text_from_pdf(file_content: bytes) -> str:
    from pypdf import PdfReader
    from io import BytesIO
    try:
        reader = PdfReader(BytesIO(file_content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"[Error extracting PDF: {str(e)}]"

@app.post("/review")
async def review_profile(
    cv: UploadFile = File(...),
    linkedin_profile: UploadFile = File(None),
    linkedin_url: str = Form(None)
):
    try:
        client = get_groq_client()
        if not client:
             raise HTTPException(status_code=500, detail="Server Configuration Error: GROQ_API_KEY is missing.")

        # Extract CV Text
        cv_contents = await cv.read()
        cv_text = extract_text_from_pdf(cv_contents)

        # Extract LinkedIn Text
        linkedin_text = ""
        if linkedin_profile:
            lp_contents = await linkedin_profile.read()
            linkedin_text = extract_text_from_pdf(lp_contents)
        
        source_info = f"LinkedIn URL provided: {linkedin_url}" if linkedin_url else ""

        # Construct the Prompt
        final_content = (
            f"Here is the user's CV Content:\n{cv_text}\n\n"
            f"Here is the user's LinkedIn Profile Content:\n{linkedin_text}\n\n"
            f"{source_info}\n\n"
            f"System Instruction: {SYSTEM_PROMPTS['reviewer']}"
        )

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

@app.post("/chat")
async def chat(request: UserRequest):
    try:
        client = get_groq_client()
        if not client:
             raise HTTPException(status_code=500, detail="Server Configuration Error: GROQ_API_KEY is missing.")

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
