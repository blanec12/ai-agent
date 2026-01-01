import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("'GEMINI_API_KEY' key not found in .env file.")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="ai-agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )

    if response.usage_metadata is not None:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Response: {response.text}")
    else:
        raise RuntimeError("Response 'usage_metadata' is None.")


if __name__ == "__main__":
    main()
