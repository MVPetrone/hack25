from langgraph.prebuilt import create_react_agent
# from langchain.agents import load_tools, create_react_agent



from app.tools.transcript import transcribe
from app.tools.video_downloader import download_video
from app.tools.book_hotel import book_hotel
from app.tools.start_vote import initiate_vote, count_vote_result
from app.tools.image_generator import generate_image

from app.config import config
from app.utils import send_user_message

openai_api_key = config.OPENAI_API_KEY

tools = [download_video, transcribe, book_hotel, initiate_vote, count_vote_result, generate_image]

prompt = """
You are a helpful assistant. STRICTLY follow these rules:

1. TOOL CALLING RULES:
   - For group_id: ALWAYS extract and use group_id if the user provides it; if missing, ask for it.
   - For vote titles: USE THE USER'S EXACT WORDS without modification
   - NEVER shorten, rephrase or generate new titles
   - If title is missing, ASK USER - don't create one
   - For vote options: ONLY use options explicitly provided by user

2. GENERAL RULES:
   - Preserve ALL user-provided text verbatim
   - Respond in the user's language
   - Don't assume missing arguments
   - Ask for clarification when needed

Example:
User: "Start a vote in group Arz7KwQDd9m about 'which fruit is your favourite' with options apple, banana"
Correct: group_id="Arz7KwQDd9m" title="which fruit is your favourite", options=["apple", "banana"]
"""

agent = create_react_agent(
    model=config.LLM_MODEL,
    tools=tools,
    debug=False,
    prompt=prompt
)

history = [{"role": "system", "content": prompt}]

# Receives a user prompt and forwards it to the AI agent for processing.
# Handles collecting tool call arguments and constructing responses based on tool usage.
def invoke(prompt, from_uid):
    print(f"Received prompt: {prompt} from {from_uid}")

    # Format the user message and append it to the interaction history
    message = {
        "role": "user",
        "content": f"{prompt}",
    }
    history.append(message)

    query = {
        "messages": history
    }

    # Invoke the AI agent with the accumulated history
    result = agent.invoke(query)

    # Initialize variables for tracking tool usage and arguments
    tool_name = None
    collected_args = {}
    required_params = []
    tool_result = None

    # Inspect agent's returned steps for tool calls and extract arguments
    for step in result.get("messages", []):
        if hasattr(step, "tool_calls"):
            for call in step.tool_calls:
                tool_name = call.get("name")
                collected_args.update(call.get("args", {}))
                # You can define required_params based on the tool manually if needed
                if tool_name == "book_hotel":
                    required_params = ["location", "check_in", "check_out", "guests", "room_type"]
                if tool_name == "initiate_vote":
                    required_params = ["group_id", "title", "options"]

        elif hasattr(step, "name") and step.name == "book_hotel":
            try:
                parsed = eval(step.content)
                if isinstance(parsed, dict):
                    collected_args.update(parsed)
            except Exception:
                pass

    # Construct structured response
    # Skip structured response if tool is in excluded list (e.g., image generation, counting)
    excluded_tools = {"count_vote_result", "generate_image"}
    if tool_name and tool_name not in excluded_tools:
        missing_params = [p for p in required_params if
                          p not in collected_args or not collected_args[p] or collected_args[p] == "undefined"]
        if missing_params:
            result["response"] = f"Got partial info for `{tool_name}`. Please provide: {', '.join(missing_params)}"
        else:
            # Actually call the tool and get the result
            try:
                if tool_name == "book_hotel":
                    tool_result = book_hotel(**collected_args)
                    result["response"] = f"✅ Hotel booking confirmed!\n\n🏨 Hotel: {tool_result['hotel']}\n📍 Location: {tool_result['location']}\n📅 Check-in: {tool_result['check_in']}\n📅 Check-out: {tool_result['check_out']}\n👥 Guests: {tool_result['guests']}\n🛏️ Room Type: {tool_result['room_type']}\n🌙 Nights: {tool_result['nights']}\n💰 Total Price: ${tool_result['total_price']}\n🆔 Confirmation ID: {tool_result['confirmation_id']}"
                elif tool_name == "initiate_vote":
                    tool_result = initiate_vote(**collected_args)
                    result["response"] = f"✅ Vote initiated successfully!\n\n📊 Title: {collected_args['title']}\n👥 Group: {collected_args['group_id']}\n🗳️ Options: {', '.join(collected_args['options'])}"
                elif tool_name == "download_video":
                    tool_result = download_video(**collected_args)
                    result["response"] = f"📹 Video download initiated for: {collected_args.get('video_url', 'unknown URL')}"
                elif tool_name == "transcribe":
                    tool_result = transcribe(**collected_args)
                    result["response"] = f"📝 Transcription completed for: {collected_args.get('video_url', 'unknown URL')}"
                else:
                    result["response"] = f"All parameters collected for `{tool_name}`: {collected_args}"
            except Exception as e:
                result["response"] = f"❌ Error executing {tool_name}: {str(e)}"
    else:
        result["response"] = result.get("messages", [])[-1].content if result.get("messages") else ""

    history.append({"role": "assistant", "content": result["response"]})

    # Send the final response back to the user via bot message
    send_user_message(from_uid, result["response"])

    return result
