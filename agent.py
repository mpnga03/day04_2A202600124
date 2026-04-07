from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv
import os

# Tải biến môi trường (API Key)
load_dotenv()

# 1. Đọc System Prompt
try:
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    SYSTEM_PROMPT = "Bạn là trợ lý du lịch hữu ích."

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Thêm System Prompt vào đầu danh sách tin nhắn nếu chưa có
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
    response = llm_with_tools.invoke(messages)
    
    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f">>> Gọi tool: {tc['name']}({tc['args']})")
    else:
        print(">>> Trả lời trực tiếp")
        
    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)

# Thêm các Node
builder.add_node("agent", agent_node)
tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Thiết lập Edges (Đã hoàn thiện phần TODO)
builder.add_edge(START, "agent")  # Bắt đầu tại Agent

# Sử dụng tools_condition để tự động quyết định: 
# Nếu có tool_calls thì sang node "tools", nếu không thì kết thúc (END)
builder.add_conditional_edges("agent", tools_condition)

# Sau khi thực hiện Tool, quay lại Agent để tổng hợp câu trả lời
builder.add_edge("tools", "agent")

# Biên dịch Graph
graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy - Trợ lý Du lịch Thông minh")
    print("      Gõ 'quit' để thoát")
    print("=" * 60)
    
    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
            
        print("\nTravelBuddy đang suy nghĩ...")
        
        # Chạy Graph
        result = graph.invoke({"messages": [("human", user_input)]})
        
        # Lấy tin nhắn cuối cùng để hiển thị
        final = result["messages"][-1]
        print(f"\nTravelBuddy: {final.content}")