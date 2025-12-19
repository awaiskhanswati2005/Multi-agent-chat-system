# Multi-Agent Chat System

A sophisticated multi-agent system implementing coordinated AI agents for information retrieval, analysis, and knowledge management with persistent memory and vector search capabilities.

## 🏗️ System Architecture

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                       │
│                    (Console / Terminal)                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    COORDINATOR AGENT                         │
│  • Query Analysis & Complexity Detection                     │
│  • Task Decomposition & Agent Routing                        │
│  • Result Synthesis & Response Generation                    │
└──────┬──────────────┬──────────────┬──────────────┬─────────┘
       │              │              │              │
       ▼              ▼              ▼              ▼
┌─────────────┐ ┌──────────────┐ ┌─────────────┐ ┌─────────┐
│  RESEARCH   │ │   ANALYSIS   │ │   MEMORY    │ │ LOGGER  │
│    AGENT    │ │    AGENT     │ │    AGENT    │ │ UTILITY │
│             │ │              │ │             │ │         │
│ • Search KB │ │ • Compare    │ │ • Store     │ │ • Track │
│ • Retrieve  │ │ • Analyze    │ │ • Retrieve  │ │ • Trace │
│ • Rank      │ │ • Recommend  │ │ • Vector    │ │ • Log   │
└─────────────┘ └──────────────┘ └─────────────┘ └─────────┘
                                        │
                                        ▼
                              ┌──────────────────┐
                              │  MEMORY LAYER    │
                              │                  │
                              │ • Conversations  │
                              │ • Knowledge Base │
                              │ • Agent States   │
                              │ • Vector Store   │
                              └──────────────────┘
```

### Agent Responsibilities

#### 1. **Coordinator Agent** (Manager)
- **Query Analysis**: Determines query complexity (simple/complex/multi-step)
- **Task Routing**: Routes queries to appropriate worker agents
- **Dependency Management**: Coordinates multi-agent workflows
- **Result Synthesis**: Merges and formats responses
- **Error Handling**: Implements fallback strategies

#### 2. **Research Agent**
- **Information Retrieval**: Searches knowledge base
- **Relevance Ranking**: Scores and ranks results
- **Topic Extraction**: Identifies relevant topics
- **Mock Web Search**: Simulates external data sources

#### 3. **Analysis Agent**
- **Comparison**: Compares different approaches/techniques
- **Tradeoff Analysis**: Evaluates efficiency vs. performance
- **Pattern Identification**: Extracts common themes
- **Recommendation Generation**: Provides actionable insights

#### 4. **Memory Agent**
- **Persistent Storage**: Stores conversation and knowledge
- **Vector Search**: Implements similarity-based retrieval
- **Keyword Search**: Traditional text matching
- **Agent State Tracking**: Maintains agent learning history

## 🚀 How It Works

### Query Processing Flow

1. **User Input** → System receives natural language query
2. **Coordinator Analysis** → Determines complexity and requirements
3. **Agent Orchestration** → Routes to appropriate agents
4. **Information Processing** → Agents perform their tasks
5. **Memory Storage** → Results stored with metadata
6. **Response Synthesis** → Final answer generated
7. **User Output** → Formatted response displayed

### Memory System

The system implements a sophisticated memory layer:

- **Conversation Memory**: Full history with timestamps
- **Knowledge Base**: Persistent facts with provenance
- **Agent States**: Tracks agent learning per task
- **Vector Search**: Cosine similarity for semantic matching
- **Keyword Search**: Traditional text-based retrieval

### Decision Making

The Coordinator uses multiple strategies:

- **Simple Queries**: Direct research → response
- **Complex Queries**: Research → analysis → synthesis
- **Multi-Step Queries**: Research → analysis → recommendation → storage
- **Memory Queries**: Direct retrieval from past interactions

## 📦 Installation & Setup

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (optional)
- Git

### Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/multi-agent-chat-system.git
cd multi-agent-chat-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the system
python main.py
```

### Docker Installation

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t multi-agent-system .
docker run -it multi-agent-system
```

## 🎯 Usage Examples

### Running Test Scenarios

The system includes 5 sample test scenarios:

1. **Simple Query**
```
You: What are the main types of neural networks?
```

2. **Complex Query**
```
You: Research transformer architectures, analyze their computational efficiency, and summarize key trade-offs.
```

3. **Memory Query**
```
You: What did we discuss about neural networks earlier?
```

4. **Multi-Step Query**
```
You: Find recent papers on reinforcement learning, analyze their methodologies, and identify common challenges.
```

5. **Comparative Query**
```
You: Compare machine learning optimization techniques and recommend which is better.
```

### System Commands

- `exit` or `quit` - End session
- `memory` - View stored knowledge
- `clear` - Clear conversation history
- `help` - Display help information
- `menu` - Show sample queries

## 📁 Project Structure

```
multi-agent-chat-system/
├── agents/
│   ├── __init__.py
│   ├── coordinator.py       # Coordinator Agent
│   ├── research_agent.py    # Research Agent
│   ├── analysis_agent.py    # Analysis Agent
│   └── memory_agent.py      # Memory Agent
├── utils/
│   ├── __init__.py
│   └── logger.py            # Logging utility
├── outputs/                 # Test scenario outputs
│   ├── simple_query.txt
│   ├── complex_query.txt
│   ├── memory_test.txt
│   ├── multi_step.txt
│   └── collaborative.txt
├── logs/                    # System logs
│   └── system.log
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose config
└── README.md               # This file
```

## 🔧 Configuration

### Knowledge Base

The Research Agent uses a pre-loaded knowledge base covering:
- Neural Networks
- Machine Learning Optimization
- Transformer Architectures
- Reinforcement Learning
- Deep Learning
- Computer Vision
- Natural Language Processing

To extend the knowledge base, edit `agents/research_agent.py` and add topics to the `_initialize_knowledge_base()` method.

### Vector Search

The Memory Agent implements simple vector search using:
- Bag-of-words representation
- TF-IDF-like weighting
- Cosine similarity matching
- Configurable vocabulary (100 ML terms)

For production, replace with:
- FAISS for large-scale vector search
- Chroma for persistent vector storage
- OpenAI embeddings for better semantic understanding

### Logging

Logs are stored in `logs/system.log` with:
- Timestamps
- Agent actions
- Query/response pairs
- Error tracking

## 🧪 Testing

### Running All Test Scenarios

```python
# Option 1: Interactive mode
python main.py
# Then enter sample queries from the menu

# Option 2: Automated testing (create test_scenarios.py)
python test_scenarios.py
```

### Sample Output Structure

Each test generates output in `outputs/` directory:
- Agent collaboration traces
- Processing steps
- Final responses
- Confidence scores
- Memory operations

## 📊 Evaluation Criteria Coverage

✅ **System Architecture**
- Clear hierarchy with Coordinator → Workers
- Well-defined role boundaries
- Clean interfaces between components

✅ **Memory Design**
- Structured persistence with metadata
- Vector + keyword search
- Conversation and knowledge tracking

✅ **Agent Coordination**
- Correct task routing
- Dependency handling
- Result synthesis

✅ **Autonomous Reasoning**
- Context-aware decisions
- Adaptive memory reuse
- Confidence scoring

✅ **Code Quality**
- Modular design
- Comprehensive documentation
- Runnable containers

✅ **Traceability**
- Detailed logging
- Agent action tracking
- Decision transparency

## 🐛 Troubleshooting

### Common Issues

**Issue**: Module not found errors
```bash
# Solution: Ensure you're in the project directory
cd multi-agent-chat-system
python main.py
```

**Issue**: Docker container exits immediately
```bash
# Solution: Use interactive mode
docker run -it multi-agent-system
```

**Issue**: Logs not being created
```bash
# Solution: Create logs directory manually
mkdir logs
```

## 🚧 Future Enhancements

- [ ] Integration with real LLMs (OpenAI, Anthropic)
- [ ] Web interface with FastAPI
- [ ] Real-time collaboration features
- [ ] Advanced vector search with FAISS
- [ ] Multi-language support
- [ ] REST API endpoints
- [ ] Persistent database (PostgreSQL)
- [ ] Cloud deployment (AWS/GCP)

## 📝 License

This project is created for educational purposes as part of the Knowledge Representation and Reasoning course assignment.

## 👥 Contributors

- [Your Name] - [Your Email]
- [Team Member Name] - [Team Member Email]

## 🙏 Acknowledgments

- Air University, Faculty of Computing and AI
- Department of Creative Technologies
- Course: Knowledge Representation and Reasoning

## 📧 Contact

For questions or issues:
- GitHub Issues: [Repository URL]/issues
- Email: [Your Email]

---

**Note**: This is an academic project demonstrating multi-agent system concepts. The knowledge base and vector search implementations are simplified for educational purposes.