from nicegui import ui, app
import json, os
from starlette.responses import FileResponse
from uuid import uuid4
from src.services.npc_chat import chat_with_npc
from dotenv import load_dotenv

load_dotenv()
ollama_model = os.getenv('OLLAMA_MODEL', 'qwen3:8b')

npc_file = 'data/generated_npcs.json'
if not os.path.exists('data'):
    os.makedirs('data')

if os.path.exists(npc_file):
    with open(npc_file, encoding='utf-8') as f:
        npcs = json.load(f)
else:
    npcs = []
    with open(npc_file, 'w', encoding='utf-8') as f:
        json.dump(npcs, f, ensure_ascii=False, indent=2)

npc_dict = {npc['name']: npc for npc in npcs}
chat_history = {}
if npc_dict:
    selected_npc = list(npc_dict.keys())[0]
else:
    selected_npc = None

app.add_static_files('/generated_images', 'generated_images')

@app.get('/generated_images/{filename}')
def serve_image(filename: str):
    path = os.path.join('generated_images', filename)
    return FileResponse(path) if os.path.exists(path) else FileResponse('path/to/default.png')

def get_npc_image(npc):
    fn = npc.get('image_filename')
    return f'/generated_images/{fn}' if fn else None


def chat_npc_page():
    global selected_npc

    def on_npc_change(e):
        global selected_npc
        selected_npc = e.value
        chat_box.refresh()
        left_panel.refresh()

    @ui.refreshable
    def left_panel():
        if not selected_npc or selected_npc not in npc_dict:
            ui.label("Nessun NPC selezionato.").classes('text-xl text-gray-500')
            return
        npc = npc_dict[selected_npc]
        with ui.column().classes('p-4 bg-white rounded shadow flex flex-col items-center'):
            # Immagine grande e centrata
            img = get_npc_image(npc)
            if img:
                ui.image(img).classes('rounded shadow-lg mb-4').style('width: 100%; max-width: 300px; height: auto;')
            # Dettagli
            ui.label(npc['name']).classes('text-3xl font-bold mb-2')
            ui.label(f"Profession: {npc.get('profession','')}").classes('mb-1')
            ui.label(f"Personality: {npc.get('personality','')}").classes('mb-1')
            ui.label(f"Description: {npc.get('description','')}").classes('mb-1')
            ui.label(f"Distinctive marks: {npc.get('marks','')}").classes('mb-1')
            ui.label(f"Background: {npc.get('background','')}").classes('mb-1')
            ui.label(f"Hook: {npc.get('hook','')}").classes('mb-1')

    @ui.refreshable
    def chat_box():
        with ui.column().classes('w-full overflow-auto p-4 bg-white rounded shadow flex-grow'):
            for msg in chat_history.get(selected_npc, []):
                align = 'justify-end' if msg['sender'] == 'user' else 'justify-start'
                bubble = 'bg-blue-100' if msg['sender'] == 'user' else 'bg-green-100'
                with ui.row().classes(f'w-full {align} items-start mb-2'):
                    if msg['sender'] == 'npc':
                        img_url = get_npc_image(npc_dict[selected_npc])
                        if img_url:
                            ui.image(img_url).classes('rounded w-10 h-10 mr-2')
                    ui.label(msg['text']).classes(f'p-3 rounded-xl {bubble} max-w-[70%]')

    def on_send():
        user_msg = input_box.value.strip()
        if not user_msg:
            return
        chat_history.setdefault(selected_npc, []).append({'sender':'user','text':user_msg})
        reply = chat_with_npc(npc_dict[selected_npc], ollama_model, [{'role':'user','content':user_msg}])
        chat_history[selected_npc].append({'sender':'npc','text':reply})
        input_box.value = ''
        chat_box.refresh()
        ui.run_javascript('window.scrollTo(0, document.body.scrollHeight);')

    @ui.refreshable
    def npc_selector():
        return ui.select(list(npc_dict.keys()), value=selected_npc, on_change=on_npc_change) \
            .props('outlined dense').classes('w-64')

    with ui.row().classes('items-center p-4'):
        npc_selector()
        ui.label('Chat with NPC').classes('text-lg ml-4')

    with ui.row().style('width: 100%; height: 100vh; display: flex; flex-wrap: nowrap; gap: 1.5rem; padding: 1rem'):
        with ui.column().style('flex: 0 0 33%; overflow-y: auto;'):
            left_panel()
        with ui.column().style('flex: 1; display: flex; flex-direction: column; height: 80%;'):
            chat_box()
            with ui.row().classes('items-center bg-white rounded-full shadow-lg p-2 mt-4').style('width: 100%'):
                input_box = ui.input(
                    placeholder='Type your message…',
                ).props('clearable dense').classes('flex-grow rounded-full')
                input_box.on('keydown.enter', lambda _: on_send())
                ui.button('Send', on_click=on_send).props('color=primary').classes('rounded-full ml-2')

