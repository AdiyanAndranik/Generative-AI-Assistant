from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np
from scipy.spatial.distance import cosine
import uvicorn

app = FastAPI()

sentence_transformer_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

pipe_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

vc_database = {}

class VCInput(BaseModel):
    url: str

def scrape_website(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch website content.")
    soup = BeautifulSoup(response.text, "html.parser")
    text_content = soup.get_text()
    return text_content

def generate_embeddings(text: str) -> List[float]:
    embeddings = sentence_transformer_model.encode(text)
    return embeddings.tolist()

@app.post("/add_vc/")
def add_vc(data: VCInput):
    url = data.url
    try:
        text_content = scrape_website(url)
        
        embeddings = generate_embeddings(text_content)
        
        vc_database[url] = {
            "embeddings": embeddings,
            "url": url
        }
        return {"message": "VC data added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/extract_info/")
def extract_info(url: str):
    try:
        text_content = scrape_website(url)
        
        questions = [
            "What is the name of VC?",
            "Who are the contacts of this company?",
            "In which type of industries they invest in?",
            "In which investment rounds does this firm participate/lead?"
        ]
        
        info = {}
        
        for question in questions:
            response = pipe_model(question=question, context=text_content)
            answer = response["answer"]
            info[question] = answer
        
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/find_similar/")
def find_similar(url: str):
    try:
        if url not in vc_database:
            raise HTTPException(status_code=400, detail="URL not found in the database.")
        
        given_embeddings = vc_database[url]["embeddings"]
        
        similarities = []
        for vc_url, data in vc_database.items():
            if vc_url != url:
                embeddings = data["embeddings"]
                similarity = 1 - cosine(np.array(given_embeddings), np.array(embeddings))
                similarities.append((similarity, vc_url))
        
        similarities.sort(reverse=True, key=lambda x: x[0])
        top_3_similar_vcs = similarities[:3]
        
        return {"similar_vcs": top_3_similar_vcs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


uvicorn.run(app, host="0.0.0.0", port=8000)
