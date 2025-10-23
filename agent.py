# agent.py
import json
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME
from tools import get_current_time, add_numbers
from context_manager import ContextManager

client = OpenAI(api_key=OPENAI_API_KEY)

TOOL_MAP = {
    "get_current_time": get_current_time,
    "add_numbers": add_numbers,
}

PROMPT = """You are a structured reasoning agent.

You can call one of the following tools:
- get_current_time: returns the current UTC time
- add_numbers: add two numbers (expects "a" and "b")

User message: {user_message}

Return a JSON like:
{{
  "tool": "<tool_name or none>",
  "params": {{...}},
  "intent": "call_tool" | "done",
  "final_answer": "<optional natural language>"
}}
"""

def decide_next_action(user_message, context):
    prompt = PROMPT.format(user_message=user_message)
    messages = [
        {"role": "system", "content": "You are an agent that plans tool calls."},
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        response_format={"type": "json_object"},
    )
    decision = json.loads(response.choices[0].message.content)
    return decision


def agent_loop():
    cm = ContextManager()
    print("🤖 12-Factor Agent ready. Type 'exit' to quit.\n")
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        decision = decide_next_action(user_message, cm.get_context())
        print(f"\nLLM decision: {decision}\n")

        if decision["intent"] == "done":
            print("✅", decision.get("final_answer", "Done."))
            continue

        tool_name = decision["tool"]
        params = decision.get("params", {})
        if tool_name in TOOL_MAP:
            result = TOOL_MAP[tool_name](params)
            print(f"🔧 Tool {tool_name} executed → {result}\n")
            cm.append({"tool": tool_name, "result": result})
        else:
            print("⚠️ Unknown tool.")

if __name__ == "__main__":
    agent_loop()
