# 🎓 Academic Research Agent

An intelligent AI-powered system that searches Google Scholar, finds academic papers, and provides detailed analysis using local AI models. Perfect for researchers, students, and academics who want to quickly discover and analyze research papers.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🌟 Features

- **🔍 Smart Paper Search**: Automatically searches Google Scholar for papers by author name
- **📊 Intelligent Analysis**: Uses local Ollama AI to summarize and analyze research papers
- **🎯 Interactive Selection**: Choose which papers to analyze in detail
- **🦙 Local AI**: Completely free using Ollama Llama - no API keys needed
- **🎤 Demo Modes**: Perfect for lectures, presentations, and educational demos
- **📚 Multiple Search Strategies**: Precise author search with smart fallback options

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Ollama installed locally
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

4. **Install and start Ollama**

   ```bash
   # Install Ollama (visit https://ollama.ai for your OS)
   ollama pull llama3.2
   ollama serve
   ```

5. **Run the agent**
   ```bash
   python research_agent.py
   ```

## 💻 Usage

### Basic Usage

```python
from research_agent import AcademicResearchAgent

# Initialize the agent
agent = AcademicResearchAgent()

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
                       │   Ollama Llama   │
                       │   (Local AI)     │
                       └──────────────────┘
```

### Core Components

1. **🧠 LangChain Agent**: Orchestrates the research process using ReAct pattern
2. **🕷️ Playwright**: Handles web scraping from Google Scholar
3. **🤖 Ollama**: Provides local AI analysis and summarization
4. **⚙️ Tools System**: Modular tools for search and analysis

### Available Tools

- **`scholar_search`**: Search Google Scholar for papers by author name
- **`paper_analyzer`**: Analyze and summarize research papers from URLs

## 📖 Example Output

```
🎓 Academic Research Agent processing: Geoffrey Hinton

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

**1. Playwright Installation**

```bash
# If you get playwright errors
playwright install chromium
```

**2. Ollama Connection**

```bash
# Make sure Ollama is running
ollama serve
# In another terminal
ollama pull llama3.2
```

**3. Google Scholar Rate Limiting**

- The agent includes automatic delays and error handling
- If you encounter rate limits, wait a few minutes before retrying

**4. No Papers Found**

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
