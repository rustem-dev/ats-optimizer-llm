# LLM-Powered Resume Optimizer to Beat ATS Filters

## 🚀 Latest Updates - Full Cross-Platform Support

**This project has been completely updated for production deployment with Docker and cross-platform compatibility:**

### 🔧 Recent Changes:
- **✅ OpenAI API Integration**: Uses OpenAI GPT-4o model for intelligent resume optimization
- **✅ Complete Docker Setup**: Full-stack deployment with PostgreSQL database
- **✅ Cross-Platform Support**: Runs on Linux, Mac, and Windows with smart dependency handling
- **✅ Environment Variables**: Secure configuration via `.env` files
- **✅ Ubuntu/Linux Optimized**: Automated setup script for Ubuntu deployment
- **✅ Production Ready**: Health checks, volume persistence, and proper networking
- **✅ Interactive Chat Interface**: Built-in chatbot for resume refinement
- **✅ State Machine Architecture**: Robust application flow management

## 🎯 What This Project Does

This is an intelligent resume optimization system that:

1. **Analyzes Job Descriptions**: Extracts key requirements and keywords from job postings
2. **Processes User Documents**: Extracts text from uploaded resume and LinkedIn PDF exports
3. **Generates Optimized Resumes**: Uses GPT-4o to create ATS-compliant, tailored resumes
4. **Interactive Refinement**: Provides a chat interface for further customization
5. **PDF Generation**: Creates professional PDF resumes using custom HTML templates
6. **Multi-User Support**: Manages multiple users and job applications

## 🏗️ Architecture

### Core Components:
- **`app.py`**: Main Streamlit application with user interface
- **`llm_agent.py`**: OpenAI GPT-4o integration with structured output parsing
- **`state_machine.py`**: Application flow management
- **`file_management.py`**: Database operations and PDF processing
- **`templates/cv_template.html`**: Professional resume template

### Database Schema:
- **Users Table**: Stores user profiles with resume and LinkedIn data
- **Jobs Table**: Tracks job applications with generated CVs and chat history
- **PostgreSQL**: Robust data persistence with JSONB support

### Key Features:
- **Structured Output**: Uses Pydantic models for consistent resume formatting
- **PDF Processing**: PyMuPDF for text extraction from uploaded documents
- **Template Engine**: Jinja2 for dynamic HTML generation
- **PDF Rendering**: WeasyPrint for professional PDF output
- **Cross-Platform**: GTK3 runtime handling for Windows compatibility

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)
```bash
# Clone the repository
git clone https://github.com/rustem-dev/ats-optimizer-llm.git
cd ats-optimizer-llm

# Create environment file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ats_optimizer
DB_USER=ats_user
DB_PASSWORD=good_password
EOF

# Start the full stack
docker-compose up -d

# Access at http://localhost:8501
```

### Option 2: Ubuntu/Linux Local Setup
```bash
# Run automated setup (installs system dependencies)
chmod +x setup.sh
./setup.sh

# Install Python dependencies
pip install -r requirements.txt

# Start database only
cd DB && docker-compose up -d

# Run application
streamlit run app.py
```

### Option 3: Manual Setup
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt update && sudo apt install -y \
    libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 \
    libffi-dev shared-mime-info libcairo2

# Create environment file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ats_optimizer
DB_USER=ats_user
DB_PASSWORD=good_password
EOF

# Install Python dependencies
pip install -r requirements.txt

# Start application
streamlit run app.py
```

## 📋 Prerequisites

### Required Software
- **Docker & Docker Compose**: For containerized deployment
- **Python 3.11+**: For local development
- **OpenAI API Key**: Get yours at [platform.openai.com](https://platform.openai.com/api-keys)

### Docker Setup (Linux/Ubuntu)
If you encounter permission errors when running Docker commands:

```bash
# Add your user to the docker group
sudo usermod -aG docker $USER

# Apply the changes (choose one):
newgrp docker          # Apply immediately in current session
# OR
logout && login        # Logout and login to apply system-wide
```

## 🛠️ Configuration

The application uses environment variables for configuration. Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ats_optimizer
DB_USER=ats_user
DB_PASSWORD=good_password
```

## 📖 How to Use

1. **User Setup**: Enter a username and upload your resume and LinkedIn PDF exports
2. **Job Description**: Paste or upload a job description you want to target
3. **AI Processing**: The system analyzes your documents and the job requirements
4. **Generated Resume**: Review the AI-optimized resume tailored to the job
5. **Interactive Chat**: Use the chat interface to refine and customize your resume
6. **PDF Download**: Generate and download the final professional PDF resume

## 🔧 Technical Details

### LLM Integration
- **Model**: OpenAI GPT-4o
- **Structured Output**: Pydantic models ensure consistent formatting
- **Prompt Engineering**: Specialized prompts for resume optimization
- **Error Handling**: Robust error handling and validation

### Database Features
- **PostgreSQL**: Production-ready database with JSONB support
- **User Management**: Multi-user support with session persistence
- **Job Tracking**: Complete history of job applications and generated resumes
- **Chat History**: Persistent chat sessions for resume refinement

### PDF Processing
- **Text Extraction**: PyMuPDF for reliable PDF text extraction
- **Template System**: Custom HTML templates with professional styling
- **Cross-Platform**: WeasyPrint with GTK3 runtime for Windows compatibility
- **Output Management**: Organized file structure for generated PDFs

## 🚀 Deployment Options

### Docker Compose (Production)
- Full-stack deployment with PostgreSQL
- Health checks and automatic restarts
- Volume persistence for data and templates
- Network isolation and security

### Local Development
- Direct Python execution for development
- Hot reloading with Streamlit
- Local PostgreSQL database
- Easy debugging and testing

## 📝 License

This project is open source. See the original Medium article for detailed implementation guide: [Medium Link](https://medium.com/@leofgonzalez/how-i-built-an-llm-powered-resume-optimizer-to-beat-ats-filters-8ace36d5d32c)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the Medium article for detailed implementation guide
- Review the code comments for technical details
- Ensure all dependencies are properly installed
- Verify your OpenAI API key is valid and has sufficient credits

---

**TL;DR**: An intelligent, production-ready resume optimization tool that uses GPT-4o to create ATS-compliant resumes tailored to specific job descriptions, with interactive refinement capabilities and professional PDF output.
