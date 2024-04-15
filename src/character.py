from random import random


class Character:
    def __init__(self, name=None, job=None, race=None, age=None, alignment=None, personality=None, profession=None,
                 description=None, marks=None, background=None):
        self.index = random()
        self.name = name
        self.job = job
        self.race = race
        self.age = age
        self.alignment = alignment
        self.personality = personality
        self.profession = profession
        self.description = description
        self.marks = marks
        self.background = background
