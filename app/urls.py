from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index-page"),
    path('ticket', views.TicketMS, name="signup-page"),
    path('status', views.status, name="signup-page"),
    path('get_ticket_details/<str:tid>/', views.get_ticket_details, name='get_ticket_details'),
    path('loginuser', views.loginuser, name="signup-page"),
    path('loginhandler', views.loginhandler, name="signup-page"),
    path('loginadmin', views.loginadmin, name="signup-page"),
    path('loginsuperadmin', views.loginsuperadmin, name="signup-page"),



    path('handler', views.handler, name="handler_page"),
    path('superadmin', views.superadmin, name="handler_page"),
    path('usertable', views.usertable, name="handler_page"),

    path('download', views.download, name="handler_page"),

    path('logout', views.logout_view, name="login-page"),
    path('admin', views.admin, name="handler_page"),

    path('signup', views.signuppageuser, name="signup-page"),
    path('signin', views.loginpageuser, name="login-page"),

    path('user', views.user, name="user-page"),

]