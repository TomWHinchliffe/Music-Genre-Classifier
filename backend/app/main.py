from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.spotify_routes import router as spotify_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Change allow origins to https://localhost:5173 later for production (currently allows any website to send a request)
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spotify_router)

@app.get("/")
def root():
    return {"message": "API is running"}
