from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.core.files.storage import default_storage
from PyPDF2 import PdfReader
from openai import OpenAI
import requests


# 從環境變數中獲取 API 金鑰
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("OPENAI_API_KEY"),
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
@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST':
        try:
            pdf_file = request.FILES.get('file')
            if not pdf_file:
                return JsonResponse({'error': 'No file provided'}, status=400)

            # 儲存 PDF 文件到伺服器
            file_path = default_storage.save(f"uploads/{pdf_file.name}", pdf_file)
            pdf_reader = PdfReader(open(file_path, "rb"))

            image_urls = []
            for page_num in range(len(pdf_reader.pages)):  # 使用 len(pdf_reader.pages) 來獲取頁數
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()

                    if text.strip():  # 確保文本內容非空
                        prompt = f"Four-panel comic strip with consistent character design and style. Maintain high resolution, avoid distortion or blurring There should be a story about the picture below the picture+ {text.strip()}"
                        response = client.images.generate(
                            model="dall-e-3",
                            prompt=prompt,
                            size="1024x1024",
                            n=1,
                        )
                        image_url = response.data[0].url if response.data else None
                        if image_url:
                            image_urls.append(image_url)

            if not image_urls:
                return JsonResponse({'error': 'No valid content found to generate images.'}, status=400)

            return JsonResponse({'image_urls': image_urls})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
#新聞生圖
@csrf_exempt
def generate_news(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            content = data.get('content', '').strip()

            if not title or not content:
                return JsonResponse({'error': 'Title and content are required'}, status=400)

            # 根據新聞標題和內容生成 prompt
            prompt = f"Generate a high-resolution image that represents the theme of this news article. Title: {title}. Content: {content}"
            
            # 設定圖片保存路徑，請確保該目錄存在
            save_directory = 'D://'  # 替換為你想要的保存路徑
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            
            image_urls = []
            for i in range(2):  # 執行十次
                # 使用你的圖像生成邏輯
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1792x1024",
                    quality="standard",
                    n=1,
                )

                # 獲取生成的圖片URL
                image_url = response.data[0].url if response.data else None
                
                if image_url:
                    # 打印生成的URL以進行調試
                    print(f"Generated image URL ({i+1}):", image_url)
                    
                    # 下載圖片
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_path = os.path.join(save_directory, f'image_{i+1}.png')
                        with open(image_path, 'wb') as f:
                            f.write(image_response.content)
                        image_urls.append(image_url)
                    else:
                        print(f"Failed to download image {i+1}")
                else:
                    print(f"No image generated for iteration {i+1}")
                    break  # 如果沒有生成圖片，終止迴圈
            
            return JsonResponse({'image_urls': image_urls})
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
