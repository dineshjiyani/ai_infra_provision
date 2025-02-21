from google import genai # pip install -q -U google-genai
from pydantic import BaseModel, TypeAdapter # pip install pydantic
import os
import json
import sys

g_api_key = "AIzaSyC7yzflyPGyAYD-d5dcdFzfIgnSmmYYxSs"

#prj_id = sys.argv[1] # Project ID first
#usr_prompt = sys.argv[2] # Then the user prompt

defined_word = "Please create a complete terraform script including oci provider with shape: VM.Standard.E4.Flex , avilibility domain: AD1, Subnet: ocid1.subnet.oc1.iad.aaaaaaaau7vcvy63usiohq4ex2eyi4a3tdx76pyxkf4eeiz3wuvfugqkzcyq,Image: ocid1.image.oc1.iad.aaaaaaaa2bulxukxsjyv3ap3x45eueiqxxpxpsfrv6qppq7xrwtiima2c2pq block for oci vm."
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
