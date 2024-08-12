from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from openai import OpenAI

# 從環境變數中獲取 API 金鑰
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="",
)

def image_generator_page(request):
    return render(request, 'image_generator.html')

@csrf_exempt
def generate_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = "Four-panel comic strip with consistent character design and style. Maintain high resolution, avoid distortion or blurring"+data.get('prompt', '').strip()
            if not prompt:
                return JsonResponse({'error': 'Prompt is required'}, status=400)

            # 直接使用前端提供的完整 prompt
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1792x1024",
                quality="standard",
                n=1,
            )
            # 正確解析 response 對象，假設 response 是一個 Pydantic 模型
            image_url = response.data[0].url if response.data else None
            return JsonResponse({'image_url': image_url})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:  # 捕捉所有其他可能的異常
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
# 文字生成
@csrf_exempt 
def generate_poem(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '').strip()
            if not prompt:
                return JsonResponse({'error': 'Prompt is required'}, status=400)

            client = openai.OpenAI(api_key='your_openai_api_key')
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                    {"role": "user", "content": prompt}
                ]
            )
            poem = completion['choices'][0]['message']['content']
            return JsonResponse({'poem': poem})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except openai.error.OpenAIError as e:
            # 具體捕捉 OpenAI API 的錯誤
            return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

#傳回參數
# st: 2024-08-09T08:15:29Z
# se: 2024-08-09T10:15:29Z
# sp: r
# sv: 2023-11-03
# sr: b
# rscd: inline
# rsct: image/png
# skoid: d505667d-d6c1-4a0a-bac7-5c84a87759f8
# sktid: a48cca56-e6da-484e-a814-9c849652bcb3
# skt: 2024-08-09T07:09:06Z
# ske: 2024-08-10T07:09:06Z
# sks: b
# skv: 2023-11-03
# sig: 3yLx77T3nlLmJkoG/Vni1O6bdNXNBbFJeaEoH1EGS10=
