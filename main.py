from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
import asyncio
import httpx  # For demonstration purposes, assuming an HTTP-based API request

# Setup your API key
genai.configure(api_key=os.environ.get('API_KEY'))
GeminiModel = genai.GenerativeModel('gemini-pro')

app = FastAPI()

class Prompt(BaseModel):
    text: str

@app.post("/generate/")
async def generate_response(prompt: Prompt):
    """
    Receives a prompt and returns the generated response from the Gemini model
    with a timeout of 2 minutes.
    """
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post('https://api.yourgeminiurl.com/generate', json={"prompt": prompt.text})
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error from the Gemini API")
            generated_essay = response.json().get('text', '')
        return {"response": generated_essay}
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
async def greet_visitor():
    """
    Returns a greeting to the visitors.
    """
    return {"message": "Hi visitors"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
