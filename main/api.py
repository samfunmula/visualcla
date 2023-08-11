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

    if type(user_input) != str : 
        return Errors.UNSUPPORTED_INPUT_FORMAT
    
    if type(history) != list : 
        return Errors.UNSUPPORTED_HISTORY_FORMAT
    
    if max_new_tokens < 0 or max_new_tokens > 1024 : 
        return Errors.INCORRECT_RANGE_OF_INPUT
    elif type(max_new_tokens) != int : 
        return Errors.INCORRECT_TYPE_OF_INPUT
    
    if top_p < 0 or top_p > 1 : 
        return Errors.INCORRECT_RANGE_OF_INPUT
    elif type(top_p) != float : 
        return Errors.INCORRECT_TYPE_OF_INPUT
    
    if top_k < 0 or top_k > 100 : 
        return Errors.INCORRECT_RANGE_OF_INPUT
    elif type(top_k) != int : 
        return Errors.INCORRECT_TYPE_OF_INPUT
    
    if temperature < 0 or temperature > 1 : 
        return Errors.INCORRECT_RANGE_OF_INPUT
    elif type(temperature) != float : 
        return Errors.INCORRECT_TYPE_OF_INPUT
    
    image_path = input_image
    
    try : 
        if all(format not in str(image_path) for format in image_format) : 
            return Errors.UNSUPPORTED_IMAGE_FORMAT
        try : 
            if(str(input_image).startswith('http')):
                input_image = await fetch_image_base64(input_image)
                image_path = process_image(input_image)
        except : 
            return Errors.NO_SUCH_FILE_OR_DIRECTORY
        with open(image_path,'rb') as file : 
            pass
    except : 
        return Errors.NO_SUCH_FILE_OR_DIRECTORY
    
    output = predict(user_input,
                     image_path,
                     max_new_tokens,
                     top_p,
                     top_k,
                     temperature,
                     history)
    print("output:",translate(output))
    torch.cuda.empty_cache()
    return translate(output)


if __name__ == '__main__' : 
    torch.cuda.empty_cache()
    import uvicorn
    uvicorn.run(app , host = "0.0.0.0" , port=9321)