import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main():
    if api_key is None:
        raise RuntimeError("'GEMINI_API_KEY' key not found in .env file.")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="ai-agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        function_calls = response.function_calls or []
        if function_calls:
            function_responses = []
            for function_call in response.function_calls:
                function_call_result = call_function(
                    function_call, verbose=args.verbose
                )
                if (
                    function_call_result.parts is None
                    or len(function_call_result.parts) == 0
                ):
                    raise Exception("function_call returned no parts")

                function_response = function_call_result.parts[0].function_response
                function_responses.append(function_call_result.parts[0])

                if function_response is None:
                    raise Exception("function_response is None")

                response_result = function_response.response
                if response_result is None:
                    raise Exception("response_result is None")

                if args.verbose:
                    print(f"-> {response_result}")

            messages.append(types.Content(role="user", parts=function_responses))
            continue

        print(response.text)
        return

    print("Agent did not finish within 20 iterations.")


if __name__ == "__main__":
    main()
