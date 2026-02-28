import os
import sys
from dotenv import load_dotenv
from groq import Groq

def initialize_client():
    """Loads the API key and initializes the Groq client securely."""
    # Load environment variables from the .env file
    load_dotenv()
    
    # Fetch the API key securely
    api_key = os.getenv("GROQ_API_KEY")
    
    # Handle the error if the key is missing (Graceful Exit)
    if not api_key:
        print("\n[ERROR] GROQ_API_KEY not found!")
        print("Please ensure you have a .env file with your API key set.")
        sys.exit(1)
        
    # Return the authenticated client
    return Groq(api_key=api_key)

def main():
    # 1. Initialize client using our secure function
    client = initialize_client()

    # 2. Print Banner
    print("\n" + "=" * 40)
    print("AI ASSISTANT TERMINAL")
    print("=" * 40)
    print("Session Started...")
    print("Enter your query or type 'exit' to quit.\n")

    # 3. Conversation memory setup
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

    # 4. Main Chat Loop
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("\n Exiting chat. Goodbye!")
            break

        # Add user message to memory
        messages.append({"role": "user", "content": user_input})

        # Send conversation to model
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )

        ai_reply = chat_completion.choices[0].message.content

        # Print response
        print("\nAI:", ai_reply)

        # Store AI response in memory
        messages.append({"role": "assistant", "content": ai_reply})

# This ensures the code only runs when executed directly
if __name__ == '__main__':
    main()
    