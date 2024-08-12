"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# 根URL視圖函數
def home(request):
    return HttpResponse(""""
        <html>
            <body>
                <h1>Welcome to the home page!</h1>
                <button onclick="window.location.href='http://127.0.0.1:8080/generate-image/'">
                    Go to Generate Image
                </button>
            </body>
        </html>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate-image/', include('myapp.urls')),
    # path('text',include('myapp.urls'))
    path('', home),  # 根URL處理
]



