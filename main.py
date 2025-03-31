from fastapi import FastAPI, File, Form, UploadFile
import os
import pandas as pd
import openai
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()

OPENAI_API_KEY = os.getenv("eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDUyODNAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.vWF4gO2PHnFGPolj9EYPRbcI0QjbYTiyb0OFSfdzPH0")
openai.api_key = OPENAI_API_KEY

app = FastAPI()

@app.post("/api/")
async def solve_question(question: str = Form(...), file: UploadFile = None):
    try:
        if file:
            # Handle file processing (CSV example)
            contents = await file.read()
            df = pd.read_csv(pd.compat.StringIO(contents.decode("utf-8")))
            if "answer" in df.columns:
                answer = df["answer"].iloc[0]  # Assuming answer is in the first row
                return JSONResponse(content={"answer": str(answer)})
        
        # Query OpenAI's GPT model for an answer
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}]
        )
        answer = response["choices"][0]["message"]["content"]
        
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
