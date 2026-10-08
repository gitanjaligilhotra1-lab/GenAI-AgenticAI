from agent import FinanceAgent
if __name__=="__main__":
 a=FinanceAgent();print("Personal Finance & Spending Agent\nTry: summary, subscriptions, unusual, afford 1500\n")
 for q in iter(lambda:input("You: ").strip(),"quit"):print("Agent:",a.chat(q),"\n")
