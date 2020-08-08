from django.urls import path , include
from blog_app import views
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from blog_app.sitemap import PostSitemap

sitemaps = {
    'Posts':PostSitemap,
}

app_name = 'blog'
urlpatterns = [
    
    path('', views.home, name='home'),

    path('home/', views.home, name='home'),

    path('blog_detail/<str:slug>/', views.blog_detail, name='blog_detail'),

    path('main_page/', views.main_page, name='main_page'),
    path('search/', views.search, name='search'),

    path('sign_up/', views.sign_up, name='sign_up'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),

    path('my_blogs/', views.my_blogs, name='my_blogs'),
    path('write_post/', views.write_post, name='write_post'),
    path('update_post/<int:id>/', views.update_post, name='update_post'),
    path('publish_post/<int:id>/', views.publish_post, name='publish_post'),
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),

    path('connect_mail/',views.connect_mail, name='connect_mail'),

    path('comment/<int:id>/', views.comment, name='comment'),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(), 
        name="password_reset_complete"),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
        name='sitemap'),
 
   
]