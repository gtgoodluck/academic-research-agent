# 🎓 Academic Research Agent

An intelligent AI-powered system that searches Google Scholar, finds academic papers, and provides detailed analysis using **multiple LLM providers**. Choose between local Ollama models or cloud-based OpenAI/Anthropic for maximum flexibility.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![LLM Support](https://img.shields.io/badge/LLM-Ollama%20|%20OpenAI%20|%20Anthropic-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🌟 Features

- **🔍 Smart Paper Search**: Automatically searches Google Scholar for papers by author name
- **🤖 Multi-Provider AI**: Choose from Ollama (local), OpenAI (cloud), or Anthropic (cloud)
- **📊 Intelligent Analysis**: AI-powered paper summarization and analysis
- **🎯 Interactive Selection**: Choose which papers to analyze in detail
- **💰 Flexible Pricing**: Free local models or pay-per-use cloud models
- **🎤 Demo Modes**: Perfect for lectures, presentations, and educational demos
- **📚 Multiple Search Strategies**: Precise author search with smart fallback options
- **🔐 Secure**: API keys managed via environment variables

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Choose your AI provider:
  - **Ollama** (local, free) - Requires Ollama installation
  - **OpenAI** (cloud, paid) - Requires API key
  - **Anthropic** (cloud, paid) - Requires API key
- Chrome/Chromium browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/academic-research-agent.git
   cd academic-research-agent
   ```

2. **Set up virtual environment (recommended)**
   ```bash
   # Create virtual environment
   python -m venv research_agent_env
   
   # Activate virtual environment
   # On Windows:
   research_agent_env\Scripts\activate
   # On macOS/Linux:
   source research_agent_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Install and start Ollama**
   ```bash
   # Install Ollama (visit https://ollama.ai for your OS)
   ollama pull llama3.2
   ollama serve
   ```

4. **Run the agent**
   ```bash
   python research_agent.py
   ```

## 💻 Usage

### Basic Usage

```python
from research_agent import AcademicResearchAgent

# Option 1: Use Ollama (local, free)
agent = AcademicResearchAgent.create_ollama_agent()

# Option 2: Use OpenAI (cloud, paid)
agent = AcademicResearchAgent.create_openai_agent()

# Option 3: Use Anthropic (cloud, paid)  
agent = AcademicResearchAgent.create_anthropic_agent()

# Option 4: Custom configuration
agent = AcademicResearchAgent(
    provider="openai", 
    model="gpt-4", 
    api_key="your-key"
)

# Search for papers by an author
results = agent.research_papers_interactive("Geoffrey Hinton")
print(results["findings"])
```

### Demo Modes

The agent offers three different modes:

#### 1. 🎯 Single Research Demo
Perfect for one-off research sessions
```bash
python research_agent.py
# Select option 1
```

#### 2. 🔄 Interactive Research Mode
Research multiple academics in one session
```bash
python research_agent.py
# Select option 2
```

#### 3. 🎤 Lecture Demo Mode
Optimized for live demonstrations and presentations
```bash
python research_agent.py
# Select option 3
```

## 🛠️ How It Works

### Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Research Agent  │───▶│   Google        │
│  (Author Name)  │    │   (LangChain)    │    │   Scholar       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  AI Provider     │
                       │ Ollama/OpenAI/   │
                       │ Anthropic        │
                       └──────────────────┘
```

### Core Components

1. **🧠 LangChain Agent**: Orchestrates the research process using ReAct pattern
2. **🕷️ Playwright**: Handles web scraping from Google Scholar
3. **🤖 Multi-Provider AI**: Flexible AI backend (Ollama, OpenAI, or Anthropic)
4. **⚙️ Tools System**: Modular tools for search and analysis

### Available Tools

- **`scholar_search`**: Search Google Scholar for papers by author name
- **`paper_analyzer`**: Analyze and summarize research papers from URLs

## 🤖 **AI Provider Comparison**

| Provider | Cost | Speed | Quality | Privacy | Setup |
|----------|------|-------|---------|---------|--------|
| **Ollama** | Free | Medium | Good | Complete | Complex |
| **OpenAI** | Paid | Fast | Excellent | Shared | Simple |
| **Anthropic** | Paid | Fast | Excellent | Shared | Simple |

### **When to Use Each Provider:**

- **🦙 Ollama**: Research, education, privacy-focused work
- **🤖 OpenAI**: Production applications, high throughput
- **🧠 Anthropic**: Complex analysis, safety-critical applications

## 📖 Example Output

```
🎓 Academic Research Agent processing: Geoffrey Hinton

🔧 **Choose your AI provider:**
1. 🦙 Ollama (Local, Free)
2. 🤖 OpenAI (Cloud, Paid)  
3. 🧠 Anthropic (Cloud, Paid)

Select provider (1-3): 2
🤖 Initializing OpenAI with model: gpt-4
✅ Research agent initialized with OPENAI provider

📚 **Step 1: Finding papers by Geoffrey Hinton**

📖 Papers by Geoffrey Hinton:

1. Deep Learning
   👥 Authors: Ian Goodfellow, Yoshua Bengio, Aaron Courville
   🔗 https://www.deeplearningbook.org

2. ImageNet Classification with Deep Convolutional Neural Networks
   👥 Authors: Alex Krizhevsky, Ilya Sutskever, Geoffrey E Hinton
   🔗 https://papers.nips.cc/paper/4824-imagenet-classification

📋 **Step 2: Choose a paper to analyze in detail**
Found 8 paper(s). Which would you like me to analyze?

1. Deep Learning
2. ImageNet Classification with Deep Convolutional Neural Networks
...
9. Skip detailed analysis

Enter your choice (1-9): 2

📄 **Step 3: Analyzing selected paper**
🎯 **Selected:** ImageNet Classification with Deep Convolutional Neural Networks

📋 **Paper Analysis:**

1. **Main Research Problem**: The paper addresses image classification on the ImageNet dataset using deep convolutional neural networks...

2. **Key Methodology**: The authors employed a deep CNN with multiple convolutional and pooling layers...

3. **Major Findings**: Achieved top-1 error rate of 37.5% and top-5 error rate of 17.0%...

4. **Significance**: This work demonstrated the power of deep learning for computer vision...
```

## 🎯 Use Cases

### For Researchers
- Quickly find relevant papers by leading authors
- Get AI-powered summaries of complex research
- Discover new papers in your field

### For Students
- Research prominent academics for assignments
- Understand complex papers through AI analysis
- Learn about research trends and methodologies

### For Educators
- Live demonstrations of AI research capabilities
- Interactive classroom activities
- Teaching research methodology

## ⚙️ Configuration

### Customizing the AI Model

```python
# In AcademicResearchAgent.__init__()
self.llm = Ollama(
    model="llama3.2",      # Change model here
    temperature=0.1        # Adjust creativity (0.0 = factual, 1.0 = creative)
)
```

### Search Parameters

```python
# Number of papers to find
valid_papers < 8  # Modify this limit

# Search timeout
timeout=15000  # Modify timeout in milliseconds
```

## 🔧 Advanced Features

### Custom Search Strategies

The agent employs intelligent name matching:

```python
name_variations = [
    author_name.lower(),                    # "geoffrey hinton"
    author_name_parts[-1],                  # "hinton" 
    f"{author_name_parts[0][0]} {author_name_parts[-1]}"  # "g hinton"
]
```

### Fallback Search

If the precise search fails, the agent automatically tries a broader search approach.

### Content Extraction

Multiple extraction strategies for different paper formats:

```python
content_selectors = [
    '.ltx_abstract',  # arXiv papers
    '#abstract',      # Journal papers  
    '.abstract',      # Generic abstracts
    'article p',      # Article paragraphs
    'p'               # Fallback: any paragraphs
]
```

## 🗺️ Roadmap

- [x] **v1.0**: Multi-provider CLI agent (Ollama, OpenAI, Anthropic)
- [ ] **v1.1**: FastAPI web server with REST endpoints  
- [ ] **v1.2**: Python client library for API integration
- [ ] **v1.3**: Web frontend interface
- [ ] **v1.4**: Database integration and result persistence

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama Team** for providing free local AI models
- **LangChain** for the excellent agent framework
- **Playwright** for reliable web automation
- **Google Scholar** for academic paper access

## 🐛 Troubleshooting

### Common Issues

**3. Playwright Installation**
```bash
# If you get playwright errors
playwright install chromium
```

**4. API Key Issues**
```bash
# Make sure your .env file contains:
OPENAI_API_KEY=your_actual_key_here
ANTHROPIC_API_KEY=your_actual_key_here

# Or set environment variables directly:
export OPENAI_API_KEY=your_key_here
```

**5. Ollama Connection**
```bash
# Make sure Ollama is running
ollama serve
# In another terminal
ollama pull llama3.2
```

**6. Google Scholar Rate Limiting**
- The agent includes automatic delays and error handling
- If you encounter rate limits, wait a few minutes before retrying

**7. No Papers Found**
- Try alternative spellings of the author name
- Check if the author has a Google Scholar profile
- Use the broader search fallback option

## 📊 Performance

- **Search Speed**: ~2-5 seconds per author search
- **Analysis Speed**: ~10-30 seconds per paper (depends on paper length)
- **Memory Usage**: ~200-500MB (including browser)
- **Success Rate**: ~85% for authors with Google Scholar profiles

## 🔮 Future Enhancements

- [ ] Web interface using FastAPI/Streamlit
- [ ] PDF download and local analysis
- [ ] Citation network visualization
- [ ] Multi-language support
- [ ] Integration with reference managers (Zotero, Mendeley)
- [ ] Batch processing for multiple authors
- [ ] Export to various formats (PDF, Excel, BibTeX)

---

**Happy Researching!** 🎉

For questions, issues, or feature requests, please open an issue on GitHub.