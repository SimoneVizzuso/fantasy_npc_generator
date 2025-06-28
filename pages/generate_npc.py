from nicegui import ui, app
import json
import os
from src.services.npc_generator import generate_npc
from src.services.npc_image import ImageGenerator
from src.utils.utils import save_npc_data

def load_data():
    with open('data/data.json') as f:
        d = json.load(f)
    return {
        'Common Races': d['races']['common'],
        'Rare Races': d['races']['rare'],
        'Exotic Races': d['races']['exotic'],
        'Classes': d['jobs'],
        'Age': ['young', 'adult', 'old'],
        'Alignment': d['alignment']
    }

checkbox_store = {}

def generate_npc_page():
    groups = load_data()
    app.add_static_files('/generated_images', 'generated_images')
    ui.label('NPC Generator').classes('text-h2 q-mb-md text-center')

    generated_npcs = load_generated_npcs()
    npc_names = [npc['name'] for npc in generated_npcs]

    with ui.row().classes('w-full items-start'):
        with ui.column().classes('w-1/5 q-pr-md q-gutter-lg'):
            btn = ui.button('Generate New NPC').classes('q-mb-lg')
            ui.label('Select Options').classes('text-h4')

            with ui.expansion("Character Archive").classes('w-full'):
                with ui.row().classes('w-full items-center'):
                    selected_npc = ui.select(npc_names, label='Select NPC already generated').classes('q-mb-md')
                    load_button = ui.button('Load NPC Details').classes('q-mb-md')

            for group_name, options in groups.items():
                with ui.expansion(group_name).classes('w-full'):
                    with ui.row().classes('justify-between'):
                        ui.button('Select all', on_click=lambda g=group_name, o=options: select_all(g, o))
                        ui.button('Clear all', on_click=lambda g=group_name: clear_all(g))
                    with ui.row().classes('w-full'):
                        per_col = (len(options) + 3) // 4
                        for i in range(4):
                            with ui.column().classes('items-start'):
                                for opt in options[i * per_col:(i + 1) * per_col]:
                                    cb = ui.checkbox(opt).props('dense color=white')
                                    checkbox_store.setdefault(group_name, []).append((cb, opt))

            generate_image_toggle = ui.switch('Generate Image', value=True).classes('q-mb-md')

            ui.label('Additional comments:')
            additional_information = ui.textarea().props('clearable').classes('w-full')

        with ui.column().classes('w-4/5 q-pl-md') as right_col:
            ui.label('Generated NPC').classes('text-h4 text-center')
            result_list = ui.column().classes('q-gutter-md')

        def load_npc_details(npc_name):
            npc = next((n for n in generated_npcs if n['name'] == npc_name), None)
            if npc:
                result_list.clear()
                with result_list:
                    if npc.get('image_filename'):
                        ui.image(f'/generated_images/{npc["image_filename"]}').classes('q-mb-md').style(
                            'max-width:400px')
                    for label, key in [
                        ('Name', 'name'),
                        ('Profession', 'profession'),
                        ('Description', 'description'),
                        ('Personality', 'personality'),
                        ('Marks', 'marks'),
                        ('Background', 'background'),
                        ('Hook', 'hook'),
                    ]:
                        text = npc.get(key, '')
                        markdown_text = f"**{label}:** {text}" if text else f"**{label}:** (non disponibile)"
                        ui.markdown(markdown_text).classes('text-body1')

        load_button.on('click', lambda: load_npc_details(selected_npc.value))

        def on_generate():
            nonlocal generated_npcs, npc_names
            def sel(group):
                return [lbl for cb, lbl in checkbox_store.get(group, []) if cb.value]

            sel_races = sel('Common Races') + sel('Rare Races') + sel('Exotic Races')
            sel_classes = sel('Classes')
            sel_ages = sel('Age')
            sel_align = sel('Alignment')

            if not sel_races:
                sel_races = groups['Common Races'] + groups['Rare Races'] + groups['Exotic Races']
            if not sel_classes:
                sel_classes = groups['Classes']
            if not sel_ages:
                sel_ages = groups['Age']
            if not sel_align:
                sel_align = groups['Alignment']

            name, personality, description, marks, profession, background, hook = generate_npc(
                char_job=sel_classes, char_race=sel_races, char_age=sel_ages,
                char_alignment=sel_align, additional_comments=additional_information.value
            )

            image_path = None
            if generate_image_toggle.value:
                prompt = f"A close-up portrait of {description} fantasy character"
                try:
                    image_gen = ImageGenerator()
                    image_path = image_gen.generate_npc_image(prompt)
                except Exception as e:
                    ui.notify(f"Image generation failed: {e}", color='negative')
                    image_path = None

            save_npc_data(
                name, personality, description, marks, profession, background, hook,
                os.path.basename(image_path) if image_path else None
            )

            # aggiorna lista npc caricata da file
            generated_npcs = load_generated_npcs()
            npc_names[:] = [npc['name'] for npc in generated_npcs]
            selected_npc._props['options'] = npc_names
            selected_npc.update()

            new_npc_data = {
                'name': name,
                'personality': personality,
                'description': description,
                'marks': marks,
                'profession': profession,
                'background': background,
                'hook': hook,
                'image_filename': os.path.basename(image_path) if image_path else None
            }

            selected_npc.value = name
            selected_npc.update()

            # mostra i dettagli nel result_list
            result_list.clear()
            with result_list:
                if image_path:
                    ui.image(f'/generated_images/{os.path.basename(image_path)}').classes('q-mb-md').style(
                        'max-width:400px')
                for label, text in [
                    ('Name', name),
                    ('Profession', profession),
                    ('Description', description),
                    ('Personality', personality),
                    ('Marks', marks),
                    ('Background', background),
                    ('Hook', hook),
                ]:
                    markdown_text = f"**{label}:** {text}" if text else f"**{label}:** (non disponibile)"
                    ui.markdown(markdown_text).classes('text-body1')

            ui.notify('NPC and image generated!')

        btn.on('click', on_generate)

def select_all(group, options):
    for cb, _ in checkbox_store.get(group, []):
        cb.value = True

def clear_all(group):
    for cb, _ in checkbox_store.get(group, []):
        cb.value = False

def load_generated_npcs():
    path = 'data/generated_npcs.json'
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        return []
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []