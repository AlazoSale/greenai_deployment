
model_id = "BAAI/bge-m3"
API_INFERENCE_URL = "https://api-inference.huggingface.co"
RAG_SERVICE_URL = f"{API_INFERENCE_URL}/pipeline/feature-extraction/{model_id}"
MISTRAL_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"