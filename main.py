from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import ssl
import os

# Disable SSL verification for development (if needed)
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except:
    pass


def english_to_hinglish(text: str) -> str:
    """
    Convert English text to Hinglish (Hindi-Roman script).
    This function uses open-source libraries to translate and transliterate any English text.
    
    Uses:
    - deep-translator: For English to Hindi translation
    - indic-transliteration: For Devanagari to Roman script conversion
    
    Args:
        text: English text to convert
        
    Returns:
        Hinglish translation in Roman script
    
    Examples:
        >>> english_to_hinglish("hello how are you")
        'namaste aap kaise hain'
        >>> english_to_hinglish("what are you doing")
        'aap kya kar rahe hain'
    """
    if not text or not text.strip():
        return ""
    
    try:
        # Step 1: Translate English to Hindi using deep-translator
        translator = GoogleTranslator(source='en', target='hi')
        hindi_text = translator.translate(text)
        
        # Step 2: Transliterate Hindi (Devanagari) to Roman script using indic-transliteration
        # Using ITRANS scheme which is commonly used for Hinglish
        hinglish_text = transliterate(
            hindi_text,
            sanscript.DEVANAGARI,
            sanscript.ITRANS
        )
        
        return hinglish_text
    
    except Exception as e:
        # Fallback: return error message
        return f"Translation error: {str(e)}"


def main():
    # Example usage
    print("English to Hinglish Converter")
    print("-" * 40)
    
    examples = [
        "hello how are you",
        "what are you doing",
        "good morning",
        "thank you"
    ]
    
    for example in examples:
        result = english_to_hinglish(example)
        print(f"{example} -> {result}")


if __name__ == "__main__":
    main()
