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
from config import MAX_ITERS

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

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY variable not set")
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    #f"Total tokens: {response.usage_metadata.total_token_count}"

    iters = 0
    try:
        while True:
            iters += 1
            if iters > MAX_ITERS:
                print("Max iterations reached")
                break
            final_text = generate_content(client, messages, args.verbose)   
            if final_text is not None:
                print("Final Response")
                print(final_text)
                break

    except Exception as e:
        print(f"Error in generate content: {e}")
    
def generate_content(client, messages, verbose):
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    for candidate in response.candidates:
        messages.append(candidate.content)
    
    if not response.function_calls:
        return response.text   #can also maybe just break here??
        

    tool_parts= []
    for fc in response.function_calls: 
        function_call_result = call_function(fc, verbose=verbose)

        if not function_call_result.parts:
            raise RuntimeError("Function call returned invalid tool content")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        tool_parts.append(function_call_result.parts[0])

    if tool_parts:
        tool_response = types.Content(
            role="user",
            parts=tool_parts)
        messages.append(tool_response)

if __name__ == "__main__":
    main()


