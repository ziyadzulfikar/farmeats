from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login', views.signin, name = 'signin'),
    path('register', views.register, name= 'register'),
    path('logout', views.signout, name = 'signout'),
    path('adminSignin', views.adminLogin, name = 'adminLogin'),
    path('adminHome', views.adminHome, name = 'adminHome'),
    path('dlteUser', views.dlteUser, name = 'dlteUser'),
    path('dlteOrder', views.dlteOrder, name = 'dlteOrder'),
    path('dlteComment', views.dlteComment, name = 'dlteComment'),
    path('dlteExpense', views.dlteExpense, name = 'dlteExpense'),
    path('addProduct', views.addProduct, name = 'addProduct'),
    path('addIncome', views.addIncome, name = 'addIncome'),
    path('yesterdayIncome', views.yesterdayIncome, name = 'yesterdayIncome'),
    path('totalIncome', views.totalIncome, name = 'totalIncome'),
    path('specificDayIncome', views.specificDayIncome, name = 'specificDayIncome'),
    path('dayToDayIncome', views.dayToDayIncome, name = 'dayToDayIncome'),
    path('expenses', views.expenses, name = 'expenses'),
    path('buy', views.buy, name = 'buy'),
    path('cart', views.cart, name = 'cart'),
    path('successfulOrder', views.successfulOrder, name = 'successfulOrder'),
    path('thankyou', views.thankyou, name = 'thankyou'),
    path('myOrders', views.myOrders, name = 'myOrders'),
    path('comments', views.comments, name = 'comments'),
    path('delivery', views.delivery, name = 'delivery'),
]