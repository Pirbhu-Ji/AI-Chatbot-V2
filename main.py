import os
import sys
from dotenv import load_dotenv
from groq import Groq

def initialize_client():
    """Loads the API key and initializes the Groq client securely."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("\n[ERROR] GROQ_API_KEY not found!")
        print("Please ensure you have a .env file with your API key set.")
        sys.exit(1)
        
    return Groq(api_key=api_key)

def print_banner():
    """Displays the startup banner and available commands."""
    print("=" * 50)
    print("      PROFESSIONAL AI ASSISTANT TERMINAL")
    print("=" * 50)
    print("Session Started...")
    print("Commands Available:")
    print("  /exit    - Close the chatbot")
    print("  /clear   - Clear conversation memory")
    print("  /history - Display conversation history")
    print("  /save    - Save conversation to a .txt file")
    print("-" * 50)

def get_user_input():
    """Gets user input safely."""
    try:
        return input("\nYou: ").strip()
    except (KeyboardInterrupt, EOFError):
        # Handles cases where the user presses Ctrl+C to force quit
        return "/exit"

def handle_commands(user_input, messages):
    """Processes user commands. Returns a tuple: (is_command_handled, should_exit)"""
    command = user_input.lower()
    
    if command == "/exit":
        print("\nExiting chat. Goodbye!")
        return True, True
        
    elif command == "/clear":
        # Keep only the first message (the system prompt)
        messages[:] = [messages[0]]
        print("\n[System] Conversation memory cleared.")
        return True, False
        
    elif command == "/history":
        print("\n--- Conversation History ---")
        if len(messages) <= 1:
            print("No history yet.")
        else:
            for msg in messages[1:]:
                role = "You" if msg["role"] == "user" else "AI"
                print(f"{role}: {msg['content']}")
        print("----------------------------")
        return True, False
        
    elif command == "/save":
        try:
            with open("chat_history.txt", "w", encoding="utf-8") as file:
                for msg in messages[1:]:
                    role = "You" if msg["role"] == "user" else "AI"
                    file.write(f"{role}: {msg['content']}\n\n")
            print("\n[System] Conversation successfully saved to chat_history.txt")
        except Exception as e:
            print(f"\n[Error] Failed to save history: {e}")
        return True, False
        
    elif command.startswith("/"):
        print(f"\n[System] Unknown command: {command}")
        return True, False
        
    # If the input doesn't start with a command, return False
    return False, False

def generate_response(client, messages):
    """Sends the conversation to Groq and returns the response, handling errors."""
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        # Prevents the app from crashing if the internet drops or the API fails
        return f"[API ERROR] Could not generate response. Details: {e}"

def main():
    # 1. Initialization
    client = initialize_client()
    print_banner()

    # 2. Memory Setup
    messages = [
        {"role": "system", "content": "You are a helpful, professional AI assistant."}
    ]

    # 3. Main Loop
    while True:
        user_input = get_user_input()
        
        # Ignore empty inputs
        if not user_input:
            continue

        # 4. Command Handling
        is_command, should_exit = handle_commands(user_input, messages)
        if should_exit:
            break
        if is_command:
            continue

        # 5. Add user message to memory
        messages.append({"role": "user", "content": user_input})

        # 6. Memory Limit Management (Max 10 Exchanges)
        # 1 System Prompt + 10 User Messages + 10 AI Replies = 21 items max
        while len(messages) > 21:
            messages.pop(1) # Removes the oldest user message
            if len(messages) > 1:
                messages.pop(1) # Removes the oldest AI reply

        # 7. Generate and Display AI Response
        ai_reply = generate_response(client, messages)
        print(f"\nAI: {ai_reply}")

        # 8. Store AI response in memory (only if it wasn't an API error)
        if not ai_reply.startswith("[API ERROR]"):
            messages.append({"role": "assistant", "content": ai_reply})
        else:
            # If there was an error, pop the last user message so we don't break the conversation flow
            messages.pop()

if __name__ == '__main__':
    main()
    