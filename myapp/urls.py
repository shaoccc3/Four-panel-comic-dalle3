from django.urls import path
from .views import generate_image, image_generator_page

urlpatterns = [
    path('', image_generator_page, name='image_generator_page'),
    path('create/', generate_image, name='generate_image'),
    # path('text',templates,name='text')
]
