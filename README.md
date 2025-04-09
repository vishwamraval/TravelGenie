# TravelGenie

Welcome to **TravelGenie**, your AI-powered travel agent designed to make trip planning effortless and enjoyable.

## Features

- Personalized travel recommendations.
- Intelligent itinerary planning.
- Real-time updates and suggestions.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- Required dependencies (install via `pip install -r requirements.txt`)

### Installing Ollama and LLM Model

1. **Install Ollama**:

   - Visit [Ollama's official website](https://ollama.com)
   - Download and install the version for your operating system
   - Verify installation by running:
     ```bash
     ollama --version
     ```

2. **Pull the Llama3.1 8B Model**:
   - Open a terminal and run:
     ```bash
     ollama pull llama3.1:8b
     ```
   - Wait for the download to complete (approximately 5GB)
   - Verify the model is ready:
     ```bash
     ollama list
     ```

### Running the Application

1. **User Interface**:  
   Launch the interactive UI with the following command:

   ```bash
   streamlit run .\app.py
   ```

2. **Agent**:  
   Run the AI agent directly using:
   ```bash
   python .\agent.py
   ```
