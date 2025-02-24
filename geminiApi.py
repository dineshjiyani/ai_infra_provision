from google import genai # pip install -q -U google-genai
from pydantic import BaseModel, TypeAdapter # pip install pydantic
import os
import json
import sys

g_api_key = "AIzaSyC7yzflyPGyAYD-d5dcdFzfIgnSmmYYxSs"

#prj_id = sys.argv[1] # Project ID first
#usr_prompt = sys.argv[2] # Then the user prompt

defined_word = "Please create a complete Terraform v1.10.5 script including aws provider with Subnet id: subnet-8b0c8fc7, instance type: t2.micro, AMI ID: ami-00bb6a80f01f03502 in region : ap-south-1"
prompt = defined_word 

class TfCode(BaseModel):
  tf_code: str


client = genai.Client(api_key=g_api_key)
response = client.models.generate_content(
    model = 'gemini-2.0-flash',
    contents = prompt,
    config={
        'response_mime_type': 'application/json',
        'response_schema': TfCode,
    },
)
# Use the response as a JSON string.
print(response.text)

dic_json =  json.loads(response.text)
tf_code = dic_json['tf_code']

# Create the file
with open('main.tf', "w") as file:
    file.write(tf_code)
