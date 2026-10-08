from agent import IncidentInvestigationAgent
def main():
    agent=IncidentInvestigationAgent()
    print("Production Incident Investigation Agent\nIncidents: INC-1001, INC-1002\nTry: Investigate INC-1001\nType quit to exit.\n")
    while True:
        message=input("You: ").strip()
        if message.lower() in {"quit","exit"}: break
        print("\nAgent:\n"+agent.chat(message)+"\n")
if __name__=="__main__": main()
