import json

import pandas as pd
import streamlit as st

from src.Character import Character
from src.npc_adventurer_chain import generate_npc
from src.utils import randomize_selection, generate_pdf_npc, save_character_json, load_characters_json

# st.set_page_config(layout="wide")

common_races = []
rare_races = []
exotic_races = []

classes = []
races = []
alignment = []
ages = []

json_file_path = 'data/characters.json'
data_path = 'data/data.json'


def initialize():
    global common_races, rare_races, exotic_races, classes, alignment, ages
    with open(data_path, 'r') as data_file:
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
    ms_exotic_race = container_exotic_races.multiselect('Select one or more exotic races:', exotic_races,
                                                        key='ms_exotic_race')

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
    ms_alignment = container_alignment.multiselect('Select one or more alignments:', alignment, key='ms_alignment')

    return ms_alignment


def age_container():
    st.header('Ages options')
    container_age = st.container()
    sb_ages = container_age.multiselect('Select one or more ages:', ['young', 'adult', 'old'], key='ms_ages')
    return sb_ages


def plot_characters(input_data_list=None):
    def _character_restore(index):
        # Filter the DataFrame to get the row with the specified index
        character_row = st.session_state["characters_dataframe_list"][
            st.session_state["characters_dataframe_list"]['Index'] == index]

        # If the character exists, convert the row to a dictionary and assign it to 'character_info'
        if not character_row.empty:
            st.session_state['character_info'] = character_row.iloc[0].to_dict()

        st.rerun()

    columns = st.columns((1, 1, 1, 1, 1, 1))
    fields = ['Name', 'Class', 'Race', 'Age', "Alignment", 'Restore']

    if len(input_data_list) > 0:
        # Create a DataFrame to display the characters in a table

        for col, field_name in zip(columns, fields):
            col.write(field_name)

        # Loop through the DataFrame rows
        for i, row in input_data_list.iterrows():
            col1, col2, col3, col4, col5, col6 = st.columns((1, 1, 1, 1, 1, 1))
            col1.write(row['Name'])  # index
            col2.write(row['Class'])  # email
            col3.write(row['Race'])  # unique ID
            col4.write(str(row['Age']))  # email status
            col5.write(row['Alignment'])
            button_type = "Restore"
            button_phold = col6.empty()  # create a placeholder
            do_action = button_phold.button(button_type, key=i)
            if do_action:
                _character_restore(row['Index'])
            st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.write('No characters yet.')


def main():
    initialize()
    st.title(f'Fantasy NPC Generator')
    st.write(f'This generator is based on Dungeons and Dragons 5th edition to create unique fantasy NPCs')

    if 'characters_list' not in st.session_state or 'characters_dataframe_list' not in st.session_state:
        st.session_state.characters_list, st.session_state.characters_dataframe_list = (
            load_characters_json(json_file_path)
        )

    if 'character_info' not in st.session_state:
        st.session_state.character_info = None

    with st.expander('Set options'):
        st.title('Options')
        st.write('You can select multiple options and the generator will only choose one of each')

        col1, col2 = st.columns(2)
        with col1:
            selected_age = age_container()
        with col2:
            selected_alignment = alignment_container()
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

            with st.spinner('Your NPC is being generated...\n(estimated time: 30-40 seconds)'):
                cc.job, cc.race, cc.age, cc.alignment = randomize_selection(
                    ages, classes, common_races + rare_races + exotic_races, alignment, selected_classes,
                    selected_races, selected_age, selected_alignment)
                cc.name, cc.personality, cc.description, cc.marks, cc.profession, cc.background, cc.hook = generate_npc(
                    cc.job, cc.race, cc.age, cc.alignment, additional_comments)
                st.session_state.characters_list.append(cc)

            st.session_state['character_info'] = {attr: value for attr, value in cc.__dict__.items()}

            input_data = pd.DataFrame({
                'Index': [cc.index],
                'Name': [cc.name],
                'Class': [cc.job],
                'Race': [cc.race],
                'Age': [cc.age],
                'Alignment': [cc.alignment],
                'Personality': [cc.personality],
                'Profession': [cc.profession],
                'Description': [cc.description],
                'Marks': [cc.marks],
                'Background': [cc.background],
                'Hook': [cc.hook]
            })

            if len(st.session_state["characters_dataframe_list"]) > 4:
                st.session_state["characters_dataframe_list"] = st.session_state["characters_dataframe_list"][:-1]
            st.session_state["characters_dataframe_list"] = pd.concat([input_data.iloc[[0]],
                                                                       st.session_state["characters_dataframe_list"]],
                                                                      ignore_index=True)

            save_character_json(json_file_path, cc)

            # Generate the PDF and provide the download link as soon as the user clicks the button
            with col4:
                pdf_link = generate_pdf_npc(st.session_state.characters_list[-1])
                st.markdown(pdf_link, unsafe_allow_html=True)

    # Display the character information from the session state
    if 'character_info' in st.session_state and st.session_state['character_info']:
        for attr, value in st.session_state['character_info'].items():
            st.write(f'{attr.capitalize()}: {value}')

    st.markdown("<hr>", unsafe_allow_html=True)

    st.header('Last 5 Characters Generated')
    plot_characters(st.session_state["characters_dataframe_list"])


if __name__ == "__main__":
    main()
