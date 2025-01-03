
# P-Reasoner: AI-Powered Reasoning Assistant

P-Reasoner is an advanced chatbot application that enhances Large Language Models (LLMs) with structured reasoning capabilities. It employs a unique dual-agent architecture featuring an Assistant and a Supervisor to provide more thorough and well-reasoned responses.

## Features

- 🧠 **Dual-Agent Architecture**: Utilizes both an Assistant and a Supervisor model for enhanced reasoning
- 💭 **Structured Problem Solving**: Breaks down complex problems into manageable steps
- 🔄 **Interactive Mode**: Toggle between standard chat and advanced reasoning modes
- 🎨 **Modern UI**: Clean, responsive interface with real-time message updates
- 🔍 **Critical Analysis**: Continuous evaluation and refinement of responses

## Prerequisites

- Python 3.12 or higher
- Poetry package manager
- OpenRouter API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/P-Reasoner.git
cd P-Reasoner
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up your environment:
   - Navigate to the `env` folder
   - Rename `.env_CHANGE` to `.env`
   - Add your OpenRouter API key:
```
API_KEY=your_openrouter_api_key_here
```

## Configuration

The project uses OpenRouter API for model access. You can modify the models used in `src/backend/chatbot.py`:

```python
self.assistant_model = "anthropic/claude-3.5-haiku"  # Change as needed
self.supervisor_model = "openai/gpt-4o-mini"        # Change as needed
```

Available models can be found on [OpenRouter's website](https://openrouter.ai/docs).

## Running the Application

1. Activate the Poetry environment:
```bash
poetry shell
```

2. Start the Flask server:
```bash
python src/app.py
```

3. Access the application at `http://localhost:5000`

## Using P-Reasoner

1. **Standard Mode**: 
   - Type your message and press enter or click send
   - Receive direct responses from the Assistant model

2. **Reasoning Mode**:
   - Toggle the "Reasoning Mode" switch in the UI
   - Messages will be processed through the dual-agent architecture
   - The Supervisor will guide the Assistant through structured reasoning steps
   - Final responses will be more thorough and well-reasoned

## Project Structure

```
ArshA03-P-Reasoner/
├── src/                  # Source code
│   ├── app.py           # Flask application
│   ├── backend/         # Backend logic
│   └── frontend/        # Frontend assets
├── tests/               # Test files
├── env/                 # Environment configuration
└── pyproject.toml       # Project dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

Added Soon!
