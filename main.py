"""
AI Chatbot Version 2 - Professional Implementation
A modular, secure terminal-based AI assistant using the Groq API.
"""

import os, sys
from dotenv import load_dotenv
from groq import Groq

def initialize_client():
    """Loads environment variables and securely initializes the Groq API client."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("\n[ERROR] GROQ_API_KEY missing in .env file.")
        sys.exit(1)
        
    return Groq(api_key=api_key)

def print_banner():
    """Displays the startup interface and available terminal commands."""
    print(f"\n{'='*40}\nAI ASSISTANT TERMINAL\n{'='*40}")
    print("Commands: /exit, /clear, /history, /save\n" + "-"*40)

def get_user_input():
    """Safely captures user input, handling forced keyboard interruptions (Ctrl+C)."""
    try:
        return input("\nYou: ").strip()
    except (KeyboardInterrupt, EOFError):
        return "/exit"

def handle_commands(cmd, messages):
    """
    Intercepts and processes system commands locally without making API calls.
    Returns a tuple: (is_command_handled, should_exit_program)
    """
    cmd = cmd.lower()
    
    if cmd == "/exit":
        print("\nGoodbye!")
        return True, True
        
    elif cmd == "/clear":
        # Delete all conversation history except the initial system prompt
        del messages[1:] 
        print("\n[System] Memory cleared.")
        return True, False
        
    elif cmd == "/history":
        print("\n--- History ---")
        for m in messages[1:]:
            print(f"{'You' if m['role']=='user' else 'AI'}: {m['content']}")
        return True, False
        
    elif cmd == "/save":
        try:
            with open("chat_history.txt", "w", encoding="utf-8") as f:
                for m in messages[1:]:
                    f.write(f"{'You' if m['role']=='user' else 'AI'}: {m['content']}\n\n")
            print("\n[System] Saved to chat_history.txt")
        except Exception as e:
            print(f"\n[Error] Failed to save file: {e}")
        return True, False
        
    elif cmd.startswith("/"):
        print(f"\n[System] Unknown command: {cmd}")
        return True, False
        
    return False, False

def generate_response(client, messages):
    """Sends the conversation history to the Llama 3 model and catches network errors."""
    try:
        res = client.chat.completions.create(
            messages=messages, 
            model="llama-3.3-70b-versatile", 
            temperature=0.7
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"[API ERROR] {e}"

def main():
    """Main application loop managing initialization, user input, and API interactions."""
    client = initialize_client()
    print_banner()
    
    # Initialize memory with the core system prompt
    messages = [{"role": "system", "content": "You are a professional AI assistant."}]

    while True:
        user_input = get_user_input()
        if not user_input: 
            continue

        # Route input through the command handler first
        is_cmd, should_exit = handle_commands(user_input, messages)
        if should_exit: 
            break
        if is_cmd: 
            continue

        messages.append({"role": "user", "content": user_input})

        # Memory Management: Retain system prompt (index 0) + last 10 exchanges (20 items)
        while len(messages) > 21:
            del messages[1:3] 

        # Fetch and display the AI's response
        reply = generate_response(client, messages)
        print(f"\nAI: {reply}")

        # Store response in memory unless an API error occurred
        if "[API ERROR]" not in reply:
            messages.append({"role": "assistant", "content": reply})
        else:
            messages.pop() # Remove the user's last message so the flow isn't broken

if __name__ == '__main__':
    main()
    