import os
from dotenv import load_dotenv

from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.openai import OpenAILlmService


load_dotenv()

class SimpleUserResolver(UserResolver):
    async def resolve_user(self, context: RequestContext) -> User:
        return User(id="default_user", roles=["admin"])

def create_agent():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please create a .env file and add it.")
        
    llm_service = OpenAILlmService(
        api_key=api_key, 
        model="llama-3.3-70b-versatile",
        base_url="https://api.groq.com/openai/v1"
    )
    
    # db-runner
    sqlite_runner = SqliteRunner(database_path="clinic.db")
    
    # Memory
    memory = DemoAgentMemory()
    
    # tools
    tool_registry = ToolRegistry()
    run_sql_tool = RunSqlTool(sql_runner=sqlite_runner)
    visualize_data_tool = VisualizeDataTool()
    save_question_tool = SaveQuestionToolArgsTool()
    search_tool = SearchSavedCorrectToolUsesTool()
    
    tool_registry.register_local_tool(run_sql_tool, access_groups=[])
    tool_registry.register_local_tool(visualize_data_tool, access_groups=[])
    tool_registry.register_local_tool(save_question_tool, access_groups=[])
    tool_registry.register_local_tool(search_tool, access_groups=[])
    
    # 5. User Resolver
    user_resolver = SimpleUserResolver()
    
    # agent
    config = AgentConfig()
    agent = Agent(
        config=config,
        llm_service=llm_service,
        tool_registry=tool_registry,
        agent_memory=memory,
        user_resolver=user_resolver
    )
    
    return agent


agent = create_agent()

if __name__ == "__main__":
    print("Vanna Agent initialized successfully with Groq!")
