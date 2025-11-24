import os
import sys
import argparse 
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_prompt')
    parser.add_argument('-v', '--verbose',
    action='store_true')
    args = parser.parse_args()

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    #f"Total tokens: {response.usage_metadata.total_token_count}"

    if response.function_calls: 
        fc = response.function_calls[0]
        function_call_result = call_function(fc, verbose=args.verbose)

        if not function_call_result.parts:
            raise RuntimeError("Function call returned invalid tool content")


        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        
    else: 
        print(response.text)

if __name__ == "__main__":
    main()
