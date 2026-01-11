from fastapi import FastAPI, HTTPException, UploadFile, File, Form # Importing essential FastAPI components for web routing and file handling
from fastapi.staticfiles import StaticFiles # Importing StaticFiles to serve CSS, JS, and image assets
from fastapi.responses import FileResponse # Importing FileResponse to return physical files like index.html
from pydantic import BaseModel # Importing BaseModel for structured request payload validation
import os # Importing os to interact with environment variables and system paths
from groq import Groq # Importing Groq client for AI model inference orchestration
from dotenv import load_dotenv # Importing load_dotenv to read secret keys from the .env file
from pathlib import Path # Importing Path for cross-platform filesystem path manipulations
import requests # Importing requests for fetching URL content
from bs4 import BeautifulSoup # Importing BeautifulSoup for HTML parsing

load_dotenv() # Executing the loading of environment variables into the process state

app = FastAPI() # Initializing the core FastAPI application instance

# Get absolute path for Vercel compatibility
BASE_DIR = Path(__file__).resolve().parent # Determining the root directory of the source file for absolute path mapping

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static") # Mounting the 'static' directory to serve frontend assets via URL

@app.get("/") # Defining the root entry point for the web application
async def read_root(): # Handler function for the landing page request
    return FileResponse(BASE_DIR / 'static/index.html') # Serving the main frontend HTML file from the static folder

class UserRequest(BaseModel): # Defining the data schema for general chat requests
    content: str # The text prompt or message sent by the user
    mode: str = "linkedin"  # The specialized AI mode selection, defaulting to linkedin

client = None # Initializing the global Groq client variable as empty

def get_groq_client(): # Logic to retrieve or initialize the Groq AI client
    global client # Accessing the singleton client instance in global scope
    api_key = os.environ.get("GROQ_API_KEY") # Attempting to find the necessary API key in environment
    if not api_key: # Validation check for missing API configuration
        print("Warning: GROQ_API_KEY not found in environment variables.") # Logging warning for missing credentials
        return None # Returning null if unauthorized
        
    if client is None: # Lazy initialization check for the AI client
        client = Groq(api_key=api_key) # Creating a new Groq client instance with the validated key
    return client # Returning the active client for API usage

SYSTEM_PROMPTS = { # Map of system instructions defining AI personas for different modes
    "linkedin": "You are a LinkedIn Viral Content Expert. Your goal is to write a high-impact post. 1. HOOK: Start with a magnetic 'Hook' (first 2 lines) that forces the reader to stop scrolling. 2. ENGAGEMENT: Optimize for maximum engagement using short, punchy sentences, adequate white space, and a clear Call to Action (CTA) at the end. Include relevant hashtags.", # Personality for social media drafting
    "research": "You are a deep research assistant. Provide comprehensive, fact-based, and detailed explanations. Structure your answers with clear headings and bullet points.", # Personality for technical depth
    "reviewer": "You are an expert LinkedIn profile consultant. Review the provided LinkedIn profile data against the user's CV. Provide a Score (1-100) and actionable advice on what to add or improve in the LinkedIn profile to match the CV's strengths. Based on the user's CV, ask them to write Current Education / Position, About (Summary), Experience, Education, Skills, Projects, Licenses, Certifications, Achievements & Extras, Additional Sections (Languages, Organizations, Interests).", # Personality for CV auditing
    "improver_hook": "You are a world-class copywriter specialized in magnetic hooks. Your task is to rewrite the user's input to create 3 different high-impact 'scroll-stopping' hooks that grab attention immediately. Keep the core message but optimize for curiosity and impact.", # Persona for hook optimization
    "improver_clarity": "You are an expert editor focused on clarity and flow. Your task is to rewrite the user's input to make it more professional, concise, and easy to read. Fix any awkward phrasing while maintaining the original tone and intent.", # Persona for technical writing improvement
    "improver_engagement": "You are a social media growth strategist. Your task is to rewrite the user's input to maximize readability and engagement. Use bullet points, line breaks for white space, and add a compelling call-to-action (CTA) at the end.", # Persona for engagement optimization
    "agent_workspace": "You are a Content Strategist. Your goal is to write a high-impact LinkedIn post based on the provided person details, tone, and optional URL research. 1. HOOK: Start with a magnetic 'Hook' (first 2 lines). 2. ANALYZE: If a URL or context is provided, incorporate its key insights. 3. STYLE: Match the chosen tone (Professional, Casual, Bold, Sarcastic, etc.) perfectly. Include relevant hashtags." # Personality for the new Agent Workspace
}


def extract_text_from_pdf(file_content: bytes) -> str: # Utility to parse text data from raw PDF byte streams
    from pypdf import PdfReader # Importing PDF parsing library locally to reduce load overhead
    from io import BytesIO # Importing BytesIO to treat raw bytes as a readable file stream
    try: # Start of error-controlled parsing block
        reader = PdfReader(BytesIO(file_content)) # Initializing the PDF reader with the byte stream
        text = "" # Creating a workspace string for the extracted text
        for page in reader.pages: # Iterating through every page in the document
            text += page.extract_text() or "" # Appending page content if readable
        return text # Returning the full document text string
    except Exception as e: # Catching any parsing or formatting errors
        return f"[Error extracting PDF: {str(e)}]" # Returning an error message instead of crashing

@app.post("/review") # Endpoint for handling CV and LinkedIn profile analysis
async def review_profile( # Handler for multipart form data submissions
    cv: UploadFile = File(...), # Required PDF upload containing the user's resume
    linkedin_profile: UploadFile = File(None), # Optional PDF upload of the user's LinkedIn profile
    linkedin_url: str = Form(None) # Optional text field for the LinkedIn profile web address
): # Function body start
    try: # Start of request processing block
        client = get_groq_client() # Retrieving the authorized AI client
        if not client: # Check for API configuration failure
             raise HTTPException(status_code=500, detail="Server Configuration Error: GROQ_API_KEY is missing.") # Aborting with server error

        # Extract CV Text
        cv_contents = await cv.read() # Reading the raw bytes from the uploaded CV file
        cv_text = extract_text_from_pdf(cv_contents) # Converting the Resume bytes into plain text

        # Extract LinkedIn Text
        linkedin_text = "" # Initializing empty string for profile data
        if linkedin_profile: # Checking if a profile PDF was provided
            lp_contents = await linkedin_profile.read() # Reading the raw bytes from the LinkedIn upload
            linkedin_text = extract_text_from_pdf(lp_contents) # Converting the Profile bytes into plain text
        
        source_info = f"LinkedIn URL provided: {linkedin_url}" if linkedin_url else "" # Formulating URL metadata if present

        # Construct the Prompt
        final_content = ( # Concatenating context together for the AI model
            f"Here is the user's CV Content:\n{cv_text}\n\n" # Injecting Resume text
            f"Here is the user's LinkedIn Profile Content:\n{linkedin_text}\n\n" # Injecting Profile text
            f"{source_info}\n\n" # Injecting URL source info
            f"System Instruction: {SYSTEM_PROMPTS['reviewer']}" # Injecting specialized persona steering
        )

        chat_completion = client.chat.completions.create( # Calling the LLM to perform the comparison analysis
            messages=[ # Defining the message thread for the model
                {
                    "role": "user", # Standard user role for providing context
                    "content": final_content, # The combined analysis prompt
                }
            ],
            model="llama-3.3-70b-versatile", # Specifying the high-performance Llama model via Groq
        )
        return {"response": chat_completion.choices[0].message.content} # Returning the generated advice JSON
    except Exception as e: # Handling runtime exceptions
        raise HTTPException(status_code=500, detail=str(e)) # Transmitting error details to client

def scrape_url(url: str) -> dict: # Utility to scrape text and metadata from a URL
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        title = soup.title.string if soup.title else "No Title Found"
        text = soup.get_text(separator=' ', strip=True)
        # Truncate text to avoid huge prompts
        return {"title": title, "content": text[:4000]}
    except Exception as e:
        return {"title": "Error", "content": f"Failed to scrape: {str(e)}"}

class WorkspaceRequest(BaseModel): # Defining the data schema for the new workspace requests
    person: str # Name or description of the person
    tone: str # Selected tone (Professional, Casual, Bold, etc.)
    url: str = None # Optional URL for research context

@app.post("/workspace") # Endpoint for the new Agent Workspace logic
async def agent_workspace(request: WorkspaceRequest):
    try:
        client = get_groq_client()
        if not client:
             raise HTTPException(status_code=500, detail="Server Configuration Error: GROQ_API_KEY is missing.")

        # Construct the Prompt for Workspace Agent
        scraped_info = ""
        scraped_summary = "None (No URL provided)"
        
        if request.url:
             data = scrape_url(request.url)
             scraped_info = f"Research Data (from URL - {data['title']}):\n{data['content']}"
             scraped_summary = f"Summary of {data['title']}: {data['content'][:200]}..."

        final_content = (
            f"Target Person: {request.person}\n"
            f"Desired Tone: {request.tone}\n"
            f"{scraped_info}\n\n"
            f"System Instruction: {SYSTEM_PROMPTS['agent_workspace']}"
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
        return {
            "response": chat_completion.choices[0].message.content,
            "scraped_summary": scraped_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat") # Endpoint for general conversational drafting and research
async def chat(request: UserRequest): # Handler accepting structured JSON payloads
    try: # Start of chat processing block
        client = get_groq_client() # Retrieving the authorized AI client
        if not client: # Check for API configuration failure
             raise HTTPException(status_code=500, detail="Server Configuration Error: GROQ_API_KEY is missing.") # Aborting with server error

        system_instruction = SYSTEM_PROMPTS.get(request.mode, SYSTEM_PROMPTS["linkedin"]) # Selecting the correct persona for the request
        
        # Combine user content with the specific system instruction
        final_content = f"{request.content}\n\nSystem Instruction: {system_instruction}" # Formatting the prompt for precise steering

        chat_completion = client.chat.completions.create( # Calling the LLM for response generation
            messages=[ # Defining the message thread for the model
                {
                    "role": "user", # User role for the specific query
                    "content": final_content, # The combined instruction prompt
                }
            ],
            model="llama-3.3-70b-versatile", # Specifying the Llama model for inference
        )
        return {"response": chat_completion.choices[0].message.content} # Returning the AI's content response
    except Exception as e: # Handling runtime and network exceptions
        raise HTTPException(status_code=500, detail=str(e)) # Transmitting error details to client

if __name__ == "__main__": # Entry point for local execution
    import uvicorn # Importing the ASGI server for hosting
    uvicorn.run(app, host="0.0.0.0", port=8000) # Launching the application on development port

