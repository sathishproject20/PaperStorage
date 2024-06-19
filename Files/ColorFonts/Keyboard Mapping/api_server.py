from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Example mapping of codes to image paths
image_mapping = {
    "C000000": "ColorFonts/000000.png",
    "C000001": "ColorFonts/000001.png"
    # Add more mappings as needed
}

# CORS middleware to allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

class ImageResponse(BaseModel):
    image_url: str

@app.get("/api/images/{code}", response_model=ImageResponse)
def get_image(code: str):
    if code in image_mapping:
        return ImageResponse(image_url=image_mapping[code])
    else:
        raise HTTPException(status_code=404, detail="Image not found")

# Serve the JSON file directly using StaticFiles
app.mount("/", StaticFiles(directory=".", html=False), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
