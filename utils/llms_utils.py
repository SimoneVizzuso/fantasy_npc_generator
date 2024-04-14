import os
import time

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_community.llms import Ollama
from dotenv import load_dotenv

prompt_NPC_generator = """
You are a dungeon master that knows every manual of dungeons and dragons 5th edition. Your task is to create an NPC 
character that respect the rules of the game written in the manuals. You will be provided with a list of 
elements to use in the creation of the NPC between <<<>>>.

You will provide the NPC with:
- A name that fits the character and the race chosen
- A brief description of the character and the behavior
- Some distinguishing marks that make the character unique
- A profession that fits the character's class with a brief summary of the role
- A brief background story that explains the character's past and how it got to the current situation, using the 
previous information, provided and generated

You will have to use the information provided to create a unique NPC character that can be used in a campaign.

####
Here are some examples:

class: Wizard
race: Elf
age: 120
alignment: Chaotic Good

name: Elrond
description: Elrond is a wise and old elf that has lived for many years in the forest. He is a very skilled wizard
that has mastered the art of magic. He is known for his kindness and his willingness to help others. He is always
ready to help those in need and to protect the forest from any danger.
marks: Elrond has a long white beard and a staff that he always carries with him. He is always wearing
a long robe and a pointed hat. He has a kind smile and a twinkle in his eyes.
profession: Court advisor, helps the king make important decisions and advises him on matters of magic.
background: Elrond was born in the Gertha’s Forest, a magical place where the elves live in harmony with nature.
He was raised by his parents, who were both skilled wizards. He learned the art of magic from them and spent many
years studying the ancient texts and scrolls that contained the secrets of the arcane. He became a powerful wizard
and a respected member of the elven community. He is now known as the protector of the forest and the guardian of
its secrets. He is always ready to help those in need and to protect the forest from any danger that may come its way.
---------------------------------------------------------------------------------------------------------------------
class: Fighter
race: Human
age: 35
alignment: Lawful Neutral

name: John
description: John is a strong and brave fighter that has fought in many battles. He is a skilled warrior that has
mastered the art of combat. He is known for his courage and his loyalty to his comrades. He is always ready to
defend those that cannot defend themselves and to fight for what he believes in.
marks: John has a scar on his face that he got in a battle with a fierce orc. He is always
wearing a suit of armor and carrying a sword and shield. He has a serious expression and a determined look in his eyes.
profession: John is a veteran soldier who now serves as a city guard, usually stationed at the town gates to control 
who comes in and who goes out.
background: He was born in the city of Valoria, a place where the warriors are respected and honored. He
was raised by his father, who was a veteran warrior that fought in many battles. He learned the art of combat from
him and spent many years training with the other warriors of the city. He became a skilled fighter and a respected
member of the warrior guild. He is now known as the champion of the city and the protector of its people. He is
always ready to defend the city from any threat that may come its way.
###

<<<
class: {char_class}
race: {char_race}
age: {char_age}
alignment: {char_alignment}
>>>

{format_instructions}
"""


class NPC(BaseModel):
    name: str = Field(description="name of the NPC")
    description: str = Field(description="description of the NPC")
    marks: str = Field(description="distinctive marks of the NPC")
    profession: str = Field(description="profession of the NPC")
    background: str = Field(description="background of the NPC")

    @validator("name", "description", "marks", "profession", "background", allow_reuse=True)
    def validate_string_fields(cls, field):
        if not isinstance(field, str):
            raise ValueError("Each field needs to be a string")
        return field


def generate_npc(char_class, char_race, char_age, char_alignment):
    # Load the environment variables from .env file
    load_dotenv("data/model.env")

    # Access the environment variable
    ollama_model = os.getenv('OLLAMA_MODEL')
    print(f'I am currently using: {ollama_model}')

    model = Ollama(model=ollama_model)

    # Set up a parser + inject instructions into the prompt template.
    parser = PydanticOutputParser(pydantic_object=NPC)

    prompt = PromptTemplate(
        template=prompt_NPC_generator,
        input_variables=['char_class', 'char_race', 'char_age', 'char_alignment'],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # And a query intended to prompt a language model to populate the data structure.
    prompt_and_model = prompt | model | parser
    start = time.time()
    output = prompt_and_model.invoke({"char_class": char_class, 'char_race': char_race, 'char_age': char_age,
                                      'char_alignment': char_alignment})
    end = time.time()
    print(f'Elapsed time: {end - start}')
    return output.name, output.description, output.marks, output.profession, output.background
