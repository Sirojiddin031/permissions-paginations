from django.urls import path


from app_posts import views

app_name = 'posts'

urlpatterns = [
    path('',views.PostApiView.as_view(),name='list'),
    path('<slug:slug>/',views.PostDetailApiView.as_view(),name='detail'),
]