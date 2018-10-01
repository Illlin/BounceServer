#  This program will take a http request and then server a modified image to the client.
#  Illin 2018

# !/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from io import BytesIO
from PIL import Image

Target_resolution = (240, 320)


# HTTPRequestHandler class
class HTTPServerRequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        print("Image: ",end="")
        print(self.path[1:])

        location = self.path[1:]  # get Image Request Location
        if location == "" or location == "favicon.ico":
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Please add an image URL after the URL")
            return

        r = requests.get(location)  # Download Image

        #  Read data to Image object
        img = Image.open(BytesIO(r.content))

        # Find aspect ratios
        target_ratio = Target_resolution[0] / Target_resolution[1]
        image_ratio = img.size[0]/img.size[1]

        if image_ratio > target_ratio:  # image wider than needed
            #  Set height right then cut extra width
            #  Squish to right height and keep width regular
            img = img.resize((round(img.size[0] * (Target_resolution[1] / img.size[1])), Target_resolution[1]))
            #  Crop width to target
            img = img.crop((
                round(img.size[0]/2) - Target_resolution[0] / 2,
                0,
                round(img.size[0]/2) + Target_resolution[0] / 2,
                Target_resolution[1],
            ))
        else:  # Image taller than needed
            #  Set width correct then cut height
            #  Squish width
            img = img.resize((Target_resolution[0], (round(img.size[1] * (Target_resolution[0] / img.size[0])))))
            #  Crop width to target
            img = img.crop((
                0,
                round(img.size[1] / 2) - Target_resolution[1] / 2,
                Target_resolution[0],
                round(img.size[1] / 2) + Target_resolution[1] / 2,
            ))



        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'image/png')
        self.end_headers()

        # Send Image Data
        output = BytesIO(None)
        img.save(output,"png")
        self.wfile.write(output.getvalue())
        return

def load_png(file):
    pass

def run():
    print('starting server...')

    # Server settings
    server_address = ('0.0.0.0', 80)
    httpd = HTTPServer(server_address, HTTPServerRequestHandler)
    print('running server...')
    httpd.serve_forever()


run()