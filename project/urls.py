"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from .views import modify_student  # Import the view for modifying student details

from app import views

urlpatterns = [  

 path('adminHome/', views.adminHome, name='adminHome'),
    path('', views.index),
    path('studentReg/', views.studentReg),
    path('login/', views.login),
    path('log_out/', views.log_out, name='logout'),

# =========================  COORDINATOR(ADMIN)  ===========================
    path('adminHome/',views.adminHome),
    path('updatestudent/<int:student_id>/', views.updatestudent, name='updatestudent'),
    path('deletestudent/<int:student_id>/', views.deletestudent, name='deletestudent'),

# ==============================  STUDENT  =================================
    path('studentHome/', views.studentHome),
    path('addProjectAbstract/', views.performance_prediction),
    path('blogdetail/',views.blogdetail),
# =================================  GUIDE  ================================   
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

