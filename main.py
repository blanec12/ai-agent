import os
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("'GEMINI_API_KEY' key not found in .env file.")

    client = genai.Client(api_key=api_key)

    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    if response.usage_metadata is not None:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Response: {response.text}")
    else:
        raise RuntimeError("Response 'usage_metadata' is None.")


if __name__ == "__main__":
    main()
