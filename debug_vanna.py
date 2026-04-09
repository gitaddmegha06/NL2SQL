import asyncio
from vanna_setup import agent
from vanna.core.user import RequestContext

async def test():
    context = RequestContext()
    try:
        print("Sending message...")
        async for component in agent.send_message(context, "How many patients?"):
            print(f"Component: {type(component)}")
            if component.simple_component:
                print(f"  Simple: {component.simple_component}")
            if component.rich_component:
                print(f"  Rich: {type(component.rich_component)}")
    except Exception as e:
        print(f"Error caught: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
