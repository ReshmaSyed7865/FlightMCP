import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json
from langchain_ollama import ChatOllama 
from langchain.chat_models import init_chat_model
llm= ChatOllama(model="llama3.1")
server_params = StdioServerParameters(
    command="python",
    args=["flight_server.py"],
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)

            agent =create_react_agent(llm, tools)
            agent_response = await agent.ainvoke({"messages":"Check whether seat number 06A in flight 8 available or not"})
            
            print(agent_response["messages"][-1].content)
    
            

if __name__ == "__main__":
    asyncio.run(main())
