from django.conf.urls import url
from django.urls import path
from . import views
from .views import GeneratePdf

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login', views.signin, name = 'signin'),
    path('register', views.register, name= 'register'), 
    path('logout', views.signout, name = 'signout'),
    path('adminlogout', views.adminSignout, name = 'adminSignout'),
    path('adminSignin', views.adminLogin, name = 'adminLogin'),
    path('adminHome', views.adminHome, name = 'adminHome'),
    path('dltPdt', views.dltPdt, name = 'dltPdt'),
    path('dlteUser', views.dlteUser, name = 'dlteUser'),
    path('dlteOrder', views.dlteOrder, name = 'dlteOrder'),
    path('dlteOrderUser', views.dlteOrderUser, name = 'dlteOrderUser'),
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
    url(r'^printInvoice/$',GeneratePdf.as_view())  
    # path('pdf', views.GeneratePdf, name = 'GeneratePdf'),
    # path('printInvoice', views.printInvoice, name = 'printInvoice'),
]