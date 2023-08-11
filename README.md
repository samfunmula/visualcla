# Visual-Chinese-LLaMA-Alpaca
### 記得創images資料夾
### Start Fast API
```
cd main/
python3 api.py
```

### Start docker
```
bash runDocker.sh
```
## Support fomat

### Support image
* jpg / jpeg
* png
* gif
* url
* bmp
* tiff / tif 
* webp
* ico

## Run with GPU 
* It'll detect the largest memory to use .
* It uses single GPU , more GPU isn't better than one .(cost more memory)  

## Request
### curl
 * It'll automatically detect language

```

```
### Response
```

```

## Error
### UNSUPPORTED_INPUT_FORMAT
```
{'result':'UNSUPPORTED_INPUT_FORMAT'}
```
### UNSUPPORTED_HISTORY_FORMAT
```
{'result':'UNSUPPORTED_HISTORY_FORMAT'}
```
### INCORRECT_RANGE_OF_INPUT
```
{'result':'INCORRECT_RANGE_OF_INPUT'}
```
### INCORRECT_TYPE_OF_INPUT
```
{'result':'INCORRECT_TYPE_OF_INPUT'}
```
### UNSUPPORTED_IMAGE_FORMAT
```
{'result':'UNSUPPORTED_IMAGE_FORMAT'}
```