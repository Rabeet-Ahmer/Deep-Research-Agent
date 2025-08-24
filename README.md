# Deep-Research-Agent
=======
# 🚀 Deep Research Agent

A comprehensive AI-powered research automation system that generates detailed reports by orchestrating multiple specialized agents to search, analyze, and synthesize information from the web.

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

The Deep Research Agent is an intelligent research automation system that combines multiple AI agents to conduct comprehensive research on any given topic. It automatically generates search queries, searches the web, analyzes sources, and synthesizes professional reports with proper citations and formatting.

### What It Does

1. **🔍 Query Generation**: Creates focused search queries based on research topics
2. **🌐 Web Search**: Searches multiple sources using DuckDuckGo
3. **📖 Source Analysis**: Analyzes and summarizes web content
4. **📝 Report Synthesis**: Generates comprehensive markdown reports
5. **📊 Real-time Progress**: Shows research progress with streaming updates

## ✨ Key Features

- **🤖 Multi-Agent Architecture**: Specialized agents for each research phase
- **🌐 Intelligent Web Search**: Smart query generation and source discovery
- **📖 Content Analysis**: AI-powered content summarization and analysis
- **📝 Professional Reports**: Markdown-formatted reports with citations
- **🔄 Streaming Updates**: Real-time progress tracking in Chainlit
- **📱 Web Interface**: Beautiful Chainlit-based web interface

## 🏗️ Architecture

The system uses a coordinator pattern with specialized agents:

```
User Input → Coordinator → Query Agent → Search Agent → Synthesis Agent → Final Report
                ↓
        Progress Streaming → Chainlit UI
```

### Core Components

- **ResearchCoordinator**: Orchestrates the entire research workflow
- **QueryAgent**: Generates focused search queries and research strategy
- **SearchAgent**: Analyzes web content and extracts summaries
- **SynthesisAgent**: Creates comprehensive research reports
- **Chainlit Interface**: Web-based user interface with streaming updates

## 🚀 Installation

### Prerequisites

- Python 3.8+
- OpenAI API key or Gemini API key
- Internet connection for web searches

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/deep-research-agent.git
   cd deep-research-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Run the application**
   ```bash
   chainlit run chainlit_app.py
   ```

### Alternative Installation with uv

```bash
# Install uv if you don't have it
pip install uv

# Install dependencies
uv sync

# Run the application
uv run chainlit run chainlit_app.py
```

## 📖 Usage

### Web Interface (Recommended)

1. **Start the application**
   ```bash
   chainlit run chainlit_app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8000`

3. **Enter a research topic** in the chat interface

4. **Watch the research process** unfold in real-time with streaming updates

5. **Get your comprehensive report** with sources and citations

### Command Line Interface

```bash
# Run research from command line
python cli_app.py "Your research topic here"
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY = your-openai-api-key
or
GEMINI_API_KEY = your-gemini-api-key
```

### Configuration File

Modify `config.py` to customize agent behavior:

```python
# Agent model configuration
agent_model = "gpt-4"

# Search parameters
max_search_results = 3
search_timeout = 30

# Report formatting
report_format = "markdown"
include_citations = True
```

## 📁 Project Structure

```
deep-research-agent/
├── chainlit_app.py          # Main web interface
├── coordinator.py            # Research workflow coordinator
├── config.py                # Configuration settings
├── cli_app.py              # Command line interface
├── pyproject.toml          # Project dependencies
├── uv.lock                 # Locked dependencies
├── research_agents/        # Specialized agent modules
│   ├── __init__.py
│   ├── query_agent.py      # Query generation agent
│   ├── search_agent.py     # Web content analysis agent
│   ├── synthesis_agent.py  # Report generation agent
│   └── main_agent.py       # Main orchestration agent
└── README.md               # This file
```


## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/yourusername/deep-research-agent.git
cd deep-research-agent
pip install -e .
pip install -r requirements-dev.txt
```

## 📝 License

This project is licensed under the MIT License

## 🙏 Acknowledgments

- **OpenAI Agents SDK** for providing the AI framework
- **Chainlit** for the beautiful web interface framework
- **DuckDuckGo** for web search capabilities
- **BeautifulSoup** for web scraping functionality

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/deep-research-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/deep-research-agent/discussions)
- **Email**: rabeetahmer9749@gmail.com

**Made with ❤️ by Me**

*Transform your research process with AI-powered automation!*
