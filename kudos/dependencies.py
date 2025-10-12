from openai import OpenAI
from .schemas.schemas import KudosFormat

#Create the client to interface with OpenAI server:
client = OpenAI()

def refined_kudos_message(message):
    
    kudos_message = client.responses.create(
    model="gpt-5",
    input=message,
    instructions = "1. First mention employee's name and team. 2. Explain his work in minimum shifting it to highlight achievements/bigwin, impact created, and how it helped to grow in product/organization/customer."
    )

    print(kudos_message.output_text)
    print(type(kudos_message))
    print(kudos_message.model)


    response = client.responses.parse(
    model="gpt-5",
    input=[
        {"role": "system", "content": "Extract the information."},
        {
            "role": "user",
            "content": kudos_message.output_text,
        },
    ],
    text_format=KudosFormat,
    )
    structured_kudos = response.output_parsed
    print(structured_kudos)
    return structured_kudos