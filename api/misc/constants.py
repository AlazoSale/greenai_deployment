
model_id = "BAAI/bge-m3"
API_INFERENCE_URL = "https://api-inference.huggingface.co"
RAG_SERVICE_URL = f"{API_INFERENCE_URL}/pipeline/feature-extraction/{model_id}"
MISTRAL_API_URL = f"{API_INFERENCE_URL}/models/mistralai/Mistral-7B-Instruct-v0.2"


SUPPORTED_T2T_LANGUAGES = {
    "Hindi": "hi",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
    "English": "en"
}

SUPPORTED_STT_LANGUAGES = {
    "Hindi": "hi",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
    "SEnglish": "en-US",
    "TEnglish": "en"
}