from agent import HelpdeskAgent

def main():
 a=HelpdeskAgent(); print("IT Helpdesk Agent\nTry: My VPN will not connect\n")
 for m in iter(lambda:input("Employee: ").strip(),"quit"): print("Agent:",a.chat(m),"\n")
if __name__=="__main__": main()
