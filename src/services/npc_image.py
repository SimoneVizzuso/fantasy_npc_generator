import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image
import os
import time


class ImageGenerator:
    def __init__(self, model_name="stabilityai/stable-diffusion-xl-base-1.0", device="cuda"):
        """
        Inizializza la pipeline di Stable Diffusion XL.

        :param model_name: Nome del modello pre-addestrato su Hugging Face.
        :param device: Dispositivo su cui eseguire il modello ("cuda" per GPU o "cpu").
        """
        self.device = device
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            model_name,
            torch_dtype=torch.float16
        ).to(self.device)

    def generate_npc_image(self, prompt, num_inference_steps=50, guidance_scale=7.5):
        """
        Genera un'immagine a partire da un prompt testuale.

        :param prompt: Il prompt testuale per la generazione dell'immagine.
        :param num_inference_steps: Numero di passi di inferenza.
        :param guidance_scale: Scala di guida per influenzare la coerenza con il prompt.
        :return: Percorso dell'immagine salvata.
        """
        # Genera l'immagine
        image = self.pipe(prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]

        # Crea la cartella per le immagini generate se non esiste
        os.makedirs("generated_images", exist_ok=True)

        # Crea un nome file basato sul timestamp
        timestamp = int(time.time() * 1000)
        image_path = f"generated_images/npc_{timestamp}.png"

        # Salva l'immagine
        image.save(image_path)
        return image_path
