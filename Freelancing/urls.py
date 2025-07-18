"""
URL configuration for Freelancing project.

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
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('contact/',views.contact),
    path('User_reg/',views.User_reg),
    path('client_reg/',views.client_reg),
    path('userhome/',views.userhome),
    path('clienthome/',views.clienthome),
    path('admhome/',views.admhome),
    path('admviewusers/',views.admviewusers),
    path('change/',views.change),
    path('login/',views.logins),
    path('admviewclient/',views.admviewclient),
    path('approve_client/',views.approve_client),
    path('reject_client/',views.reject_client),
    path('add_job/',views.add_job),
    path('client_job_view/',views.client_job_view),
    path('delete_job/',views.delete_job),
    path('search_jobs/',views.search_jobs),
    path('view_jobs/',views.view_jobs),
    path('apply_job/',views.apply_job),
    path('job_applied/',views.job_applied),
    path('userview_job_applied/',views.userview_job_applied),
    path('view_applications/',views.client_view_applications),
    path('approve_ap/',views.approve_ap),
    path('reject_ap/',views.reject_ap),
    path('add_work/',views.add_work),
    path('client_view_staffs/',views.client_view_staffs),
    path('clientchat/',views.clientchat),
    path('userchat/',views.userchat),
    path('freelacer_view_work/',views.freelacer_view_work),
    path('total_works/',views.total_works),
    path('search_users/',views.search_users),
    # path('search_chats/',views.search_chats),
    path('payment_page/',views.payment_page),
    path('amount_page/',views.amount_page),
    path('add_feed/',views.add_feed),
    path('user_payment_details/',views.user_payment_details),
    path('user_profile/',views.user_profile),
    path('update_profile/',views.update_profile),
    path('delete_ap/',views.delete_ap),
    path('udp/',views.udp),
    path('add_guidence/',views.add_guidence),
    path('user_view_guide/',views.user_view_guide),
    path('company_profile/',views.company_profile),
    path('company_update_profile/',views.company_update_profile),
    path('userfeedbacks/',views.userfeedbacks),
    path('useraddfeedback/',views.useraddfeedback),
    path('delete_feedback/',views.delete_feedback),
    path('view_feedbacks/',views.view_feedbacks),
    path('newimages/',views.newimages),
    path('delete_post/',views.delete_post),
    path('requestuser/',views.requestuser),
    path('togglerequestuser/',views.togglerequestuser),
    path('requestscompany/',views.requestscompany),
    path('adminhelp/',views.adminhelp),
    path('adminpayment/',views.adminpayment),
    path('upayment/',views.upayment),

]
