from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain.schema import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger
import os

router=APIRouter()

@router.post("/ask_questions/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"user query: {question}")

        # Validate environment variables
        if not os.environ.get("PINECONE_API_KEY"):
            return JSONResponse(status_code=500, content={"error": "PINECONE_API_KEY not configured"})
        if not os.environ.get("PINECONE_INDEX_NAME"):
            return JSONResponse(status_code=500, content={"error": "PINECONE_INDEX_NAME not configured"})

        # Embed model + Pinecone setup
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
        embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        embedded_query = embed_model.embed_query(question)
        res = index.query(vector=embedded_query, top_k=3, include_metadata=True)

        logger.debug(f"Retrieved {len(res['matches'])} matches from Pinecone")
        for i, match in enumerate(res["matches"]):
            logger.debug(f"Match {i}: score={match['score']}, metadata={match['metadata']}")

        docs = [
            Document(
                page_content=match["metadata"].get("text", ""),
                metadata=match["metadata"]
            ) for match in res["matches"]
        ]
        
        logger.debug(f"Created {len(docs)} documents")
        for i, doc in enumerate(docs):
            logger.debug(f"Doc {i}: content_length={len(doc.page_content)}, metadata={doc.metadata}")

        # Create a simple retriever that returns the retrieved documents
        class SimpleRetriever(BaseRetriever):
            def __init__(self, documents: List[Document]):
                super().__init__()
                self._docs = documents

            def _get_relevant_documents(self, query: str) -> List[Document]:
                logger.debug(f"Retriever called with query: {query}, returning {len(self._docs)} docs")
                return self._docs

        retriever = SimpleRetriever(docs)
        chain = get_llm_chain(retriever)
        
        # Test the retriever directly
        retrieved_docs = retriever.get_relevant_documents(question)
        logger.debug(f"Direct retriever test returned {len(retrieved_docs)} docs")
        
        result = query_chain(chain, question)

        logger.info("query successful")
        return result

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})