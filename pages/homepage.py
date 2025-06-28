from nicegui import ui

def homepage_content():
    # Colonna centrale, contenuti allineati in alto
    with ui.column().classes('items-center justify-start q-pt-xl q-px-md w-full'):
        # Titolo centrato
        ui.label('Fantasy NPC Generator').classes('text-h2 q-mb-md text-center')

        # Contenitore testo centrato con giustificazione
        ui.html('''
            <div class="text-justify text-center text-[1.35em]"
                 style="max-width:700px;">
            Benvenuto nel Fantasy NPC Generator!<br>
            Questo strumento ti permette di generare NPC unici per le tue campagne fantasy e di chattare con loro grazie all'intelligenza artificiale.<br><br>
            <b>- Vai su <span style="color:#90caf9;">Generate NPC</span> per creare un nuovo personaggio.<br>
            - Vai su <span style="color:#90caf9;">Chat with NPC</span> per parlare con il tuo NPC.</b>
            </div>
        ''')
