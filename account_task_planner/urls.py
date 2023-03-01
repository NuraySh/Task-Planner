from django.urls import path
from account_task_planner.views import CustomLoginView, RegisterPage, ActivateAccount, logout_view
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('logout/', logout_view, name='logout')
    
]
