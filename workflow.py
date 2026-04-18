from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def start_worfklow(text_content: str):
    llm = ChatGroq(model="qwen/qwen3-32b", temperature=0, reasoning_format="parsed" )
    script_dir = os.path.dirname(os.path.abspath(__file__))
    system_prompt_path = os.path.join(script_dir, "SYS_PROMPT.txt")
    
    with open(system_prompt_path, "r") as f:
        system_prompt = f.read()
    sys_msg = SystemMessage(content = system_prompt)

    def summarize(state: MessagesState):
        response = llm.invoke([sys_msg]+state["messages"])
        return {"messages": [response]}
    
    graph = StateGraph(MessagesState)

    graph.add_node("summarize", summarize)
    graph.add_edge(START, "summarize")
    graph.add_edge("summarize", END)

    agent = graph.compile()

    response_to_user = agent.invoke({"messages":[{"role": "user", "content":text_content}]})["messages"][-1].content
    
    return response_to_user
