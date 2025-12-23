import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types



def main():
    print("Hello from gemi!")

    #load the environment 
    load_dotenv()
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User must type a prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access 'args.user_prompt'

    #create the role structure
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    
    #get the api key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("environment variable wasn't found")
    else:
        print("environment variable was found")
    client = genai.Client(api_key=api_key) 
    
    #call to generate content
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
    )
    data = response.usage_metadata
    if not data:
        raise ValidationError("missing metadat from response")
    if args.verbose:
        print(f"User prompt:{args.user_prompt}\nPrompt tokens: {data.prompt_token_count}\nResponse tokens: {data.candidates_token_count}")
    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
