from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os

# Setup your API key
genai.configure(api_key=os.environ.get('API_KEY'))
GeminiModel = genai.GenerativeModel('gemini-pro')

app = FastAPI()

class Prompt(BaseModel):
    text: str

@app.post("/generate/")
async def generate_response(prompt: Prompt):
    """
    Receives a prompt and returns the generated response from the Gemini model.
    """
    try:
        generated_essay = GeminiModel.generate_content(prompt.text).text
        return {"response": generated_essay}
    except Exception as e:
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
