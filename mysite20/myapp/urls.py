from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views

app_name = 'myapp'

urlpatterns = [
    # path(r'', views.index, name='index'),
    path(r'', views.IndexView.as_view(), name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:topic_id>/', views.TopicDetailView.as_view(), name='detail'),
    # path(r'<int:topic_id>/', views.detail, name='detail'),
    path(r'findcourses/', views.findcourses, name='findcourses'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'review/', views.review, name='review'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'myaccount/', views.myaccount, name='myaccount'),
    path(r'register/', views.register, name='register'),
    path(r'edit/', views.edit, name='edit'),
    path(r'myorders/', views.myorders, name='myorders'),
    path(r'password_change/', auth_views.PasswordChangeView.as_view(template_name='myapp/password_change_form.html', success_url='/myapp/password_change/done/'), name='password_change'),
    path(r'password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='myapp/password_change_done.html'), name='password_change_done'),
    path(r'password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', email_template_name='registration/password_reset_email.html'), name='password_reset'),
    path(r'password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='myapp/templates/registration/password_reset_done.html'), name='password_reset_done'),
    path(r'reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path(r'reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
