import json
import random

import streamlit as st

common_races = []
rare_races = []
exotic_races = []

classes = []
races = []
alignment = []
ages = []


def initialize():
    global common_races, rare_races, exotic_races, classes, alignment, ages
    with open('data/data.json', 'r') as data_file:
        data = json.load(data_file)
        common_races = data['races']['common']
        rare_races = data['races']['rare']
        exotic_races = data['races']['exotic']
        classes = data['classes']
        alignment = data['alignment']
        ages = data['age']


def races_container():
    global races
    st.header('Races options')

    st.subheader('Common Races')

    if 'common_races' not in st.session_state:
        st.session_state['common_races'] = []

    container_common_races = st.container()

    ms_common_race = container_common_races.multiselect('Select one or more common races:',
                                                        common_races, key='ms_common_race')

    def _common_select_all():
        st.session_state.ms_common_race = common_races

    st.button("Select all common", on_click=_common_select_all)

    st.subheader('Rare Races')

    if 'rare_races' not in st.session_state:
        st.session_state['rare_races'] = []

    container_rare_races = st.container()

    ms_rare_race = container_rare_races.multiselect('Select one or more rare races:',
                                                    rare_races, key='ms_rare_race')

    def _rare_select_all():
        st.session_state.ms_rare_race = rare_races

    st.button("Select all rare", on_click=_rare_select_all)

    st.subheader('Exotic Races')

    if 'exotic_races' not in st.session_state:
        st.session_state['exotic_races'] = []

    container_exotic_races = st.container()

    ms_exotic_race = container_exotic_races.multiselect('Select one or more exotic races:',
                                                        exotic_races, key='ms_exotic_race')

    def _exotic_select_all():
        st.session_state.ms_exotic_race = exotic_races

    st.button("Select all exotic", on_click=_exotic_select_all)
    st.markdown("<hr>", unsafe_allow_html=True)

    return list(ms_common_race + ms_rare_race + ms_exotic_race)


def classes_container():
    st.header('Classes options')

    if 'classes' not in st.session_state:
        st.session_state['classes'] = []

    container_classes = st.container()

    ms_class = container_classes.multiselect('Select one or more classes:',
                                             classes, key='ms_class')

    def _class_select_all():
        st.session_state.ms_class = classes

    st.button("Select all classes", on_click=_class_select_all)
    st.markdown("<hr>", unsafe_allow_html=True)

    return ms_class


def alignment_container():
    st.header('Alignment options')

    if 'alignment' not in st.session_state:
        st.session_state['alignment'] = []

    container_alignment = st.container()

    sb_alignment = container_alignment.selectbox('Select one alignment:',
                                                 alignment, key='sb_alignment')

    st.markdown("<hr>", unsafe_allow_html=True)

    return sb_alignment


def randomize_selection(chosen_classes, chosen_races, chosen_ages):
    char_class = random.choice(chosen_classes)
    char_race = random.choice(chosen_races)
    char_age_range = random.choice(chosen_ages)
    char_age = age_calculator(char_race, char_age_range)
    return char_class, char_race, char_age


def age_container():
    st.header('Ages options')
    container_age = st.container()
    sb_ages = container_age.multiselect('Select one or more ages:',
                                        ['young', 'adult', 'old'], key='ms_ages')
    st.markdown("<hr>", unsafe_allow_html=True)
    return sb_ages


def age_calculator(char_race, char_age_range):
    global ages
    age_ranges = ages[char_race]
    mature_age, max_age = age_ranges.split('-')
    mature_age = int(mature_age)

    check_over_max_age = False  #TODO: implement this as a message to the user
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


def main():
    initialize()
    st.title(f'Fantasy NPC Generator')
    st.write(f'This generator is based on Dungeons and Dragons 5th edition to create unique fantasy NPCs')

    with st.sidebar:
        st.title('Options')
        st.write('Except for alignment, you can select multiple options but the generator will only choose one of each')

        selected_classes = classes_container()
        selected_age = age_container()
        char_alignment = alignment_container()
        selected_races = races_container()

    if len(selected_races) > 0 and len(selected_classes) > 0:
        if st.button('Generate NPC'):
            char_class, char_race, char_age = randomize_selection(selected_classes, selected_races, selected_age)
            st.write(f'classes: {char_class}, races: {char_race}, alignment: {char_alignment}, age: {char_age}')


if __name__ == "__main__":
    main()
