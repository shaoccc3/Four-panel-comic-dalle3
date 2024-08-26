from django.urls import path
from .views import generate_image, image_generator_page,upload_pdf,generate_news

urlpatterns = [
    path('', image_generator_page, name='image_generator_page'),
    path('create/', generate_image, name='generate_image'),
    path('upload-pdf/', upload_pdf, name='upload_pdf'),
     path('news/', generate_news, name='generate_news')
    # path('text',templates,name='text')
]
