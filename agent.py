import os
import json
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

MODEL = "qwen/qwen3.8-27b"


def search(query: str) -> str:
    results = tavily_client.search(query=query, max_results=3)
    formatted = []
    for r in results["results"]:
        formatted.append(f"- {r['title']}: {r['content']}")
    return "\n".join(formatted)


tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search the internet for recent information. Use this when the question needs up-to-date info not in your knowledge.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


def run_agent(question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a research assistant. When you need recent information, use the search tool. Answer in English."
        },
        {"role": "user", "content": question}
    ]

    while True:
        response = groq_client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                args = json.loads(tool_call.function.arguments)
                result = search(args["query"])

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        else:
            return message.content
