import requests
from diffusers import StableDiffusionControlNetInpaintPipeline, ControlNetModel
from diffusers.utils import load_image
from diffusers.schedulers import DDIMScheduler
import numpy as np
import torch


def make_inpaint_condition(image, image_mask):
    image = np.array(image.convert("RGB")).astype(np.float32) / 255.0
    image_mask = np.array(image_mask.convert("L")).astype(np.float32) / 255.0
    assert image.shape[0:1] == image_mask.shape[0:1], "image and image_mask must have the same image size"
    image[image_mask > 0.5] = -1.0  # set as masked pixel
    image = np.expand_dims(image, 0).transpose(0, 3, 1, 2)
    image = torch.from_numpy(image)
    return image


def get_outfit(caption: str, image, mask_image):
    init_image = load_image(image)
    init_image = init_image.resize((512, 512))

    generator = torch.Generator(device="cpu").manual_seed(1)
    
    mask_image = load_image(mask_image)
    mask_image = mask_image.resize((512, 512))

    control_image = make_inpaint_condition(init_image, mask_image)
    controlnet = ControlNetModel.from_pretrained(
        "lllyasviel/control_v11p_sd15_inpaint", torch_dtype=torch.float32
    )

    pipe = StableDiffusionControlNetInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float32
    )
    pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)

    image = pipe(
        caption,
        num_inference_steps=20,
        generator=generator,
        eta=1.0,
        image=init_image,
        mask_image=mask_image,
        control_image=control_image,
    ).images[0]

    return image


class APIs:
    api_urls = {
        "CAPTIONS": "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    }
    headers = {
        "CAPTIONS": {
            "Authorization": "Bearer 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"
        }
    }

    def query(self, image, api):
        response = requests.post(self.api_urls[api], headers=self.headers[api], data=image.read())
        return response

    def get_caption(self, image):
        output = self.query(image, "CAPTIONS").json()
        caption = output[0]["generated_text"]
        return caption
