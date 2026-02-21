from llm.openai_client import OpenAIClient

if __name__ == "__main__":
    client = OpenAIClient(model="gpt-4o-mini")

    messages = [
        {"role": "system", "content": "You are a helpful banking assistant."},
        {"role": "user", "content": "Say hello in one sentence."},
    ]

    response = client.chat(messages)
    print("LLM Response:")
    print(response)
