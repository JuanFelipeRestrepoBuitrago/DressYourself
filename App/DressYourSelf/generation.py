import requests
from diffusers import StableDiffusionControlNetInpaintPipeline, ControlNetModel
from diffusers.schedulers import DDIMScheduler
import numpy as np
import torch
from django.core.files.storage import default_storage
from PIL import Image
import os
from django.conf import settings

def get_outfit_caption(tops: list, bottoms: list, footwears: list, others: list):
    """
    This function takes a list of tops, bottoms, footwears and others and returns a caption
    :param tops: list of tops
    :param bottoms: list of bottoms
    :param footwears: list of footwears
    :param others: list of others
    :return: caption
    """
    caption = "A beautiful person with: "
    if tops is not None and len(tops) > 0:
        for top in tops:
            caption += top.description + ", "
    if bottoms is not None and len(bottoms) > 0:
        for bottom in bottoms:
            caption += bottom.description + ", "
    if footwears is not None and len(footwears) > 0:
        for footwear in footwears:
            caption += footwear.description + ", "
    if others is not None and len(others) > 0:
        for other in others:
            caption += other.description + ", "
    if caption != "" and caption != " " and caption[-2:] == ", ":
        caption = caption[:-2]
    else:
        caption = "Same Image"
    return caption


def make_inpaint_condition(image, image_mask):
    """
    This function takes an image and a mask and returns a masked image
    :param image: original image
    :param image_mask: mask
    :return:
    """
    image = np.array(image.convert("RGB")).astype(np.float32) / 255.0
    image_mask = np.array(image_mask.convert("L")).astype(np.float32) / 255.0
    assert image.shape[0:1] == image_mask.shape[0:1], "image and image_mask must have the same image size"
    image[image_mask > 0.5] = -1.0  # set as masked pixel
    image = np.expand_dims(image, 0).transpose(0, 3, 1, 2)
    image = torch.from_numpy(image)
    return image


def get_outfit(caption: str, image, mask_image):
    """
    This function takes a caption, an image and a mask and returns an image of the new outfit
    :param caption: Caption of the outfit to be generated
    :param image: Original image
    :param mask_image: Mask
    :return: Image of the new outfit
    """
    init_image = default_storage.open(image, "rb")
    init_image = Image.open(init_image)
    init_image = init_image.resize((512, 512))

    generator = torch.Generator(device="cpu").manual_seed(1)

    mask_image = default_storage.open(mask_image, "rb")
    mask_image = Image.open(mask_image)
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

    with default_storage.open(os.path.join("uploaded_images", "generated_image.png"), "wb") as destination:
        print(destination)
        image.save(destination)

    return "/media/uploaded_images/generated_image.png", os.path.join("uploaded_images", "generated_image.png")


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
        """
        This function takes an image and an api and returns the response of the api

        :type image: file
        :param image: image to be sent to the api
        :param api: api to be used
        :return: response of the api
        """
        response = requests.post(self.api_urls[api], headers=self.headers[api], data=image.read())
        return response

    def get_caption(self, image):
        """
        This function takes an image and returns a caption

        :param image: image to be captioned
        :return: caption
        """
        output = self.query(image, "CAPTIONS").json()
        caption = output[0]["generated_text"]
        return caption
