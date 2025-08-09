# RAG Agent - Intelligent Document Query System

A LLM-Powered Intelligent Query–Retrieval System that uses Large Language Models (LLMs) to process natural language queries and retrieve relevant information from large unstructured documents such as policy documents, contracts, and emails.

## 🚀 Features

- **Document Processing**: Upload and process PDF documents
- **Semantic Search**: Vector-based document retrieval using Pinecone
- **AI-Powered Analysis**: Insurance/policy analysis using Groq LLM
- **Interactive Chat Interface**: Streamlit-based user interface
- **Real-time Query Processing**: Fast response times with cloud-based infrastructure
- **Source Attribution**: Track and display document sources for responses

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Uvicorn
- **Vector Database**: Pinecone (AWS infrastructure)
- **Embeddings**: Google Generative AI (models/embedding-001)
- **LLM**: Groq (llama3-70b-8192)
- **Document Processing**: PyPDF for PDF parsing
- **Deployment**: Render cloud platform

### Frontend (Streamlit)
- **Framework**: Streamlit
- **Components**: Chat interface, file upload, history download
- **Session Management**: Built-in session state for chat history

## 🛠️ Technology Stack

### Cloud Services
- **Vector Database**: Pinecone (AWS)
- **Embeddings**: Google Cloud AI
- **LLM**: Groq
- **Backend Hosting**: Render
- **Region**: us-east-1

### Core Libraries
- **FastAPI**: Web framework
- **LangChain**: LLM orchestration
- **Streamlit**: Frontend interface
- **Pinecone**: Vector database
- **PyPDF**: PDF processing

## 📋 Prerequisites

- Python 3.13+
- Google Cloud API key
- Pinecone API key
- Groq API key

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd RAG_AGENT
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory (same level as README.md):
```env
# Google Cloud AI API Key for embeddings
GOOGLE_API_KEY=your_google_api_key_here

# Pinecone Vector Database API Key
PINECONE_API_KEY=your_pinecone_api_key_here

# Groq LLM API Key
GROQ_API_KEY=your_groq_api_key_here

# Pinecone Configuration
PINECONE_INDEX_NAME=rag-agent
PINECONE_ENV=us-east-1
```

**Important**: The `.env` file is already in `.gitignore` to keep your API keys secure. Never commit this file to version control.

### 3. Install Dependencies

#### Backend Dependencies
```bash
cd Backend
pip install -r requirements.txt
```

#### Frontend Dependencies
```bash
cd client
uv pip install -r requirements.txt
```

### 4. Run the Application

#### Start Backend Server
```bash
cd Backend
uvicorn main:app --host 0.0.0.0 --port 10000
```

#### Start Frontend Application
```bash
cd client
streamlit run app.py
```

## 📖 Usage Guide

### 1. Upload Documents
- Navigate to the sidebar in the Streamlit interface
- Click "Upload documents (.PDFs)"
- Select one or more PDF files
- Click "Upload DB" to process and index documents

### 2. Ask Questions
- Use the chat interface to ask questions about your documents
- The system will:
  - Process your query
  - Search through document embeddings
  - Retrieve relevant context
  - Generate AI-powered responses
  - Provide source attribution

### 3. Download Chat History
- Use the download button to save your conversation history
- Chat history is maintained in session state

## 🔧 API Endpoints

### Upload Documents
```
POST /upload_pdfs/
Content-Type: multipart/form-data
Body: files (PDF files)
```

### Ask Questions
```
POST /ask/
Content-Type: application/x-www-form-urlencoded
Body: question (string)
```

## 🏛️ Project Structure

```
RAG_AGENT/
├── Backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Backend dependencies
│   ├── modules/
│   │   ├── load_vectorstore.py # Document processing
│   │   ├── llm.py             # LLM chain setup
│   │   ├── query_handlers.py  # Query processing
│   │   └── pdf_handlers.py    # PDF utilities
│   ├── routes/
│   │   ├── upload_pdfs.py     # Upload endpoints
│   │   └── ask_questions.py   # Query endpoints
│   └── middlewares/
│       └── exception_handlers.py
├── client/
│   ├── app.py                 # Streamlit main app
│   ├── requirements.txt       # Frontend dependencies
│   ├── components/
│   │   ├── chatUI.py         # Chat interface
│   │   ├── upload.py         # File upload
│   │   └── history_download.py
│   ├── utils/
│   │   └── api.py            # API utilities
│   └── config.py             # Configuration
├── pyproject.toml            # Project metadata
└── README.md                # This file
```

## 🔍 How It Works

### 1. Document Processing Pipeline
1. **Upload**: PDF files are uploaded via Streamlit interface
2. **Parsing**: PyPDF extracts text content from PDFs
3. **Chunking**: Text is split into 500-character chunks with 50-character overlap
4. **Embedding**: Google AI generates 768-dimensional embeddings
5. **Storage**: Embeddings and metadata are stored in Pinecone vector database

### 2. Query Processing Pipeline
1. **Query Input**: User submits natural language question
2. **Query Embedding**: Question is converted to vector representation
3. **Semantic Search**: Pinecone retrieves top 3 most similar document chunks
4. **Context Assembly**: Retrieved chunks are assembled as context
5. **LLM Processing**: Groq LLM analyzes context and generates response
6. **Response Delivery**: Structured response with source attribution

## 🎯 Use Cases

### Insurance Policy Analysis
- Coverage determination
- Claim processing guidance
- Policy interpretation
- Compliance checking

### Document Q&A
- Contract analysis
- Legal document review
- Technical documentation
- Research paper analysis

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_API_KEY` | Google Cloud AI API key | Yes | - |
| `PINECONE_API_KEY` | Pinecone vector database API key | Yes | - |
| `GROQ_API_KEY` | Groq LLM API key | Yes | - |
| `PINECONE_INDEX_NAME` | Pinecone index name | Yes | rag-agent |
| `PINECONE_ENV` | Pinecone environment region | No | us-east-1 |
| `UPLOAD_DIR` | Local directory for uploaded files | No | ./uploaded_docs |

### Vector Database Settings
- **Dimension**: 768 (Google AI embeddings)
- **Metric**: dotproduct
- **Cloud**: AWS (via Pinecone)
- **Region**: us-east-1

## 🚀 Deployment

### Backend Deployment (Render)
1. Connect your GitHub repository to Render
2. Configure environment variables
3. Set build command: `pip install -r Backend/requirements.txt`
4. Set start command: `uvicorn Backend.main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment
- Deploy Streamlit app to Streamlit Cloud
- Configure API URL to point to deployed backend

## 🔒 Security Considerations

- API keys are stored as environment variables
- CORS is configured for cross-origin requests
- File uploads are restricted to PDF format
- Exception handling prevents information leakage

## 📊 Performance

- **Embedding Generation**: ~1-2 seconds per document
- **Query Response**: ~3-5 seconds
- **Vector Search**: Sub-second retrieval
- **Concurrent Users**: Limited by API rate limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs` endpoint
2. Review the logs for error messages
3. Verify environment variables are set correctly
4. Ensure API keys have sufficient quotas

## 🔄 Version History

- **v0.1.0**: Initial release with basic RAG functionality
  - PDF document processing
  - Semantic search with Pinecone
  - Groq LLM integration
  - Streamlit frontend
