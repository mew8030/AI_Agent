import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function



def main():
    print("Hello from gemi!")

    #load the environment 
    load_dotenv()
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User must type a prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access 'args.user_prompt'

    #get the api key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("environment variable wasn't found")
    else:
        print("environment variable was found")
    client = genai.Client(api_key=api_key) 
    
    #create the role structure
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    for i in range(20):
        try:
            #call to generate content
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                    ),
            )

            for candidate in response.candidates:
                messages.append(candidate.content)

            #check if there are function calls
            if response.candidates[0].content.parts[0].function_call:
                fun_results_list = []
                #execute each function call
                for part in response.candidates[0].content.parts:
                    if part.function_call:
                        function_call_results = call_function(part.function_call, args.verbose)
                        if not function_call_results.parts:
                            raise Exception("parts list empty in function_call_results")
                        if not function_call_results.parts[0].function_response:
                            raise Exception("FunctionResponse is somehow type None")
                        fun_results_list.append(function_call_results.parts[0])
                        if args.verbose:
                            print(f"-> {function_call_results.parts[0].function_response.response}")
                messages.append(types.Content(role="user", parts=fun_results_list))
            else:
                if response.text:
                    print(response.text)
                    break
        except Exception as e:
            print(f"Error: {e}")
            break

        data = response.usage_metadata
        if not data:
            raise ValidationError("missing metadat from response")
        if args.verbose:
            print(f"User prompt:{args.user_prompt}\nPrompt tokens: {data.prompt_token_count}\nResponse tokens: {data.candidates_token_count}")


if __name__ == "__main__":
    main()
