"""
FastAPI application for English to Hinglish translation service
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os

# Add parent directory to path to import utility module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utility.translator import english_to_hinglish
from api.models import TranslationRequest, TranslationResponse, HealthResponse

# Create FastAPI app
app = FastAPI(
    title="English to Hinglish Translator API",
    description="API for translating English text to Hinglish (Hindi in Roman script)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse, tags=["Health"])
async def root():
    """
    Root endpoint - Health check
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        message="English to Hinglish Translator API is running"
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        message="Service is running and ready to translate"
    )


@app.post("/translate", response_model=TranslationResponse, tags=["Translation"])
async def translate(request: TranslationRequest):
    """
    Translate English text to Hinglish (Hindi in Roman script)
    
    - **text**: English text to translate (1-1000 characters)
    
    Returns the original text and translated Hinglish text.
    """
    try:
        # Validate input
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )
        
        # Perform translation
        hinglish_text = english_to_hinglish(request.text)
        
        # Check if translation failed
        if hinglish_text.startswith("Translation error:"):
            return TranslationResponse(
                original_text=request.text,
                hinglish_text="",
                success=False,
                error=hinglish_text
            )
        
        # Return successful translation
        return TranslationResponse(
            original_text=request.text,
            hinglish_text=hinglish_text,
            success=True,
            error=None
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
