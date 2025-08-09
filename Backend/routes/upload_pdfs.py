from fastapi import APIRouter, UploadFile, File
from typing import List
from modules.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger


router=APIRouter()

@router.get("/test/")
async def test_endpoint():
    return {"message": "Upload endpoint is working"}

@router.post("/upload_pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        logger.info(f"Received request with {len(files) if files else 'no'} files")
        
        # Log request details for debugging
        if files:
            for i, file in enumerate(files):
                logger.info(f"File {i+1}: name='{file.filename}', content_type='{file.content_type}', size='{getattr(file, 'size', 'unknown')}'")
        else:
            logger.error("No files received in request")
            return JSONResponse(status_code=400, content={"error": "No files provided"})
        
        # Validate files before processing
        for file in files:
            logger.info(f"Processing file: {file.filename}, size: {file.size if hasattr(file, 'size') else 'unknown'}")
            if not file.filename:
                return JSONResponse(status_code=400, content={"error": "File has no filename"})
            if not file.filename.lower().endswith('.pdf'):
                return JSONResponse(status_code=400, content={"error": f"File {file.filename} is not a PDF"})
        
        load_vectorstore(files)
        logger.info("Document added to vectorstore")
        return {"messages": "Files processed and vectorstore updated"}
    except Exception as e:
        logger.exception("Error during PDF upload")
        return JSONResponse(status_code=500, content={"error": str(e)})