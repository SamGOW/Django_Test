from django.urls import path
from authentication import views
from django.conf.urls import url
from django.conf.urls.static import static
from Django_LoginSystem import settings

app_name = 'authentication'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^checkLogin/$', views.checkLogin, name='checkLogin'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^writeBlog/$', views.writeBlogsV, name='writeBlogs'),
    path('viewBlog/<int:blog_id>/', views.viewBlog, name='viewBlogs'),
    url(r'^editProfile/$', views.editProfile, name='editProfile'),
    url(r'^profile/$', views.viewProfile, name='viewProfile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)