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

# Load environment variables (e.g., GROQ_API_KEY)
load_dotenv()

class SimpleUserResolver(UserResolver):
    def resolve_user(self, context: RequestContext) -> User:
        return User(id="default_user", roles=["admin"])

def create_agent():
    # 1. LLM Service (Using Groq as provider)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please create a .env file and add it.")
        
    llm_service = OpenAILlmService(
        api_key=api_key, 
        model="llama-3.3-70b-versatile",
        client_kwargs={
            "base_url": "https://api.groq.com/openai/v1"
        }
    )
    
    # 2. Database connection handled by built-in SqliteRunner
    sqlite_runner = SqliteRunner(db_path="clinic.db")
    
    # 3. Agent Memory
    memory = DemoAgentMemory()
    
    # 4. Tool Registry and Tools
    tool_registry = ToolRegistry()
    run_sql_tool = RunSqlTool(runner=sqlite_runner)
    visualize_data_tool = VisualizeDataTool()
    save_question_tool = SaveQuestionToolArgsTool(memory=memory)
    search_tool = SearchSavedCorrectToolUsesTool(memory=memory)
    
    tool_registry.register(run_sql_tool)
    tool_registry.register(visualize_data_tool)
    tool_registry.register(save_question_tool)
    tool_registry.register(search_tool)
    
    # 5. User Resolver
    user_resolver = SimpleUserResolver()
    
    # 6. Create Agent with all connected components
    config = AgentConfig()
    agent = Agent(
        config=config,
        llm_service=llm_service,
        tool_registry=tool_registry,
        agent_memory=memory,
        user_resolver=user_resolver
    )
    
    return agent

# Standard export to easily reference in other files
agent = create_agent()

if __name__ == "__main__":
    print("Vanna Agent initialized successfully with Groq!")
