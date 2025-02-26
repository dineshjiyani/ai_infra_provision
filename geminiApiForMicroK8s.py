from google import genai  # pip install -q -U google-genai
from pydantic import BaseModel, TypeAdapter  # pip install pydantic
import os
import json
import sys

g_api_key = "AIzaSyC7yzflyPGyAYD-d5dcdFzfIgnSmmYYxSs" # Replace with your actual API key

usr_prompt = sys.argv[1]  # User prompt from command line

# Construct the prompt for Ansible YAML generation
defined_word = "Generate a complete Ansible YAML file to provision the following: "
prompt = defined_word + usr_prompt

class AnsibleYaml(BaseModel):
    ansible_yaml: str  # Changed to ansible_yaml


client = genai.Client(api_key=g_api_key)
response = client.models.generate_content(
    model='gemini-2.0-flash',  # Or another suitable model
    contents=prompt,
    config={
        'response_mime_type': 'application/json',
        'response_schema': AnsibleYaml,  # Use the correct schema
    },
)

try:
    # Attempt to parse the response
    dic_json = json.loads(response.text)
    ansible_yaml_code = dic_json['ansible_yaml'] # Access the correct field

    # Create the YAML file
    with open('playbook.yml', "w") as file:  # Changed filename to playbook.yml
        file.write(ansible_yaml_code)

    print(f"Ansible YAML file 'playbook.yml' created successfully.")

except (json.JSONDecodeError, KeyError) as e:
    print(f"Error processing API response: {e}")
    print(f"Raw response text: {response.text}") # Print raw response for debugging
    sys.exit(1) # Exit with an error code


except Exception as e: # Catch any other exceptions
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)