import os, sys
from dotenv import load_dotenv
from groq import Groq

def initialize_client():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("\n[ERROR] GROQ_API_KEY missing in .env file.")
        sys.exit(1)
    return Groq(api_key=api_key)

def print_banner():
    print(f"\n{'='*40}\nAI ASSISTANT TERMINAL\n{'='*40}")
    print("Commands: /exit, /clear, /history, /save\n" + "-"*40)

def get_user_input():
    try:
        return input("\nYou: ").strip()
    except (KeyboardInterrupt, EOFError):
        return "/exit"

def handle_commands(cmd, messages):
    cmd = cmd.lower()
    if cmd == "/exit":
        print("\nGoodbye!")
        return True, True
        
    elif cmd == "/clear":
        del messages[1:] # Deletes everything except the system prompt
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
            print(f"\n[Error] {e}")
        return True, False
        
    elif cmd.startswith("/"):
        print(f"\n[System] Unknown command: {cmd}")
        return True, False
        
    return False, False

def generate_response(client, messages):
    try:
        res = client.chat.completions.create(messages=messages, model="llama-3.3-70b-versatile", temperature=0.7)
        return res.choices[0].message.content
    except Exception as e:
        return f"[API ERROR] {e}"

def main():
    client = initialize_client()
    print_banner()
    messages = [{"role": "system", "content": "You are a professional AI assistant."}]

    while True:
        user_input = get_user_input()
        if not user_input: continue

        is_cmd, should_exit = handle_commands(user_input, messages)
        if should_exit: break
        if is_cmd: continue

        messages.append({"role": "user", "content": user_input})

        # Memory Limit: Keep system prompt (1) + last 10 exchanges (20)
        while len(messages) > 21:
            del messages[1:3] 

        reply = generate_response(client, messages)
        print(f"\nAI: {reply}")

        if "[API ERROR]" not in reply:
            messages.append({"role": "assistant", "content": reply})
        else:
            messages.pop()

if __name__ == '__main__':
    main()