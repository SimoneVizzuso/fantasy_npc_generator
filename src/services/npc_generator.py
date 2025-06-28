import os
import time
import json
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field, field_validator
from ollama import chat


prompt_NPC_generator = """
You are a dungeon master that knows every manual of dungeons and dragons 5th edition. Your task is to create an NPC
character that respect the rules of the game written in the manuals. You will be provided with a list of
elements to use in the creation of the NPC between <<<>>> where there could be also a comment that need to be present
in the final result and take in consideration for every aspect of the character. Take in high consideration the
age of the character, so a young character will not have the experience of an adult, while an older one will not have
the same spirit or stamina of a young one. The alignment of the character will also influence the personality and the
behavior of the character.

You will provide the NPC with:
- A name that fits the character and the race chosen, you can be creative with it
- A brief description of the character appearance, you can describe what the character looks like, what it wears, etc.
- The personality of the character, you can describe how the character behaves and interacts with others
- Some distinguishing marks that make the character unique and recognizable
- A profession that fits the character's class, but it's not the name of the class, with a brief summary of the role.
You need to write explicitly the profession name and then add a comma and a brief description of the role
- A brief background story that explains the character's past and how it got to the current situation, using the
previous information, provided and generated
- A brief hook that can be used to introduce the character in a campaign, it can be a rumor, a legend, a prophecy, etc.

You will have to use the information provided to create a unique NPC character that can be used in a campaign.

<<<
class: {char_job}
race: {char_race}
age: {char_age}
alignment: {char_alignment}
additional comments: {additional_comments}
>>>

{format_instructions}

IMPORTANT: Output ONLY the JSON object, with NO explanations, NO tags, NO extra text. Do not include any commentary or markdown. Only valid JSON.
"""


class NPC(BaseModel):
    name: str = Field(description="name of the NPC")
    personality: str = Field(description="personality of the NPC")
    description: str = Field(description="description of the NPC")
    marks: str = Field(description="distinctive marks of the NPC")
    profession: str = Field(description="profession of the NPC")
    background: str = Field(description="background of the NPC")
    hook: str = Field(description="hook of the NPC")

    @field_validator("name", "personality", "description", "marks", "profession", "background", "hook", mode="before")
    @classmethod
    def validate_string_fields(cls, value):
        if not isinstance(value, str):
            return str(value)
        return value

def extract_json(text):
    import re
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group(0)
    raise ValueError("No JSON found in LLM output")


def generate_npc(char_job, char_race, char_age, char_alignment, additional_comments=""):
    load_dotenv()
    text_model = os.getenv('TEXT_MODEL')
    print(f'I am currently using: {text_model}')

    parser = PydanticOutputParser(pydantic_object=NPC)
    prompt = PromptTemplate(
        template=prompt_NPC_generator,
        input_variables=['char_job', 'char_race', 'char_age', 'char_alignment'],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    prompt_str = prompt.format(
        char_job=char_job,
        char_race=char_race,
        char_age=char_age,
        char_alignment=char_alignment,
        additional_comments=additional_comments
    )

    history = [
        {"role": "user", "content": prompt_str}
    ]

    start = time.time()
    resp = chat(model=text_model, messages=history, think=False)
    response = resp["message"]["content"]
    end = time.time()
    print(f'Elapsed time: {end - start}')

    json_str = extract_json(response)
    output = parser.parse(json_str)
    return (output.name, output.personality, output.description, output.marks, output.profession, output.background, output.hook)