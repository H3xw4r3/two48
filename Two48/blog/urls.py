from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog_home'),
    path('dashboard/', views.dashboard, name="dashboard"),
    #path('<slug:slug>/', views.post_view, name='post_view'),

    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('register/login/', views.login, name="login"),

    path('create/', views.create_post, name='createpost'),
    path('search/', views.search, name="search"),
    path('<int:pk>/', views.post_view, name="post_view"),
    path('<category>/', views.category_view, name="category"),
]