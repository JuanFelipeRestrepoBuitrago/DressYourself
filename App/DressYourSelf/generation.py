import requests


class APIs:
    API_URL_CAPTIONS = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {
        "CAPTIONS": {
            "Authorization": "Bearer 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"
        }
    }

    def query(self, image, api):
        response = requests.post(api, headers=self.headers[api], data=image.read())
        return response

    def get_caption(self, image):
        output = self.query(image, "CAPTIONS").json()
        caption = output[0]["generated_text"]
        return caption
