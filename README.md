# AI Chatbot Version 2 (Professional Implementation)

This project is a modular, secure, and production-ready terminal AI assistant powered by the Groq API and Llama 3 model. It was developed as part of the Generative AI Internship at Borlo Labs.

## Features
* **Secure API Handling:** Uses environment variables to protect sensitive API keys.
* **Modular Code Structure:** Cleanly separated functions for handling UI, input, commands, and API requests.
* **Command System:** Built-in terminal commands (`/exit`, `/clear`, `/history`, `/save`) that operate without making API calls.
* **Conversation Memory Limit:** Automatically manages context window by keeping only the 10 most recent conversational exchanges.
* **Robust Error Handling:** `try-except` blocks prevent crashes from KeyboardInterrupts (Ctrl+C) and network failures.

---
## Setup Instructions

### 1. Install Dependencies
This project requires Python 3.10 or higher. You will need to install the required external libraries using pip:
```bash
pip install groq python-dotenv

2. Set the Environment Variable (API Key)
For security, this application does not hardcode the API key. You must set up a local environment variable.

In the root directory of this project, create a new file named exactly .env
Open the .env file and add your Groq API key in the following format:
      GROQ_API_KEY=your_actual_api_key_here
⚠️ SECURITY WARNING: Never upload your .env file or expose your API key to GitHub. Ensure .env is listed in your .gitignore file.

3. Run the Program
Once the dependencies are installed and the .env file is saved, you can run the chatbot from your terminal:
  ```bash
      python main.py

Available Commands
While chatting with the AI, you can use the following commands to manage the application:

/exit - Safely close the chatbot.

/clear - Wipe the conversation memory to start fresh.

/history - Display the full text of the current session's history.

/save - Export the current conversation to a local chat_history.txt file.

Author:  Pirbhu Ji
Project: Borlo Labs Generative AI Internship
