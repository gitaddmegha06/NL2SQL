import asyncio
import os
import sys
from vanna_setup import agent
from vanna.core.user import RequestContext
from vanna.components import SimpleTextComponent, RichTextComponent, StatusCardComponent

async def run_chat():
    print("\n" + "="*50)
    print("🏥  Clinic Management NL2SQL Chat System")
    print("="*50)
    print("Type your questions in plain English.")
    print("Example: 'How many patients are from Mumbai?'")
    print("Type 'exit' or 'quit' to stop.")
    print("="*50 + "\n")

    # Initialize a dummy request context
    context = RequestContext()
    
    # We can keep a conversation ID to track history if the agent supports it
    conversation_id = None

    while True:
        try:
            # Use input() for user query
            user_input = input("🗣️  You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                print("\nGoodbye! 👋")
                break

            print("\n🤖 Assistant is thinking...")
            
            # agent.send_message is an AsyncGenerator in Vanna 2.x
            async for component in agent.send_message(context, user_input, conversation_id=conversation_id):
                
                # 1. Handle Simple Text Output (Direct answers/SQL previews)
                if isinstance(component.simple_component, SimpleTextComponent):
                    print(f"\n{component.simple_component.text}")
                
                # 2. Handle Rich Text (Markdown compatible)
                elif isinstance(component.rich_component, RichTextComponent):
                    print(f"\n{component.rich_component.content}")
                
                # 3. Handle Status Updates (e.g. "Executing SQL")
                elif isinstance(component.rich_component, StatusCardComponent):
                    status = component.rich_component
                    if status.status == "running":
                        print(f"⏳ [{status.title}] {status.description}")
                    elif status.status == "error":
                        print(f"❌ Error: {status.description}")
            
            print("\n" + "-"*30)
            
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n⚠️  An unexpected error occurred: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(run_chat())
    except KeyboardInterrupt:
        pass
