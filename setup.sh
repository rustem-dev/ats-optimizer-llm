#!/bin/bash

# ATS Optimizer Setup Script for Ubuntu/Linux

echo "🚀 Setting up ATS Optimizer on Ubuntu..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first:"
    echo "   sudo apt update && sudo apt install docker.io docker-compose"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first:"
    echo "   sudo apt update && sudo apt install docker-compose"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your OpenAI API key!"
    echo "   OPENAI_API_KEY=your_actual_api_key_here"
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p output templates

# Check if templates directory has content
if [ ! -f templates/cv_template.html ]; then
    echo "⚠️  Warning: templates/cv_template.html not found"
    echo "   Make sure to add your CV template file"
fi

# Install WeasyPrint system dependencies for local development
echo "📦 Installing WeasyPrint system dependencies..."
sudo apt update
sudo apt install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libcairo2 \
    python3-dev \
    python3-pip

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your OpenAI API key"
echo "2. Start with Docker: docker-compose up -d"
echo "3. Or install Python deps: pip install -r requirements.txt"
echo "4. For local run: streamlit run app.py"
echo ""
echo "Access the app at: http://localhost:8501"