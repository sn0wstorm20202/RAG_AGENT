import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
PINECONE_ENV="us-east-1"
PINECONE_INDEX_NAME="rag-agent"

os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY

UPLOAD_DIR="./uploaded_docs"
os.makedirs(UPLOAD_DIR,exist_ok=True)


# initialize pinecone instance
pc=Pinecone(api_key=PINECONE_API_KEY)
spec=ServerlessSpec(cloud="aws",region=PINECONE_ENV)
existing_indexes=[i["name"] for i in pc.list_indexes()]


if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,
        metric="dotproduct",
        spec=spec
    )
    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)


index=pc.Index(PINECONE_INDEX_NAME)

# load,split,embed and upsert pdf docs content

def load_vectorstore(uploaded_files):
    # Validate environment variables
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY environment variable is not set")
    
    # Validate input files
    if not uploaded_files:
        raise ValueError("No files provided")
    
    # Validate file types
    for file in uploaded_files:
        if not file.filename.lower().endswith('.pdf'):
            raise ValueError(f"File {file.filename} is not a PDF")
        if not file.filename:
            raise ValueError("File has no filename")
    
    embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    file_paths = []
    
    try:
        # 1.Upload
        for file in uploaded_files:
            save_path = Path(UPLOAD_DIR) / file.filename
            with open(save_path, "wb") as f:
                f.write(file.file.read())
            file_paths.append(str(save_path))
        

        # 2. Load and Split
        for file_path in file_paths:
            loader = PyPDFLoader(file_path)
            documents = loader.load()

            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(documents)

            texts = [chunk.page_content for chunk in chunks]
            metadatas = [chunk.metadata for chunk in chunks]
            ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

            # Add text content to metadata so it can be retrieved later
            for i, metadata in enumerate(metadatas):
                metadata['text'] = texts[i]
                metadata['source'] = str(file_path)

            #3. Embed and Upsert
            print(f"🔍 Embedding {len(texts)} chunks...")
            embeddings = embed_model.embed_documents(texts)

            print("📤 Uploading to Pinecone...")
            with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
                index.upsert(vectors=zip(ids, embeddings, metadatas))
                progress.update(len(embeddings))

            print(f"✅ Upload complete for {file_path}")
            
    except Exception as e:
        # Clean up uploaded files on error
        for file_path in file_paths:
            try:
                Path(file_path).unlink(missing_ok=True)
            except:
                pass
        raise e
