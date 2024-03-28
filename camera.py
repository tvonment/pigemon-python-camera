import requests
from picamera import PiCamera
from time import sleep
import asyncio
import time
import os

# Replace with your endpoint URL and prediction key
ENDPOINT_URL = "https://pigemonvision-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/976bfd0a-30e1-48ff-b61c-ba2969826049/detect/iterations/Iteration5/image"
PREDICTION_KEY = "9a020bd42dbd4b70b5e6714de81544ac"

# The path to the image file you want to send
IMAGE_PATH = "/home/pigemon/image.jpg"

async def capture_image(image_path):
    camera = PiCamera()
    camera.start_preview()  # Camera warm-up time
    camera.capture(image_path)
    camera.stop_preview()

def send_image_to_custom_vision(endpoint_url, prediction_key, image_path):
    # Open the image file in binary mode
    with open(image_path, "rb") as image_file:
        # Set up the header with the prediction key
        headers = {
            "Content-Type": "application/octet-stream",
            "Prediction-key": prediction_key
        }

        # Send a post request with the image file and headers
        response = requests.post(endpoint_url, headers=headers, data=image_file)

        # Check the status code and return the response if successful
        if response.status_code == 200:
            return response.json()
        else:
            # If not successful, raise an error with the response to help with debugging
            raise Exception(f"Request failed: {response.text}")

async def main():
    # Call the function and print the returned results
    try:
        start_time = time.time()
        await capture_image(IMAGE_PATH)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Image Capture Execution Time: {execution_time}")
        start_time = time.time()
        prediction_response = send_image_to_custom_vision(ENDPOINT_URL, PREDICTION_KEY, IMAGE_PATH)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Image Recognition Execution Time: {execution_time}")
        #print(f"Prediction Results: {prediction_response}")
        data = prediction_response
        if data['predictions'] == []:
            print("Nothing recognized in the image.")
        if data['predictions'] != []:
            counter = 0
            for prediction in data['predictions']:
                if prediction['tagName'] == "columbidae" and prediction['probability'] > 0.8:
                    counter += 1
            if counter > 0: 
                print("Pigeon(s) recognized in the image.")
            else:
                print("No Pigeons recognized in the image.")
        os.remove(IMAGE_PATH)
    except Exception as e:
        print(e)

asyncio.run(main())
