# LLM-Powered Resume Optimizer to Beat ATS Filters

## 🚀 Recent Updates - OpenAI Integration

**This fork has been updated to use OpenAI API instead of Groq LLM for enhanced compatibility and performance:**

### Changes Made:
- **✅ OpenAI API Integration**: Replaced Groq LLM with OpenAI GPT-4o model
- **✅ Environment Variables**: Removed hardcoded API key paths, now uses `OPENAI_API_KEY` environment variable
- **✅ Cross-Platform Support**: Fixed Windows-specific paths for better compatibility across Linux, Mac, and Windows
- **✅ Improved Security**: API keys are now handled through environment variables instead of local files
- **✅ Updated Dependencies**: Updated `requirements.txt` with OpenAI-related packages

### Quick Setup:
1. Set your OpenAI API key: `export OPENAI_API_KEY=your_api_key_here`
2. Copy `.env.example` to `.env` and add your API key
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `streamlit run app.py`

---

## Original Project Description

Automates resume generation and optimization by analyzing job descriptions, user resumes, and LinkedIn exports. The system uses a modular architecture with Python, PostgreSQL (via Docker), and LangChain with OpenAI's GPT-4o and Pydantic's accuracy to produce high-quality, ATS-compliant resume PDFs.

Medium Article with the complete guide and walkthrough: [Medium Link](https://medium.com/@leofgonzalez/how-i-built-an-llm-powered-resume-optimizer-to-beat-ats-filters-8ace36d5d32c)


# Key Sections Covered in the Medium Guide:

Local Setup & UI Flow: Simple, privacy-first Streamlit interface with support for multiple job versions and chat-based interaction.

LLM Integration: Structured resume output via LLaMA 3.3 and LangChain’s Pydantic parsing system.

PDF Rendering: Dynamic Jinja2 HTML template rendered with WeasyPrint.

Database Design: Dockerized PostgreSQL storing users, job inputs, LLM outputs, and chat history.

Future Improvements: Rate limiting, project sections, Ollama summarization for job titles, and ATS scoring features.

# TL;DR

An open-source resume tailoring tool that helps candidates pass automated filters and better match job expectations using local workflows, LLMs, and clean design.

For a detailed walkthrough, check out the Medium article linked above.
