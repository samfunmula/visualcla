import uvicorn
from fastapi import FastAPI, Request
from lib import *


print(" ## Set Model ##")
setmodel()

app = FastAPI()
@app.post('/')
async def upload_image(request : dict , history : list[dict] = []):
    print(" ## Start to Load Input ##")
    user_input = request.get("user_input")
    input_image = request.get("input_image")
    max_new_tokens = request.get("max_new_tokens",512)
    top_p = request.get("top_p",0.9)
    top_k = request.get("top_k",40)
    temperature = request.get("temperature",0.5)

        
    if(str(input_image).startswith('http')):
        input_image = await fetch_image_base64(input_image)

    image_path = process_image(input_image)

    output = predict(user_input,
                     image_path,
                     max_new_tokens,
                     top_p,
                     top_k,
                     temperature,
                     history)
    
    print("output:",translate(output))
    return translate(output)


if __name__ == '__main__' : 
    torch.cuda.empty_cache()
    import uvicorn
    uvicorn.run(app , host = "0.0.0.0" , port=9321)