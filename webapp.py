import json
import random

import streamlit as st

from src.Character import Character
from src.npc_adventurer_chain import generate_npc
from src.utils import *

# st.set_page_config(layout="wide")

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


def races_container(col4):
    global races
    with col4:
        st.header('Races options')

        if 'common_races' not in st.session_state:
            st.session_state['common_races'] = []

        container_common_races = st.container()

        ms_common_race = container_common_races.multiselect('Select one or more common races:',
                                                            common_races, key='ms_common_race')

        def _common_select_all():
            st.session_state.ms_common_race = common_races

        st.button("Select all common", on_click=_common_select_all)

    st.markdown("<hr>", unsafe_allow_html=True)

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

    return list(ms_common_race + ms_rare_race + ms_exotic_race)


def classes_container():
    global classes
    st.header('Classes options')

    if 'classes' not in st.session_state:
        st.session_state['classes'] = []

    container_classes = st.container()

    ms_class = container_classes.multiselect('Select one or more classes:',
                                             classes, key='ms_class')

    def _class_select_all():
        st.session_state.ms_class = classes

    st.button("Select all classes", on_click=_class_select_all)

    return ms_class


def alignment_container():
    st.header('Alignment options')

    if 'alignment' not in st.session_state:
        st.session_state['alignment'] = []

    container_alignment = st.container()

    sb_alignment = container_alignment.selectbox('Select one alignment:',
                                                 alignment, key='sb_alignment')

    return sb_alignment


def age_container():
    st.header('Ages options')
    container_age = st.container()
    sb_ages = container_age.multiselect('Select one or more ages:',
                                        ['young', 'adult', 'old'], key='ms_ages')
    return sb_ages


def main():
    initialize()
    st.title(f'Fantasy NPC Generator')
    st.write(f'This generator is based on Dungeons and Dragons 5th edition to create unique fantasy NPCs')
    if 'characters_list' not in st.session_state:
        st.session_state.characters_list = []

    with st.expander('Set options'):
        st.title('Options')
        st.write('Except for alignment, you can select multiple options but the generator will only choose one of each')

        col1, col2 = st.columns(2)
        with col1:
            selected_age = age_container()
        with col2:
            char_alignment = alignment_container()
        st.markdown("<hr>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            selected_classes = classes_container()
        selected_races = races_container(col4)
        additional_comments = st.text_area('Add any additional comments here to take into account in the NPC '
                                           'generation.:', '')
    col3, col4 = st.columns(2)
    with col3:
        if st.button('Generate NPC'):
            cc = Character()
            with st.spinner('Your NPC is being generated... (estimated time: 30-40 seconds)'):
                cc.alignment = char_alignment
                cc.job, cc.race, cc.age = randomize_selection(
                    ages, classes, common_races + rare_races + exotic_races, selected_classes, selected_races, selected_age)
                cc.name, cc.personality, cc.description, cc.marks, cc.profession, cc.background, cc.hook = generate_npc(
                    cc.job, cc.race, cc.age, cc.alignment, additional_comments)
                st.session_state.characters_list.append(cc)
            # Store the character information in the session state
            st.session_state['character_info'] = {attr: value for attr, value in cc.__dict__.items()}
            # Generate the PDF and provide the download link as soon as the user clicks the button
            with col4:
                pdf_link = generate_pdf_npc(st.session_state.characters_list[-1])
                st.markdown(pdf_link, unsafe_allow_html=True)

    # Display the character information from the session state
    if 'character_info' in st.session_state:
        for attr, value in st.session_state['character_info'].items():
            st.write(f'{attr.capitalize()}: {value}')


if __name__ == "__main__":
    main()
