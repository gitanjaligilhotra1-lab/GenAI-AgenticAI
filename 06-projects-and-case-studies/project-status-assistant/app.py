from assistant import ProjectStatusAssistant
if __name__=="__main__":
 a=ProjectStatusAssistant();print("Project Status Assistant\nTry: status, blockers, what changed\n")
 for q in iter(lambda:input("You: ").strip(),"quit"):print(a.answer(q),"\n")
