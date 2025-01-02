
# P-Reasoner: Reasoning on Demand for LLM Models

Welcome to **P-Reasoner**, a chatbot framework designed to add reasoning abilities to language models, even the simplest ones. This project showcases how reasoning can be introduced to enhance accuracy and functionality while keeping API costs low.

## Features
- **Reasoning Mode**: A toggleable feature that adds structured reasoning steps, enabling models to perform better on complex tasks.
- **Customizable Backend**: Users can modify the language models used via OpenRouter-supported APIs.
- **Interactive Frontend**: A fun and engaging chatbot interface built with HTML, CSS, and Flask.
- **Open-Source**: Fully customizable and open to contributions.

---

## Directory Structure
```plaintext
ArshA03-P-Reasoner/
├── README.md              # This file
├── pyproject.toml         # Python project configuration
├── env/
│   └── .env_CHANGE        # Template for API keys (rename to .env)
├── src/
│   ├── app.py             # Flask application
│   ├── backend/
│   │   └── chatbot.py     # Chatbot logic
│   └── frontend/
│       ├── static/
│       │   ├── css/
│       │   │   ├── animations.css
│       │   │   └── style.css
│       │   └── js/
│       │       └── main.js
│       └── templates/
│           └── index.html # Chatbot frontend template
└── tests/
    ├── configure_openai.py
    ├── convo_class.py
    ├── multi_agent.py
    ├── reason_advanced.py
    ├── reason_advanced2.py
    └── reasoning_advanced3.py
```

---

## Getting Started

### Prerequisites
1. **Python**: Version 3.12 or later.
2. **API Key**: Obtain an OpenRouter API key from [OpenRouter](https://openrouter.ai/).

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ArshA03/P-Reasoner.git
   cd ArshA03-P-Reasoner
   ```
2. Install dependencies using [Poetry](https://python-poetry.org/):
   ```bash
   poetry install
   ```
3. Configure the `.env` file:
   - Navigate to the `env` folder.
   - Rename `.env_CHANGE` to `.env`:
     ```bash
     mv env/.env_CHANGE env/.env
     ```
   - Add your API key in the `.env` file:
     ```
     API_KEY=your_openrouter_api_key
     ```

---

### Running the Chatbot
1. Start the Flask application:
   ```bash
   poetry run python src/app.py
   ```
2. Access the chatbot in your web browser at:
   ```
   http://127.0.0.1:5000
   ```

---

## Using the Chatbot
- **Send Messages**: Type your message in the input box and click the send button.
- **Toggle Reasoning Mode**: Enable or disable reasoning by using the switch at the top-right corner of the chat interface.
- **Customize Models**: Edit `src/backend/chatbot.py` to use different OpenRouter-supported models for both reasoning and supervision.

---

## Showcase Video
Check out the video demonstration to see the chatbot in action. The reasoning mode enables GPT-3.5 Turbo to correctly solve the question: *"Which is greater, 9.9 or 9.11?"*

---

## Future Work
- Benchmarking performance in reasoning mode.
- Adding support for more complex tasks and use cases.

---

## Contributing
Contributions are welcome! Feel free to fork the repository, submit pull requests, or raise issues.

---

## License
This project is open-sourced under the MIT License.

---

Enjoy exploring P-Reasoner! 🚀
