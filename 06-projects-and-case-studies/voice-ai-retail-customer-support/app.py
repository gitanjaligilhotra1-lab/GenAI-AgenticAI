from agent import VoiceRetailAgent

def main():
    agent=VoiceRetailAgent()
    print("Voice AI Retail Support — text simulator\nTry: Where is order ORD-2001?\n")
    for message in iter(lambda: input("Caller: ").strip(), "quit"):
        print("Agent:",agent.handle_turn(message),"\n")
if __name__=="__main__": main()
