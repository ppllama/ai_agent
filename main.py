import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt, MAX_ITERS
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


def main():
    load_dotenv()

    verbose = "--x" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)


    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]


    
    i = 0
    while True:
        i += 1
        if i > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)
        
        try:
            response_text = generate_content(client, messages, verbose)
            if response_text:
                print(f"Final response: {response_text}")
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")



def generate_content(client, messages, verbose):


    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )   


    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001',
        contents = messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


    function_responses = []
    function_calls = response.function_calls
    if function_calls:
        for call in function_calls:
            print(f"Calling function: {call.name}({call.args})")
            result = call_function(call, verbose)
            if not result.parts[0].function_response.response:
                raise Exception("empty function call result")
            if verbose:
                print(f"-> {result.parts[0].function_response.response}")
            function_responses.append(result.parts[0])
            
        if not function_responses:
            raise Exception("no function responses generated, exiting.")
        
        messages.append(types.Content(role="tool", parts=function_responses))

    else:
        return(response.text)


if __name__ == "__main__":
    main()