from kandinsky2 import get_kandinsky2
import torch

model = get_kandinsky2('cuda', task_type='text2img', model_version='2.2')

def generate_image(prompt: str, path_to_save: str, w=1920, h=1080):
    images = model.generate_text2img(
        prompt,
        h=h,
        w=w,
    )
    image = images[0]
    image.save(path_to_save)

    return path_to_save