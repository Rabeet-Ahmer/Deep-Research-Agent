from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent
import chainlit as cl
from coordinator import ResearchCoordinator


@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hi! Send me a research topic and I'll generate a report.").send()


@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history")

    msg = message.content.strip()
    if not msg:
        await cl.Message(content="Please provide a valid research topic.").send()
        return
    
    history.append({"role": "user", "content": msg})

    # Prepare the outgoing assistant message (for streaming the final answer)
    answer_message = cl.Message(content="")
    await answer_message.send()

    # Show this only if a handoff/tool is invoked
    status_message = cl.Message(content="🔍 Thinking...")
    await status_message.send()

    try:
        coordinator = ResearchCoordinator()
        
        # Use streaming method for real-time updates
        async for progress_update in coordinator.conduct_research_streaming(msg):
            await answer_message.stream_token(progress_update)
        
        # Remove status message
        await status_message.remove()

        # Persist history
        history.append({"role": "assistant", "content": answer_message.content})
        cl.user_session.set("history", history)
        
    except Exception as e:
        # Clean up status message if present
        if status_message is not None:
            try:
                await status_message.remove()
            except Exception:
                pass
        # Update the answer message with error
        error_msg = f"Error during research: {str(e)}"
        answer_message.content = error_msg
        await answer_message.update()
        print(f"Error in research: {e}")
        # Add error to history
        history.append({"role": "assistant", "content": error_msg})
        cl.user_session.set("history", history)
