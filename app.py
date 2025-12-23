from agent.agent import CompanionAgent

def main():
    agent = CompanionAgent()

    print("AI Companion is ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("User: ")
        
        if user_input.lower() in ["exit", "quit", "bye", "掰掰", "再見"]:
            print("\n🤖 再見！期待下次見面~")
            break

        response = agent.chat(user_input)
        print(f"AI: {response}\n")

if __name__ == "__main__":
    main()