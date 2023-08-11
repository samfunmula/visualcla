# Visual-Chinese-LLaMA-Alpaca
### Start Fast API
```
cd main/
python3 api.py
```

### Start docker
```
bash runDocker.sh
```

### 模型合併
#### 參考 https://github.com/airaria/Visual-Chinese-LLaMA-Alpaca/tree/main 的 colab

## 圖片位置 
* ./images

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
* 可以用多顆GPU，目前是3顆

## Request
### 參數介紹
####  Request
* user_input : query => str
* input_image : img_path => str => look at Support image above
* max_new_token : int => default = 512 (可以不用) => 範圍 0 ~ 1024 
* top_p : float => default = 0.9 (可以不用) => 範圍 0 ~ 1
* top_k : int => default = 40 (可以不用) => 範圍 0 ~ 100
* temperature : float => default = 0.5 => 範圍 0 ~ 1

#### history
* 作用 : 模型會根據history(過往的聊天紀錄)，來進行回答
* 格式 : list ， 預設為空 (皆須為雙引號，單引號傳不進去)
```
"history": [{
    "type": "instruction",
    "value": "請描述這張圖",
    "first_instruction": true  => 這個可有可無，只有第一句會有
  },
  {
    "type": "response",
    "value": "這張圖片展示了一些哆啦A夢的宣傳海報，海報上可以看到一隻穿着宇航服、戴着頭盔的哆啦A夢。哆啦A夢似乎在微笑，可能表示他很高興能在太空中飛行。"
  }]
```



### curl
 * It'll automatically detect language

```
curl -X 'POST' \
  'http://localhost:9321/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "request": {
  "user_input" : "哆啦A夢是誰",
  "input_image" : "https://miro.medium.com/v2/resize:fit:1400/1*FKlRYAU5z-74RYqsTYrOAQ@2x.png",
  "max_new_token" : 512,
  "top_p" : 0.9,
  "top_k" : 40,
  "temperature" : 0.5
},
  "history": [{
    "type": "instruction",
    "value": "請描述這張圖",
    "first_instruction": true
  },
  {
    "type": "response",
    "value": "這張圖片展示了一些哆啦A夢的宣傳海報，海報上可以看到一隻穿着宇航服、戴着頭盔的哆啦A夢。哆啦A夢似乎在微笑，可能表示他很高興能在太空中飛行。"
  }]
}'
```
### Response
```
[
  [
    {
      "type": "instruction",
      "value": "請描述這張圖",
      "first_instruction": true
    },
    {
      "type": "response",
      "value": "這張圖片展示了一些哆啦A夢的宣傳海報，海報上可以看到一隻穿着宇航服、戴着頭盔的哆啦A夢。哆啦A夢似乎在微笑，可能表示他很高興能在太空中飛行。"
    },
    {
      "type": "instruction",
      "value": "哆啦A夢是誰"
    },
    {
      "type": "response",
      "value": "哆啦A夢是日本漫畫家藤子·F不二雄（原名藤本弘行）所創作的動畫角色。哆啦A夢是一個來自宇宙的外星人，他擁有神奇的能力，可以穿越時空，甚至可以製造出自己的物品。哆啦A夢在許多日本動畫和電影中都有出現，深受觀衆喜愛。"
    }
  ],
  {
    "user_input": "哆啦A夢是誰",
    "response": "哆啦A夢是日本漫畫家藤子·F不二雄（原名藤本弘行）所創作的動畫角色。哆啦A夢是一個來自宇宙的外星人，他擁有神奇的能力，可以穿越時空，甚至可以製造出自己的物品。哆啦A夢在許多日本動畫和電影中都有出現，深受觀衆喜愛。"
  }
]
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
### NO_SUCH_FILE_OR_DIRECTORY
```
{'result':'NO_SUCH_FILE_OR_DIRECTORY'}
```