#!/usr/bin/env python
import os, requests, json, mammoth, time
from rich import print
from rich.markdown import Markdown
from dotenv import load_dotenv
from lib.openlib import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS

from tools.functions import handle_user_input, save_conversation


app = Flask(__name__)
# app.debug = True
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
CORS(app)


# Get API key
load_dotenv()
api_key = os.getenv("open_ai_key")
# brave_api = os.getenv("brave_api")
assistant_id = os.getenv("assistant_id")
print("api_key-----", api_key)
client = OpenAI(api_key=api_key, assistant_id=assistant_id)
client.assistant_id = str(assistant_id)
client.load_thread()
assistants = client.list_assistants()
# print("assistants-------", assistants)

def file_extract():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400

    if file:
        result = mammoth.extract_raw_text(file)
        content = result.value  # Extracted content
    return content

conversation = []

# while True:
#     if client.debug_mode == True:
#         user_input = input("Debug mode enabled: ")
#     else:
#         user_input = input(f"\n[{client.assistant_name}]: ")

#     print("-------------------------------------------------------------------------")

#     if user_input == "quit" or user_input == "q":
#         break
#     elif user_input == "save":
#         save_conversation(conversation)
#     elif handle_user_input(user_input, client):
#         gpt_output = client.output()
#         conversation.append(gpt_output)
#         markdown = Markdown(gpt_output, code_theme="one-dark")
#         print(markdown)

#     print("-------------------------------------------------------------------------")

@app.route('/api/proprietary-assistant', methods = ['POST'])
def proprietary_assistant():
    prompt = request.json["prompt"]
    print(prompt)
    client.create_message(prompt)
    client.create_run()
    gpt_output = client.output()
    conversation.append(gpt_output)
    markdown = Markdown(gpt_output, code_theme="one-dark")
    print('-------------------MARK-----------------', markdown)

    return jsonify({'result': gpt_output})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    print(request.form)
    tone = request.form.get("tone")
    print('-- Start ---', file.filename)
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400

    if file:
        # filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Use mammoth to extract content from the docx file
        # with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as file_data:
        result = mammoth.extract_raw_text(file)
        content = result.value  # Extracted content
        prompt = content + "; Tone of Voice: " + tone
        print(prompt)
        client.create_message(prompt)
        client.create_run()
        gpt_output = client.output()
        conversation.append(gpt_output)
        markdown = Markdown(gpt_output, code_theme="one-dark")
        print('-------------------MARK-----------------', markdown)

        return jsonify({'result': gpt_output})

@app.route('/add-instruction', methods=['POST'])
def add_instruction():
    instructions = request.json["instructions"]
    print(instructions)
    add_instruction_url = "https://api.openai.com/v1/assistants/asst_a96Xkrj84wvRb7dARe7W4KMP"

    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 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",
    "OpenAI-Beta": "assistants=v1"
    }

    data ={
    "instructions": "You are a blog generator. You have to generate well-marked blogs. " + instructions,
    "name": "Blog Generator",
    "tools": [{"type": "code_interpreter"}],
    "model": "gpt-4"
    }

    response = requests.post(add_instruction_url, json=data, headers=headers)
    if(response):
        print(response)

    return response.text

@app.route('/image-generator', methods=['POST'])
def image_generator():
    if request.form.get('prompt'):
        prompt = request.form.get('prompt')
        
    else:
        file_content = file_extract()
        instruction = request.form.get('instruction')
        prompt = (file_content + instruction)

    negative_prompt = request.form.get('negative_prompt')
    model_id = request.form.get("model_id")
        
    print(prompt)
    print(negative_prompt)
    print(model_id)

    image_post_url = "https://cloud.leonardo.ai/api/rest/v1/generations"

    headers ={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer 688e061a-fde1-46f2-ab8f-5237c9a6ff25",
    }

    data ={ 
        "height": 512,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": 512,
        # "alchemy": True,
        # "photoReal": True,
        # "photoRealStrength": 0.55,
        "presetStyle": "CINEMATIC",
        "modelId": model_id,
    }

    response = requests.post(image_post_url, json = data, headers = headers)
    generation_id = json.loads(response.text)['sdGenerationJob']['generationId']
    print("post-response-------------->", generation_id)

    image_get_url ="https://cloud.leonardo.ai/api/rest/v1/generations/" + generation_id

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer 688e061a-fde1-46f2-ab8f-5237c9a6ff25",
    }

    
    while True:
        response = requests.get(image_get_url, headers=headers)
        print(json.loads(response.text))
        generated_images = json.loads(response.text)['generations_by_pk']['generated_images']
        print(generated_images)
        if generated_images != []:
            generated_image = generated_images[0]['url']
            break
        else:
            time.sleep(5)
    print(generated_image)


    return generated_image


@app.route('/init-image-generator', methods=['POST'])
def init_image_generator():
    if request.form.get('prompt'):
        prompt = request.form.get('prompt')
        negative_prompt = request.form.get('negative_prompt')
    else:
        file_content = file_extract()
        instruction = request.form.get('instruction')
        prompt = (file_content + instruction)

    image = request.files["init_image"]
    print(image.filename)

    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer 688e061a-fde1-46f2-ab8f-5237c9a6ff25"
    }
    url = "https://cloud.leonardo.ai/api/rest/v1/init-image"

    payload = {"extension": "jpg"}

    response = requests.post(url, json=payload, headers=headers)

    print(response.status_code)

    fields = json.loads(response.json()['uploadInitImage']['fields'])

    url = response.json()['uploadInitImage']['url']

    image_id = response.json()['uploadInitImage']['id']

    files = {'file': image}

    response = requests.post(url, data=fields, files=files)

    print(response.status_code)

    url = "https://cloud.leonardo.ai/api/rest/v1/generations"

    payload = {
        "height": 512,
        "init_image_id": image_id, # Setting model ID to Leonardo Creative
        "init_strength": 0.3,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": 512,
        # "imagePrompts": [image_id], # Accepts an array of image IDs
        "alchemy": True,
        "photoReal": True,
        "photoRealStrength": 0.55,
        "presetStyle": "CINEMATIC"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.status_code)

    generation_id = response.json()['sdGenerationJob']['generationId']

    url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id

    time.sleep(20)

    response = requests.get(url, headers=headers)

    print(response.text)

    generated_images = json.loads(response.text)['generations_by_pk']['generated_images']

    generated_image = generated_images[0]['url']

    return generated_image


@app.route('/dall-image-generator', methods=['POST'])
def dall_image_generator():
    if request.form.get('prompt'):
        prompt = request.form.get('prompt')
    else:
        file_content = file_extract()
        instruction = request.form.get('instruction')
        prompt = (file_content + instruction)

    print("prompt------------>",prompt)
    size = request.form.get('size')
    quality = request.form.get('quality')
    

    url = "https://api.openai.com/v1/images/generations"

    headers ={
        "Content-Type": "application/json",
        "Authorization": "Bearer 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",
    }

    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality":quality
    }

    response = requests.post(url, json=data, headers=headers)
    print(response.text)

    generated_image = json.loads(response.text)['data'][0]
    print(generated_image)

    return generated_image


@app.route('/stability-image-generator', methods=['POST'])
def stability_image_generator():
    print("----request success")
    prompt = request.form.get('prompt')   
    image_strength = request.form.get('image_strength')
    steps = request.form.get('steps')
    cfg_scale = request.form.get('cfg_scale')
    style_preset = request.form.get('style_preset')
    negative_prompt = request.form.get('negative_prompt')
    model = request.form.get('model')


    if 'init_image' not in request.files:
        if model == "Stable Diffusion XL 1.0":
            width = 1024
            height = 1024
            url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        else:
            width = 512
            height = 512
            url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"

        headers ={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-QJ3pj9ignXLZT8IgAG8tkggeVkzFQj61gZKmIxOcFVaSMIsP",
        }

        data = {
            "steps": int(steps),
            "width": width,
            "height": height,
            "seed": 0,
            "cfg_scale": int(cfg_scale),
            "samples": 1,
            "style_preset": style_preset,
            "text_prompts": [
                {
                "text": prompt,
                "weight": 1
                },
            ]
        }

        if negative_prompt:
            negative_prompt = {
                "text": negative_prompt,
                "weight": -1
                }
            data["text_prompts"].append(negative_prompt)

        response = requests.post(url, json=data, headers=headers)
        image_base64 = json.loads(response.text)['artifacts'][0]['base64']

    else:
        init_image = request.files["init_image"]        

        if model == "Stable Diffusion XL 1.0":
            url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image"
        else:
            url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/image-to-image"

        

        headers ={
            "Accept": "application/json",
            "Authorization": "Bearer sk-QJ3pj9ignXLZT8IgAG8tkggeVkzFQj61gZKmIxOcFVaSMIsP",
        }
        
        data={
        "init_image_mode": "IMAGE_STRENGTH",
		"image_strength": float(image_strength),
		"steps": int(steps),
		"seed": 0,
		"cfg_scale": int(cfg_scale),
		"samples": 1,
		"text_prompts[0][text]": prompt,
		"text_prompts[0][weight]": 1,
		"text_prompts[1][text]": negative_prompt+" ",
		"text_prompts[1][weight]": -1,
    }
        
        files = {
            "init_image": init_image
        }

        response = requests.post(url=url, headers=headers, data=data, files=files)

        image_base64 = json.loads(response.text)['artifacts'][0]['base64']

    return image_base64



if __name__ == "__main__":
    print("kkk")
    app.run(port=5050)
