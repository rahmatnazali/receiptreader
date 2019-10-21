import io
import os
import io
from google.cloud import vision
from google.cloud.vision import types
import json
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict

# from .models import RawJson


class GoogleVisionApi:

    def __init__(self):
        #export GOOGLE_APPLICATION_CREDENTIALS="/Users/mtottrup/Desktop/BcLiqScanv1-6326a79539e7.json"
        self.client = vision.ImageAnnotatorClient()


    def ocr_image(self, image_model):
        # file_name = os.path.join(
        # os.path.dirname(__file__),
        # 'resources/wakeupcat.jpg')

        # # Loads the image into memory
        # with io.open(file_name, 'rb') as image_file:
        #     content = image_file.read()
        client = vision.ImageAnnotatorClient()
        content = image_model.binary.read()

        image = vision.types.Image(content=content)

        # Performs label detection on the image file
        response = client.text_detection(image=image)
        #texts = response.text_annotations
        texts = MessageToDict(response)
             #print('Texts:')
        # output = "OCR Output:"

        # for text in texts:
        #     output += '\n"{}"'.format(text.description)

        #     vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in text.bounding_poly.vertices])

        #     output += 'bounds: {}'.format(','.join(vertices))

        # todo: Get the file name

        res_json = json.dumps(texts)

        # with open('jsons/name.txt', 'wb+') as destination:
        #     destination.write(res_json)

        #     import pdb; pdb.set_trace()

        #     document.rawjson_set.create(
        #             document = document,
        #             name="Untitled",
        #             file=destination
        #         )

        #     document.save()


        #print(res_json)

        return res_json




    def label_image(self, document):

        # Instantiates a client
        client = vision.ImageAnnotatorClient()

        # The name of the image file to annotate
        content = document.image.file.read()

        # Loads the image into memory
       # with io.open(file_name, 'rb') as image_file:
           # content = image_file.read()

        image = types.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        print('Labels:')
        for label in labels:
            print(label.description)



# Imports the Google Cloud client library

# Instantiates a client


# The name of the image file to annotate
