import torch
import visualcla
from visualcla.modeling_utils import DEFAULT_GENERATION_CONFIG
import os
from PIL import Image
from io import BytesIO
import hashlib
from typing import Optional
from aiohttp import ClientSession
import base64
from opencc import OpenCC

from fastapi.responses import JSONResponse
from dataclasses import dataclass

# produce image
async def fetch_image_base64(url: str) -> Optional[str]:
    try:
        async with ClientSession() as session:
            async with await session.get(url) as res:
                if res.status != 200:
                    return None
                img_byte = await res.read()
                img_base64 = base64.b64encode(img_byte).decode('utf-8')
                return img_base64
    except:
        return None

def process_image(image_encoded):
    decoded_image = base64.b64decode(image_encoded)
    image = Image.open(BytesIO(decoded_image))
    image_hash = hashlib.sha256(image.tobytes()).hexdigest()
    image_path = f'./images/{image_hash}.png'
    if not os.path.isfile(image_path):
        image.save(image_path)
    return os.path.abspath(image_path)


visualcla_model = 'visualcla'
gpus = "0"
cc = OpenCC('s2t')

def translate(target) : 
    for item in target:
        if "value" in item:
            item["value"] = cc.convert(item["value"])
    return target

def parse_text(text):
    """copy from https://github.com/GaiZhenbiao/ChuanhuChatGPT/"""
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>"+line
    text = "".join(lines)
    return text


def predict(input_text, image_path, max_new_tokens, top_p, top_k, temperature, history):
    DEFAULT_GENERATION_CONFIG.top_p = top_p
    DEFAULT_GENERATION_CONFIG.top_k = top_k
    DEFAULT_GENERATION_CONFIG.max_new_tokens = max_new_tokens
    DEFAULT_GENERATION_CONFIG.temperature = temperature
    if image_path is None:
        return [(input_text, "Image should not be empty。Please reupload image")], []
    
    with torch.no_grad():
        if True:
            response, history = visualcla.chat(model, image=image_path, text=input_text, history=history, generation_config=DEFAULT_GENERATION_CONFIG)
            return history
            

def setmodel(): 
    global model
    print("Loading the model...")
    load_type = torch.float16
    print(type(load_type))

    if torch.cuda.is_available():
            device = torch.device(0)
            device_map='auto'
    else:
        device = torch.device('cpu')
        device_map={'':device}

    print(f"device: {device}")
    print(f"device_map: {device_map}")

    base_model, tokenizer, _ = visualcla.get_model_and_tokenizer_and_processor(
        visualcla_model=visualcla_model,
        torch_dtype=load_type,
        default_device=device,
        device_map=device_map
    )
    model = base_model

    if device == torch.device('cpu'):
        model.float()
    model.eval()
    
@dataclass
class Errors:
    UNSUPPORTED_HISTORY_FORMAT = JSONResponse({'result':'UNSUPPORTED_HISTORY_FORMAT'},400)
    INCORRECT_RANGE_OF_INPUT = JSONResponse({'result':'INCORRECT_RANGE_OF_INPUT'},400)
    INCORRECT_TYPE_OF_INPUT = JSONResponse({'result':'INCORRECT_TYPE_OF_INPUT'},400)
    UNSUPPORTED_IMAGE_FORMAT = JSONResponse({'result':'UNSUPPORTED_IMAGE_FORMAT'},400)
    UNSUPPORTED_LANGUAGE = JSONResponse({'result':"UNSUPPORTED_LANGUAGE"},400)
    UNSUPPORTED_INPUT_FORMAT = JSONResponse({'result':'UNSUPPORTED_INPUT_FORMAT'},400)