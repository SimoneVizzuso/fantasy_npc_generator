from nicegui import ui
from pages.homepage import homepage_content
from pages.generate_npc import generate_npc_page as gen_content
from pages.chat_npc import chat_npc_page

def navbar():
    ui.add_head_html("""
    <style>
        body { background: #dedede !important; }
        .nicegui-content { background: transparent !important; }
    </style>""")
    with ui.header().classes('items-center'):
        with ui.row().classes('gap-2'):
            ui.button('Home',
                      on_click=lambda: ui.navigate.to('/'),
                      ).props('flat color=white')
            ui.button('Generate NPC',
                      on_click=lambda: ui.navigate.to('/generate_npc'),
                      ).props('flat color=white')
            ui.button('Chat NPC',  # aggiungi il pulsante per la chat
                      on_click=lambda: ui.navigate.to('/chat_npc'),
                      ).props('flat color=white')

@ui.page('/')
def home():
    navbar()
    homepage_content()

@ui.page('/generate_npc')
def generate_npc_route():
    navbar()
    gen_content()

@ui.page('/chat_npc')
def chat_npc_route():
    navbar()
    chat_npc_page()

ui.run()
