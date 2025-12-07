# MCP Server LLM - FastAPI Backend

A powerful FastAPI-based backend for multi-agent LLM interactions with support for document processing, web search, Firebase integration, and multiple AI model providers.

## 🚀 Features

- **Multi-Agent System**: 6 specialized virtual expert agents (SQL, AI/ML, Android, Web, DevOps, Blockchain)
- **Multiple LLM Providers**: Google Gemini, Groq, OpenRouter
- **Document Processing**: PDF text extraction and OCR with Tesseract
- **Vector Search**: FAISS-based semantic search with sentence transformers
- **Web Search Integration**: DuckDuckGo web search API
- **Firebase Integration**: Real-time chat storage and user management
- **Streaming Support**: Real-time response streaming for long-running queries
- **File Upload**: Cloudinary integration for file management

## 📋 Prerequisites

- Python 3.12 or higher
- Virtual environment (`venv` or `uv`)
- API keys for:
  - Google Generative AI (Gemini)
  - Groq (optional)
  - OpenRouter (optional)
  - Cloudinary (optional)
  - Firebase credentials

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/abhilashpatra04/mcp-server-llm.git
cd mcp-server-llm
```

### 2. Create Virtual Environment

Using `venv`:
```bash
python -m venv promtenv
.\promtenv\Scripts\Activate.ps1  # On Windows PowerShell
# or
source promtenv/bin/activate     # On macOS/Linux
```

Using `uv` (faster):
```bash
uv venv promtenv
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install System Dependencies

**For OCR (Tesseract):**

**Windows:**
```powershell
# Using Chocolatey
choco install tesseract

# Or download from: https://github.com/UB-Mannheim/tesseract/wiki
```

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

### 5. Environment Configuration

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Then edit `.env` with your API keys (see [Environment Variables](#environment-variables) section).

## 📝 Environment Variables

Create a `.env` file with the following variables:

```env
# Google Generative AI (Gemini)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=path/to/firebase-service-account.json

# Groq API (optional)
GROQ_API_KEY=your_groq_api_key_here

# OpenRouter API (optional)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Cloudinary (optional, for file uploads)
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name

# Firebase
FIREBASE_PROJECT_ID=your_firebase_project_id
```

See `.env.example` for all available options.

## 🚀 Running the Server

### Development Mode (with auto-reload)

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Health Check
```bash
GET /health
```

### Chat Endpoint
```bash
POST /chat
Content-Type: application/json

{
  "message": "Your question here",
  "chat_id": "unique_chat_id",
  "user_id": "user_id",
  "agent": "sql",  // or: "ai_ml", "android", "web", "devops", "blockchain"
  "model": "gemini-1.5-pro",  // or: "groq", "openrouter"
  "stream": true,
  "user_api_keys": {
    "openrouter": "optional_custom_api_key"
  }
}
```

**Response (Streaming):**
```
data: {"content": "chunk of response"}
data: {"content": "more content"}
...
```

## 🏗️ Project Structure

```
mcp_server_llm/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration and constants
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project metadata
├── .env.example           # Environment variables template
├── chains/
│   └── base_chat.py       # Chat router and virtual agents
├── tools/
│   ├── firestore_tool.py  # Firestore database operations
│   └── web_search_tool.py # Web search integration
├── utils/
│   ├── model_loader.py    # LLM provider interfaces
│   ├── firebase_utils.py  # Firebase utilities
│   ├── context_utils.py   # Text/PDF extraction
│   ├── pdf_vector_store.py # Vector search setup
│   └── web_scraper.py     # Web scraping utilities
└── vectorstores/          # FAISS vector indices (git-ignored)
```

## 🤖 Virtual Expert Agents

The system includes 6 pre-configured expert agents:

1. **SQL Expert**: Database design, optimization, and query assistance
2. **AI/ML Expert**: Machine learning, deep learning, and AI concepts
3. **Android Expert**: Android development, Kotlin, Jetpack libraries
4. **Web Expert**: Web development, frameworks, and best practices
5. **DevOps Expert**: Infrastructure, deployment, and CI/CD
6. **Blockchain Expert**: Blockchain development and Web3

Each agent has specialized system prompts and knowledge bases.

## 🔐 Security Notes

⚠️ **Important**: 
- Never commit `.env` files or credentials to version control
- Rotate API keys regularly
- Use environment variables for all sensitive data
- Firebase credentials should be restricted to service accounts only

## 🚀 Deployment

### Using Heroku

```bash
heroku create your-app-name
heroku config:set GOOGLE_API_KEY=your_key
git push heroku main
```

### Using Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Railway, Render, or Vercel

Simply connect your GitHub repository and add environment variables in the dashboard.

## 📦 Dependencies

Key dependencies:
- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **google-generativeai**: Google Gemini API
- **langchain**: LLM orchestration
- **sentence-transformers**: Text embeddings
- **faiss-cpu**: Vector search
- **google-cloud-firestore**: Database
- **pdfplumber**: PDF processing
- **pytesseract**: OCR
- **duckduckgo-search**: Web search

See `requirements.txt` for complete list with versions.

## 🧪 Testing

Run tests with pytest:

```bash
pytest tests/ -v
```

## 📊 Monitoring

The application logs are available in:
- Console output (development mode)
- Firebase Realtime Logs (production)

## 🐛 Troubleshooting

### Import Errors
If you encounter import errors:
```bash
pip install --upgrade google-generativeai langchain langchain-text-splitters
```

### Tesseract Not Found
Ensure Tesseract is installed and in your PATH. Check:
```bash
tesseract --version
```

### API Key Issues
Verify all required API keys are set:
```bash
python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"
```

### Port Already in Use
Use a different port:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author

Abhilash Patra

## 🔗 Links

- [GitHub Repository](https://github.com/abhilashpatra04/mcp-server-llm)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Langchain Documentation](https://python.langchain.com/)
- [Google Generative AI](https://ai.google.dev/)

## 💬 Support

For issues and questions, please open a GitHub issue.

---

**Last Updated**: December 2024
**Status**: ✅ Production Ready
