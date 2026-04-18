from langgraph.graph import StateGraph, MessagesState, START, END

def build_agent():
    def summarize(state: MessagesState):
        return {"messages": [{"role": "ai", "content": "This is the output from the summarization node"}]}
    
    graph = StateGraph(MessagesState)

    graph.add_node(summarize)
    graph.add_edge(START, "summarize")
    graph.add_edge("summarize", END)

    agent = graph.compile()

    return agent
