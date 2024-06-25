

from django.conf import settings
import requests, json
from pinecone import Pinecone
import time

from api.misc import constants as miscConstants

def process_query(query):
    context_docs = rag_service(query)
    if not context_docs:
        return {"response": "Sorry but I don't have relevant knowledge to answer that query."}

    context = " ".join(context_docs)
    prompt = generate_prompt(query, context)

    headers = {"Authorization": f"Bearer {settings.HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "top_p": 0.40,
            "max_new_tokens": 2000,
            "temperature": 0.40,
        }
    }
    #here
    start_time = time.time() 
    response = requests.post(miscConstants.MISTRAL_API_URL, headers=headers, json=payload, timeout=600)
    if response.status_code != 200:
        return {"response": "Error in generating response from model."}
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Mistral time {time_taken}")
    #---------------------------------------------------------------
    try:
        result_json = response.json()
        result = result_json[0]["generated_text"].rpartition("Answer:")[-1].strip()
        return {"response": result}
    except json.JSONDecodeError:
        return {"response": "Failed to decode JSON response from model."}


def generate_prompt(query: str, context: str) -> str:
    prompt = f"""
    You are a Legal Expert who provides expert legal analysis and advice, solely based on the relevant context provided to you. You must show professionalism, knowledge, and experience as a highly respected and seasoned legal professional.

    Your responses should reflect a deep and nuanced understanding of case law, statutes, regulations, and legal principles across various domains. Analyze all facts objectively, identifying key issues and providing thorough legal assessments. Maintain a strategic mindset, anticipating potential challenges and proactively suggesting courses of action aligned with optimal outcomes for the client's interests.

    Craft your advice with clarity and precision, explaining complex legal concepts in a manner that is authoritative yet accessible. Tailor your communication style to be appropriate for legal contexts. However, ensure your analysis stems purely from the provided context, and does not introduce any external information or perspective AT ALL!

    You cannot refer to the context directly or quote from it. Your role is to synthesize and convey the relevant legal guidance as if it were your own deeply studied expertise. If critical details are missing from the context that inhibits a comprehensive response, then gently refuse to answer. Otherwise, provide definitive legal counsel as a leading expert you are.

    Always adhere to following points:
      1. You may be provided with chat history of the user in your context. Your answer should take this chat history into account while generating the answer. The final answer should stay relevant to previous chat.
      2. At no point you are allowed to refer anything out of context. You cannot cite laws, cases, citations, and (or) quotations that are not provided in the context.
      3. You can only use context to form your answer, you cannot refer to the context or the conversation directly. You must always act as a legal expert who is just giving advice based on the context.
      4. If you are unable to generate an answer based on the context provided, then simply decline to answer. Do not try to come up with your own answer.
      5. Banned phrases:
        a. "based on the context/information"
        b. "according to the context/information"
        c. "in the conversation history"
        d. "in the context provided"
        e. "it appears that you"
        f. "the context/information provided"
        g. "as a legal expert"
      6. Do not end your answer by suggesting the user consult a legal professional as you are the legal expert they are consulting.

    CONTEXT FOR THE QUERY (STRICTLY ADHERE TO IT)
    ----------------------
    {context}
    ----------------------
    Query: {query}
    
    Answer:
    """
    return prompt

def rag_service(query: str) -> list:
    """
    Retrieves relevant legal contexts from a knowledge base using a Retrieval-Augmented Generation (RAG) approach.

    Args:
        query (str): The user's legal query.

    Returns:
        list: A list of relevant legal contexts found in the knowledge base.
    """
    hf_token = settings.HF_TOKEN
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    #here
    s = time.time() 
    response = requests.post(miscConstants.RAG_SERVICE_URL, headers=headers, json={"inputs": query, "options": {"wait_for_model": True}}, timeout=6000)
    response.raise_for_status()
    e = time.time()
    tt = e - s
    print(f"Embedder time {tt}")

    query_emb = response.json()
    #---------------------------------------------------------------

    #here
    start_time = time.time() 
    index = Pinecone(api_key=settings.PC_KEY).Index("ai-law")
    result = index.query(vector=query_emb, top_k=settings.MAX_RET_DOCS, include_values=True, include_metadata=True)
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Pinecone time {time_taken}")
    #---------------------------------------------------------------
    
    return [
        f"{match['metadata']['question']} {match['metadata']['answer']}"
        for match in result.matches
        if match["score"] <= settings.MAX_SCORE and match["metadata"].get("question") and match["metadata"].get("answer")
    ]
