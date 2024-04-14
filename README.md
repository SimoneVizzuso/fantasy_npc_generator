# Fantasy NPC Generator
This is a simple NPC generator for fantasy settings. It is designed based on Dungeons and Dragons 5th Edition, but can be used for any fantasy setting. It is designed to be used by a Dungeon Master to quickly generate NPCs for their campaign. It is a work in progress and will be updated as I have time to work on it.

## How to Use
The first step is setting up a Python Environment: this guide will walk you through the process for setting up a new PC without Python.

### Step 1: Download and Install Python

- Open your web browser and navigate to the official Python website [here](python.org).  
- Click on the "Downloads" tab located on the top navigation bar and choose.  
- Choose the **python version 3.10** for your operating system (Windows, macOS, or Linux) and click on the download link.  
- Once the download is complete, run the installer and follow the installation instructions provided.  

### Step 2: Verify Python Installation

- After the installation is complete, open your terminal, type `python --version` and press Enter. This command should display the installed Python version.  
- Check that the version is `3.10`

### Step 3: Setting Up the Environment

- Ensure that you have the necessary dependencies installed.
- Open the terminal in *fantasy_npc_generator* folder, type `pip install -r requirements.txt` and press Enter.

### Step 4: Install the LLM

- For the generator to work, you need to install a LLM (Large Language Model). The fastest and easiest way to do this is to use Ollama.
- You can download Ollama from [here](https://ollama.com/)
- Once you have downloaded Ollama, you need to choose an LLM. This generator is optimized for Mistral 8x7b (or Mixtral).
  - For Mistral 8x7b you need at least 48GB of RAM and a GPU with at least 24GB of VRAM.
    - To use Mistral 7b, you need to open the terminal and type `ollama pull mixtral` and press Enter.
- Once you have downloaded the LLM, you need to set the environment variable `OLLAMA_MODEL` in the file model.env
  - To use Mistral 8x7b, you need to set `OLLAMA_MODEL=mixtral`.

### Step 5: Open the web app

- Navigate to *fantasy_npc_generator* using the command prompt or terminal.  
- Type `streamlit run webapp.py` and press Enter.
- A page will be opened in the default browser. If not, simply click on the Local URL link that will appear in the terminal.
- When the web app is opened, you can start to use it to generate your NPCs!