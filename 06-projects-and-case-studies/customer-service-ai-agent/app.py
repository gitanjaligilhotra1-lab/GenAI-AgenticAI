from agent import CustomerSupportAgent

def main():
    agent = CustomerSupportAgent()
    print("Customer Support AI Agent")
    print("Try: My order ORD-1001 arrived damaged. Can you replace it?")
    print("Type quit to exit.\n")
    while True:
        message = input("You: ").strip()
        if message.lower() in {"quit", "exit"}:
            break
        print("\nAgent:", agent.chat(message), "\n")

if __name__ == "__main__":
    main()
