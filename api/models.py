"""
Pydantic models for API request and response schemas
"""

from pydantic import BaseModel, Field
from typing import Optional


class TranslationRequest(BaseModel):
    """Request model for translation"""
    text: str = Field(..., min_length=1, max_length=1000, description="English text to translate to Hinglish")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "hello how are you"
                },
                {
                    "text": "what are you doing"
                }
            ]
        }
    }


class TranslationResponse(BaseModel):
    """Response model for translation"""
    original_text: str = Field(..., description="Original English text")
    hinglish_text: str = Field(..., description="Translated Hinglish text in Roman script")
    success: bool = Field(default=True, description="Whether translation was successful")
    error: Optional[str] = Field(default=None, description="Error message if translation failed")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "original_text": "hello how are you",
                    "hinglish_text": "namaste Apa kaise ho",
                    "success": True,
                    "error": None
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    message: str = Field(..., description="Health check message")
