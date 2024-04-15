import random


def randomize_selection(ages, classes, races, chosen_classes, chosen_races, chosen_ages):
    if len(chosen_classes) < 1:
        chosen_classes = classes
    if len(chosen_races) < 1:
        chosen_races = races
    if len(chosen_ages) < 1:
        chosen_ages = ['young', 'adult', 'old']
    char_class = random.choice(chosen_classes)
    char_race = random.choice(chosen_races)
    char_age_range = random.choice(chosen_ages)
    char_age = age_calculator(ages, char_race, char_age_range)
    return char_class, char_race, char_age


def age_calculator(ages, char_race, char_age_range):
    age_ranges = ages[char_race]
    mature_age, max_age = age_ranges.split('-')
    mature_age = int(mature_age)

    check_over_max_age = False  # TODO: implement this as a message to the user
    if max_age.endswith('+'):
        max_age = int(max_age[:-1])
        check_over_max_age = True
    else:
        max_age = int(max_age)

    if char_age_range == 'young':
        char_age = random.randint(mature_age - int(mature_age * 0.4), mature_age - 1)
    elif char_age_range == 'adult':
        char_age = random.randint(mature_age, int(max_age * 0.3))
    elif char_age_range == 'old':
        char_age = random.randint(int(max_age * 0.3) + 1, max_age)
    else:
        char_age = random.randint(1, max_age)

    return char_age
