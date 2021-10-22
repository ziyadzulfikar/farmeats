from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Cart, Comments, Expenses, Orders, Product, users
from datetime import date, timedelta

# Create your views here.
# @login_required(login_url='/login')
def home(request):
    products = Product.objects.all()
    if request.session.has_key('username'):
        cartValue = int(Cart.objects.filter(userId_id = request.session['id']).count())
        if(request.method == 'POST'):
            pdtname = request.POST['productname']
            category = request.POST['category']
            quantity = int(request.POST['quantity'])
            price = int(request.POST['price'])
            userId = request.POST['user']
            pdtId = request.POST['pdtId']
            totalprice = quantity*price
            # cartfilterUser = Cart.objects.filter(userId_id = request.session['id'])
            # cartfilterPdt = cartfilterUser.filter(pdtId_id = pdtId)
            # cartpdt = cartfilterPdt.get()
            if(Cart.objects.filter(userId_id = request.session['id'])):
                if(Cart.objects.filter(userId_id = request.session['id'], pdtId_id = pdtId)): 
                        cartpdt = Cart.objects.get(userId_id = userId, pdtId_id = pdtId)
                        # pdt = Cart.objects.get(pdtId_id = pdtId)       
                        # cartpdt = Cart.objects.all()
                        totPrice = cartpdt.totalprice + totalprice
                        totQty = cartpdt.quantity + quantity
                        cartTotal = int(Cart.objects.filter(userId_id = request.session['id']).count())
                        Cart.objects.filter(userId_id = userId, pdtId_id = pdtId).update(quantity=totQty, totalprice=totPrice)
                        # addpdt.save() 
                        return JsonResponse(
                            {'success':True, 'cartTotal':cartTotal}, 
                            safe=False
                        )
                else:
                    
                    cartTotal = int(Cart.objects.filter(userId_id = request.session['id']).count())
                    addCart = Cart.objects.create(productname=pdtname, category=category, quantity=quantity, price=price, totalprice=totalprice, userId_id=userId, pdtId_id=pdtId)
                    addCart.save()
                    return JsonResponse(
                        {'success':True, 'cartTotal':cartTotal+1},
                        safe=False
                    )
            else: 
                cartTotal = int(Cart.objects.filter(userId_id = request.session['id']).count())
                addCart = Cart.objects.create(productname=pdtname, category=category, quantity=quantity, price=price, totalprice=totalprice, userId_id=userId, pdtId_id=pdtId)
                addCart.save()
                return JsonResponse(
                    {'success':True, 'cartTotal':cartTotal+1},
                    safe=False
                )
        return render(request, 'home.html', {'cartValue':cartValue,'sessions':request.session, 'products':products}) 
    else:
        return render(request, 'home.html',{'products':products})

def signin(request):
    if request.session.has_key('username'):
        return redirect('/')
    else:
        if(request.method == 'POST'):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['id'] = user.id
                request.session['username'] = user.username
                # cartValue = int(Cart.objects.filter(userId_id = user.id).count())
                return JsonResponse(
                    {'success':True},
                    safe=False
                )
            else:
                return JsonResponse(
                    {'success':False},
                    safe=False
                )
        else:
            return render(request, 'accounts/login.html')

def register(request):
    if(request.method == 'POST'):
        name = request.POST["name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if(password1 == password2):
            if(User.objects.filter(username=name).exists()):
                messages.info(request,'Username already taken')
                print("Username already taken")
                return redirect('./register')
            elif(User.objects.filter(email=email).exists()):
                messages.info(request,'Email already taken')
                print("email already taken")
                return redirect('./register')
            else:
                user = User.objects.create_user(username=name, email=email, password=password1)
                request.session['id'] = user.id
                request.session['username'] = user.username
                # request.session['cartValue'] = int(Cart.objects.filter(userId_id = user.id).count())
                user.save()
                return redirect('/')
        else:
            print("Password not matching")
            messages.info(request,'Password not matching')
            return redirect('./register')
    else:
        return render(request, 'accounts/signup.html')

# @login_required(login_url='/')
def signout(request):
   try:
      del request.session['id']
      logout(request)
   except:
      print(request.session['id'])
      print("error")
   return redirect('/')

def adminSignout(request):
   try:
      del request.session['id']
      logout(request)
   except:
      print(request.session['id'])
      print("error")
   return redirect('adminHome')

def adminLogin(request):
    if request.session.has_key('superuser')==True:
        return redirect('adminHome')
    else:
        if(request.method == 'POST'):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password, is_superuser = True)
            if user is not None:
                if( user.is_superuser == True ):
                    request.session['id'] = user.id
                    request.session['username'] = user.username
                    request.session['superuser'] = user.is_superuser
                    return JsonResponse(
                        {'success':True},
                        safe=False
                    )
                else:
                    messages.info(request,'Username or password is incorrect')
                    return JsonResponse(
                        {'success':False},
                        safe=False
                    )
            else:
                messages.info(request,'Username or password is incorrect')
                return JsonResponse(
                    {'success':False},
                    safe=False
                )
        else:
            return render(request, 'admin/signin.html')

def adminHome(request):
    if request.session.has_key('superuser')==True:
        allUsers = User.objects.all()
        allProducts = Product.objects.all()
        allOrders = Orders.objects.all()
        allComments = Comments.objects.all()
        Burger = 0
        Shawarma = 0
        Pizza = 0
        FriedChicken = 0
        Juice = 0
        allExpenses = Expenses.objects.filter(CurrentDate = date.today())
        allOrdersIncome = Orders.objects.filter(delivery = "Delivered", date = date.today())
        allBurgerIncome = Orders.objects.filter(delivery = "Delivered", date = date.today(), category = "Burger")
        allShawarmaIncome = Orders.objects.filter(delivery = "Delivered", date = date.today(), category = "Shawarma")
        allPizzaIncome = Orders.objects.filter(delivery = "Delivered", date = date.today(), category = "Pizza")
        allFriedChickenIncome = Orders.objects.filter(delivery = "Delivered", date = date.today(), category = "FriedChicken")
        allJuicesIncome = Orders.objects.filter(delivery = "Delivered", date = date.today(), category = "Juices")
        for Burgers in allBurgerIncome:
            Burger = Burger + Burgers.price
        for Shawarmas in allShawarmaIncome:
            Shawarma = Shawarma + Shawarmas.price
        for Pizzas in allPizzaIncome:
            Pizza = Pizza + Pizzas.price
        for FriedChickens in allFriedChickenIncome:
            FriedChicken = FriedChicken + FriedChickens.price
        for Juices in allJuicesIncome:
            Juice = Juice + Juices.price
        TodayGrossExpense = Expenses.objects.filter(CurrentDate = date.today())
        TodayTotalIncome = Orders.objects.filter(date = date.today(), delivery = "Delivered")
        totalIncomeToday = 0
        totalIncomeQuantity = 0
        TotalGross = 0
        Rent = 0
        Electricity = 0
        TotalSalary = 0
        OtherExpense = 0
        TotalExpense = 0
        for totalIncome in allOrdersIncome:
            totalIncomeToday = totalIncomeToday + totalIncome.price
            totalIncomeQuantity = totalIncomeQuantity + totalIncome.quantity
        for TodayExpense in TodayGrossExpense:
            TotalGross = TotalGross+TodayExpense.FoodItems
            Rent = Rent + TodayExpense.Rent 
            Electricity = Electricity + TodayExpense.Electricity
            TotalSalary = TotalSalary + TodayExpense.TotalSalary
            OtherExpense = OtherExpense + TodayExpense.OtherExpense
            TotalExpense = TotalExpense + TodayExpense.TotalExpense
        TotalGrossProfit = totalIncomeToday - TotalGross
        TotalNetProfit = totalIncomeToday - (TotalGross+Rent+Electricity+TotalSalary+OtherExpense)
        if (User.objects.filter(is_superuser = True).exists()):
            return render(request, 'admin/admin-home.html', {'session':request.session,'Juice':Juice,'FriedChicken':FriedChicken,'Pizza':Pizza,'Shawarma':Shawarma,'Burger':Burger,'TotalNetProfit':TotalNetProfit,'TotalGrossProfit':TotalGrossProfit,'totalIncomeQuantity':totalIncomeQuantity,'TodayTotalIncome':TodayTotalIncome ,'TotalExpense':TotalExpense ,'OtherExpense':OtherExpense ,'TotalSalary':TotalSalary ,'Electricity':Electricity ,'Rent':Rent ,'TotalGross':TotalGross ,'allUsers':allUsers,'allProducts':allProducts,'allOrders':allOrders, 'allComments':allComments,'allExpenses':allExpenses, 'totalIncomeToday':totalIncomeToday})
        else:
            return redirect('/adminSignin')
    else:
        return redirect('/adminSignin')

def yesterdayIncome(request):
    if request.session.has_key('superuser')==True:
        Burger = 0
        Shawarma = 0
        Pizza = 0
        FriedChicken = 0
        Juice = 0
        yesterday = date.today() - timedelta(days = 1)
        allExpenses = Expenses.objects.filter(CurrentDate = yesterday)
        allOrdersIncome = Orders.objects.filter(delivery = "Delivered", date = yesterday)
        allBurgerIncome = Orders.objects.filter(delivery = "Delivered", date = yesterday, category = "Burger")
        allShawarmaIncome = Orders.objects.filter(delivery = "Delivered", date = yesterday, category = "Shawarma")
        allPizzaIncome = Orders.objects.filter(delivery = "Delivered", date = yesterday, category = "Pizza")
        allFriedChickenIncome = Orders.objects.filter(delivery = "Delivered", date = yesterday, category = "FriedChicken")
        allJuicesIncome = Orders.objects.filter(delivery = "Delivered", date = yesterday, category = "Juices")
        for Burgers in allBurgerIncome:
            Burger = Burger + Burgers.price
        for Shawarmas in allShawarmaIncome:
            Shawarma = Shawarma + Shawarmas.price
        for Pizzas in allPizzaIncome:
            Pizza = Pizza + Pizzas.price
        for FriedChickens in allFriedChickenIncome:
            FriedChicken = FriedChicken + FriedChickens.price
        for Juices in allJuicesIncome:
            Juice = Juice + Juices.price
        TodayGrossExpense = Expenses.objects.filter(CurrentDate = yesterday)
        TodayTotalIncome = Orders.objects.filter(date = yesterday, delivery = "Delivered")
        totalIncomeToday = 0
        totalIncomeQuantity = 0
        TotalGross = 0
        Rent = 0
        Electricity = 0
        TotalSalary = 0
        OtherExpense = 0
        TotalExpense = 0
        for totalIncome in allOrdersIncome:
            totalIncomeToday = totalIncomeToday + totalIncome.price
            totalIncomeQuantity = totalIncomeQuantity + totalIncome.quantity
        for TodayExpense in TodayGrossExpense:
            TotalGross = TotalGross+TodayExpense.FoodItems
            Rent = Rent + TodayExpense.Rent 
            Electricity = Electricity + TodayExpense.Electricity
            TotalSalary = TotalSalary + TodayExpense.TotalSalary
            OtherExpense = OtherExpense + TodayExpense.OtherExpense
            TotalExpense = TotalExpense + TodayExpense.TotalExpense
        TotalGrossProfit = totalIncomeToday - TotalGross
        TotalNetProfit = totalIncomeToday - (TotalGross+Rent+Electricity+TotalSalary+OtherExpense)
        allExpenses = Expenses.objects.filter(CurrentDate = yesterday)
        return render(request, 'admin/yesterdayIncome.html', {'Juice':Juice,'FriedChicken':FriedChicken,'Pizza':Pizza,'Shawarma':Shawarma,'Burger':Burger,'TotalNetProfit':TotalNetProfit,'TotalGrossProfit':TotalGrossProfit,'totalIncomeQuantity':totalIncomeQuantity,'TodayTotalIncome':TodayTotalIncome ,'TotalExpense':TotalExpense ,'OtherExpense':OtherExpense ,'TotalSalary':TotalSalary ,'Electricity':Electricity ,'Rent':Rent ,'TotalGross':TotalGross ,'allExpenses':allExpenses, 'totalIncomeToday':totalIncomeToday})

    else:
        return redirect('/adminSignin')

def totalIncome(request):
    if request.session.has_key('superuser')==True:
        Burger = 0
        Shawarma = 0
        Pizza = 0
        FriedChicken = 0
        Juice = 0
        allExpenses = Expenses.objects.filter()
        allOrdersIncome = Orders.objects.filter(delivery = "Delivered")
        allBurgerIncome = Orders.objects.filter(delivery = "Delivered", category = "Burger")
        allShawarmaIncome = Orders.objects.filter(delivery = "Delivered", category = "Shawarma")
        allPizzaIncome = Orders.objects.filter(delivery = "Delivered", category = "Pizza")
        allFriedChickenIncome = Orders.objects.filter(delivery = "Delivered", category = "FriedChicken")
        allJuicesIncome = Orders.objects.filter(delivery = "Delivered", category = "Juices")
        for Burgers in allBurgerIncome:
            Burger = Burger + Burgers.price
        for Shawarmas in allShawarmaIncome:
            Shawarma = Shawarma + Shawarmas.price
        for Pizzas in allPizzaIncome:
            Pizza = Pizza + Pizzas.price
        for FriedChickens in allFriedChickenIncome:
            FriedChicken = FriedChicken + FriedChickens.price
        for Juices in allJuicesIncome:
            Juice = Juice + Juices.price
        TodayGrossExpense = Expenses.objects.filter()
        TodayTotalIncome = Orders.objects.filter(delivery = "Delivered")
        totalIncomeToday = 0
        totalIncomeQuantity = 0
        TotalGross = 0
        Rent = 0
        Electricity = 0
        TotalSalary = 0
        OtherExpense = 0
        TotalExpense = 0
        for totalIncome in allOrdersIncome:
            totalIncomeToday = totalIncomeToday + totalIncome.price
            totalIncomeQuantity = totalIncomeQuantity + totalIncome.quantity
        for TodayExpense in TodayGrossExpense:
            TotalGross = TotalGross+TodayExpense.FoodItems
            Rent = Rent + TodayExpense.Rent 
            Electricity = Electricity + TodayExpense.Electricity
            TotalSalary = TotalSalary + TodayExpense.TotalSalary
            OtherExpense = OtherExpense + TodayExpense.OtherExpense
            TotalExpense = TotalExpense + TodayExpense.TotalExpense
        TotalGrossProfit = totalIncomeToday - TotalGross
        TotalNetProfit = totalIncomeToday - (TotalGross+Rent+Electricity+TotalSalary+OtherExpense)
        allExpenses = Expenses.objects.filter()
        return render(request, 'admin/totalIncome.html', {'Juice':Juice,'FriedChicken':FriedChicken,'Pizza':Pizza,'Shawarma':Shawarma,'Burger':Burger,'TotalNetProfit':TotalNetProfit,'TotalGrossProfit':TotalGrossProfit,'totalIncomeQuantity':totalIncomeQuantity,'TodayTotalIncome':TodayTotalIncome ,'TotalExpense':TotalExpense ,'OtherExpense':OtherExpense ,'TotalSalary':TotalSalary ,'Electricity':Electricity ,'Rent':Rent ,'TotalGross':TotalGross ,'allExpenses':allExpenses, 'totalIncomeToday':totalIncomeToday})

    else:
        return redirect('/adminSignin')


def specificDayIncome(request):
    if request.session.has_key('superuser')==True:
        specificDate = request.POST['day']
        Burger = 0
        Shawarma = 0
        Pizza = 0
        FriedChicken = 0
        Juice = 0
        # yesterday = date.today() - timedelta(days = 1)
        allExpenses = Expenses.objects.filter(CurrentDate = specificDate)
        allOrdersIncome = Orders.objects.filter(delivery = "Delivered", date = specificDate)
        allBurgerIncome = Orders.objects.filter(delivery = "Delivered", date = specificDate, category = "Burger")
        allShawarmaIncome = Orders.objects.filter(delivery = "Delivered", date = specificDate, category = "Shawarma")
        allPizzaIncome = Orders.objects.filter(delivery = "Delivered", date = specificDate, category = "Pizza")
        allFriedChickenIncome = Orders.objects.filter(delivery = "Delivered", date = specificDate, category = "FriedChicken")
        allJuicesIncome = Orders.objects.filter(delivery = "Delivered", date = specificDate, category = "Juices")
        for Burgers in allBurgerIncome:
            Burger = Burger + Burgers.price
        for Shawarmas in allShawarmaIncome:
            Shawarma = Shawarma + Shawarmas.price
        for Pizzas in allPizzaIncome:
            Pizza = Pizza + Pizzas.price
        for FriedChickens in allFriedChickenIncome:
            FriedChicken = FriedChicken + FriedChickens.price
        for Juices in allJuicesIncome:
            Juice = Juice + Juices.price
        TodayGrossExpense = Expenses.objects.filter(CurrentDate = specificDate)
        TodayTotalIncome = Orders.objects.filter(date = specificDate, delivery = "Delivered")
        totalIncomeToday = 0
        totalIncomeQuantity = 0
        TotalGross = 0
        Rent = 0
        Electricity = 0
        TotalSalary = 0
        OtherExpense = 0
        TotalExpense = 0
        for totalIncome in allOrdersIncome:
            totalIncomeToday = totalIncomeToday + totalIncome.price
            totalIncomeQuantity = totalIncomeQuantity + totalIncome.quantity
        for TodayExpense in TodayGrossExpense:
            TotalGross = TotalGross+TodayExpense.FoodItems
            Rent = Rent + TodayExpense.Rent 
            Electricity = Electricity + TodayExpense.Electricity
            TotalSalary = TotalSalary + TodayExpense.TotalSalary
            OtherExpense = OtherExpense + TodayExpense.OtherExpense
            TotalExpense = TotalExpense + TodayExpense.TotalExpense
        TotalGrossProfit = totalIncomeToday - TotalGross
        TotalNetProfit = totalIncomeToday - (TotalGross+Rent+Electricity+TotalSalary+OtherExpense)
        allExpenses = Expenses.objects.filter(CurrentDate = specificDate)
        return render(request, 'admin/specificDayIncome.html', {'specificDate':specificDate,'Juice':Juice,'FriedChicken':FriedChicken,'Pizza':Pizza,'Shawarma':Shawarma,'Burger':Burger,'TotalNetProfit':TotalNetProfit,'TotalGrossProfit':TotalGrossProfit,'totalIncomeQuantity':totalIncomeQuantity,'TodayTotalIncome':TodayTotalIncome ,'TotalExpense':TotalExpense ,'OtherExpense':OtherExpense ,'TotalSalary':TotalSalary ,'Electricity':Electricity ,'Rent':Rent ,'TotalGross':TotalGross ,'allExpenses':allExpenses, 'totalIncomeToday':totalIncomeToday})

    else:
        return redirect('/adminSignin')

def dayToDayIncome(request):
    if request.session.has_key('superuser')==True:
        dayFrom = request.POST['dayFrom']
        dayTo = request.POST['dayTo']
        Burger = 0
        Shawarma = 0
        Pizza = 0
        FriedChicken = 0
        Juice = 0
        # yesterday = date.today() - timedelta(days = 1)
        allExpenses = Expenses.objects.filter(CurrentDate__gte=dayFrom,CurrentDate__lte=dayTo)
        allOrdersIncome = Orders.objects.filter(delivery = "Delivered", date__gte=dayFrom,date__lte=dayTo)
        allBurgerIncome = Orders.objects.filter(delivery = "Delivered", date__gte=dayFrom,date__lte=dayTo, category = "Burger")
        allShawarmaIncome = Orders.objects.filter(delivery = "Delivered", date__gte=dayFrom,date__lte=dayTo, category = "Shawarma")
        allPizzaIncome = Orders.objects.filter(delivery = "Delivered", date__gte=dayFrom,date__lte=dayTo, category = "Pizza")
        allFriedChickenIncome = Orders.objects.filter(delivery = "Delivered", date__gte=dayFrom,date__lte=dayTo, category = "FriedChicken")
        allJuicesIncome = Orders.objects.filter(delivery = "Delivered", date__gte=dayFrom,date__lte=dayTo, category = "Juices")
        for Burgers in allBurgerIncome:
            Burger = Burger + Burgers.price
        for Shawarmas in allShawarmaIncome:
            Shawarma = Shawarma + Shawarmas.price
        for Pizzas in allPizzaIncome:
            Pizza = Pizza + Pizzas.price
        for FriedChickens in allFriedChickenIncome:
            FriedChicken = FriedChicken + FriedChickens.price
        for Juices in allJuicesIncome:
            Juice = Juice + Juices.price
        TodayGrossExpense = Expenses.objects.filter(CurrentDate__gte=dayFrom,CurrentDate__lte=dayTo)
        TodayTotalIncome = Orders.objects.filter(date__gte=dayFrom,date__lte=dayTo, delivery = "Delivered")
        totalIncomeToday = 0
        totalIncomeQuantity = 0
        TotalGross = 0
        Rent = 0
        Electricity = 0
        TotalSalary = 0
        OtherExpense = 0
        TotalExpense = 0
        for totalIncome in allOrdersIncome:
            totalIncomeToday = totalIncomeToday + totalIncome.price
            totalIncomeQuantity = totalIncomeQuantity + totalIncome.quantity
        for TodayExpense in TodayGrossExpense:
            TotalGross = TotalGross+TodayExpense.FoodItems
            Rent = Rent + TodayExpense.Rent 
            Electricity = Electricity + TodayExpense.Electricity
            TotalSalary = TotalSalary + TodayExpense.TotalSalary
            OtherExpense = OtherExpense + TodayExpense.OtherExpense
            TotalExpense = TotalExpense + TodayExpense.TotalExpense
        TotalGrossProfit = totalIncomeToday - TotalGross
        TotalNetProfit = totalIncomeToday - (TotalGross+Rent+Electricity+TotalSalary+OtherExpense)
        allExpenses = Expenses.objects.filter(CurrentDate__gte=dayFrom,CurrentDate__lte=dayTo)
        return render(request, 'admin/dayToDayIncome.html', {'dayFrom':dayFrom, 'dayTo':dayTo ,'Juice':Juice,'FriedChicken':FriedChicken,'Pizza':Pizza,'Shawarma':Shawarma,'Burger':Burger,'TotalNetProfit':TotalNetProfit,'TotalGrossProfit':TotalGrossProfit,'totalIncomeQuantity':totalIncomeQuantity,'TodayTotalIncome':TodayTotalIncome ,'TotalExpense':TotalExpense ,'OtherExpense':OtherExpense ,'TotalSalary':TotalSalary ,'Electricity':Electricity ,'Rent':Rent ,'TotalGross':TotalGross ,'allExpenses':allExpenses, 'totalIncomeToday':totalIncomeToday})

    else:
        return redirect('/adminSignin')


def delivery(request):
    if(request.method == 'POST'):
        deliveryStatus = request.POST['deliveryStatus'] 
        orderId = request.POST['orderId'] 
        Orders.objects.filter(id = orderId).update(delivery = deliveryStatus)
        return JsonResponse(
            {'success':True,},
                safe=False
        )

def expenses(request):
    if(request.method == 'POST'):
        FoodItems = int(request.POST['FoodItems']) 
        Rent = int(request.POST['Rent']) 
        Electricity = int(request.POST['Electricity']) 
        TotalSalary = int(request.POST['TotalSalary'] )
        OtherExpense = int(request.POST['OtherExpense'] )
        TotalExpense = FoodItems+Rent+Electricity+TotalSalary+OtherExpense
        CurrentDate = date.today()
        expense = Expenses.objects.create(FoodItems=FoodItems, Rent=Rent, Electricity=Electricity, TotalSalary=TotalSalary, OtherExpense=OtherExpense, TotalExpense=TotalExpense, CurrentDate=CurrentDate)
        expense.save()  
        return redirect('adminHome')

def dltPdt(request):
    if(request.method == 'POST'):
        pdtId = request.POST['pdtId'] 
        if(Product.objects.filter(id = pdtId).exists()):
            dlteThisUsers = Product.objects.filter(id = pdtId)  
            dlteThisUsers.delete()
    return redirect('adminHome') 


def dlteUser(request):
    if(request.method == 'POST'):
        userId = request.POST['userId'] 
        if(User.objects.filter(id = userId).exists()):
            dlteThisUsers = User.objects.filter(id = userId)  
            dlteThisUsers.delete()
    return redirect('adminHome') 

def dlteOrder(request):
    if(request.method == 'POST'):
        orderId = request.POST['orderId'] 
        if(Orders.objects.filter(id = orderId).exists()):
            dlteOrder = Orders.objects.filter(id = orderId)  
            dlteOrder.delete()
    return redirect('adminHome') 

def dlteComment(request):
    if(request.method == 'POST'):
        commentId = request.POST['commentId'] 
        if(Comments.objects.filter(id = commentId).exists()):
            dlteComments = Comments.objects.filter(id = commentId)  
            dlteComments.delete()
    return redirect('adminHome') 

def dlteExpense(request):
    if(request.method == 'POST'):
        expenseId = request.POST['expenseId'] 
        if(Expenses.objects.filter(id = expenseId).exists()):
            dlteComments = Expenses.objects.filter(id = expenseId)  
            dlteComments.delete()
    return redirect('adminHome') 

def addProduct(request):
    if(request.method == 'POST'):
        pdtname = request.POST['pdtname']
        category = request.POST['category']
        price = request.POST['price']
        desc = request.POST['desc']
        image = request.FILES['image']
        product = Product.objects.create(productname=pdtname, category=category, price=price, description=desc, image=image)
        product.save()
        return redirect('adminHome') 

def addIncome(request):
    if(request.method == 'POST'):
        ProductName = request.POST['ProductName']
        Quantity = request.POST['Quantity']
        price = request.POST['Price']
        category = request.POST['category']
        CurrentDate = request.POST['CurrentDate']
        user = request.POST['user']
        delivery = request.POST['delivery']
        orders = Orders.objects.create(name="admin",products=ProductName, quantity=Quantity, price=price, category=category, delivery=delivery, date=CurrentDate, userId_id=user)
        orders.save()
        return redirect('adminHome') 
 
def buy(request):
    if(request.method == 'POST'):
        cartValue = int(Cart.objects.filter(userId_id = request.session['id']).count())
        pdtname = request.POST['ProductName']
        category = request.POST['Category']
        quantity = int(request.POST['Quantity'])
        price = int(request.POST['Price'])
        userId = request.POST['User']
        totalprice = quantity*price

    return render(request, 'checkout.html',{'cartValue':cartValue,'sessions':request.session,'pdtname':pdtname, 'category':category, 'quantity':quantity, 'price':price, 'session':request.session, 'totalprice':totalprice})

@login_required(login_url='/login')        
def cart(request):
    totalPrice = 0
    cartValue = int(Cart.objects.filter(userId_id = request.session['id']).count())
    if(Cart.objects.filter(userId_id = request.session['id'])):
        allCart = Cart.objects.filter(userId_id = request.session['id'])
        if(request.method == 'POST'):
            if 'dlte' in request.POST:
            # dtle = request.POST['dtl']
            # if(dtle == '1'):
                deletePdtCart = request.POST['dlte']
                delte = Cart.objects.get(id=deletePdtCart)
                delte.delete()
                cartTotal = int(Cart.objects.filter(userId_id = request.session['id']).count())
                return JsonResponse(
                        {'success':True, 'cartTotal':cartTotal},
                        safe=False
                    )
            else:
                price = int(request.POST['price'])
                quantity = int(request.POST['quantity'])
                cartId = request.POST['cartId']
                Cart.objects.filter(id = cartId).update(quantity=quantity, totalprice=price*quantity)
                return JsonResponse(
                        {'success':True},
                        safe=False
                    )
        else:
            for cart in allCart:
                totalPrice = totalPrice + cart.totalprice
            return render(request, 'cart.html',{'cartValue':cartValue,'sessions':request.session,'allcart':allCart, 'totalPrice':totalPrice})
    else:
        messages.info(request,'Nothing to display in cart')
        return redirect('/')

@login_required(login_url='/login') 
def successfulOrder(request):
    cartValue = int(Cart.objects.filter(userId_id = request.session['id']).count())
    if(request.method == 'POST'):
        if(Cart.objects.filter(userId_id = request.session['id'])):
            name = request.POST['fullName']
            phone = request.POST['phoneNumber']
            address = request.POST['address']
            address2 = request.POST['address2']
            district = request.POST['district']
            zip = request.POST['zip']
            paymentMethod = request.POST['paymentMethod']
            userId = request.session['id']
            delivery = request.POST['delivery']
            totalPrice=0
            cartItems = Cart.objects.filter(userId_id = request.session['id'])
            for cartpdt in cartItems:
                totalPrice = totalPrice+cartpdt.totalprice
            for cartpdt in cartItems:
                products = cartpdt.productname
                quantity = cartpdt.quantity
                price = cartpdt.totalprice
                category = cartpdt.category
                dat = date.today()
                if(paymentMethod == 'COD'):
                    order = Orders.objects.create(name=name, phone=phone, address=address, address2=address2, district=district, zip=zip, paymentMethod=paymentMethod, products=products, quantity=quantity, price=price, category=category, userId_id=userId, delivery=delivery, date=dat)
                    order.save()
                else:
                    return render(request, 'paypal.html',{'cartValue':cartValue,'sessions':request.session,'name':name, 'phone':phone, 'address':address, 'address2':address2, 'district':district, 'zip':zip, 'paymentMethod':paymentMethod, 'products':products, 'quantity':quantity, 'price':price, 'category':category, 'userId_id':userId, 'delivery':delivery, 'date':dat, 'totalPrice':totalPrice})
            messages.info(request,'Your order is placed')
            return redirect('/')
        # (name,phone,address,address2,district,zip,paymentMethod,products,quantity,price,category,userId,delivery,date)

@login_required(login_url='/login') 
def thankyou(request):
    if(request.method == 'POST'):
        if(Cart.objects.filter(userId_id = request.session['id'])):
            cartItems = Cart.objects.all()
            for cartpdt in cartItems:
                name = request.POST['name']
                phone = request.POST['phone']
                address = request.POST['address']
                address2 = request.POST['address2']
                district = request.POST['district']
                zip = request.POST['zip']
                paymentMethod = request.POST['paymentMethod']
                products = cartpdt.productname
                quantity = cartpdt.quantity
                price = cartpdt.totalprice
                category = cartpdt.category
                userId = request.session['id']
                delivery = request.POST['delivery']
                dat = date.today()
                order = Orders.objects.create(name=name, phone=phone, address=address, address2=address2, district=district, zip=zip, paymentMethod=paymentMethod, products=products, quantity=quantity, price=price, category=category, userId_id=userId, delivery=delivery, date=dat)
                order.save()
                messages.info(request,'Your order is placed')
        return JsonResponse(
            {'success':True},
                safe=False
        )

@login_required(login_url='/login')  
def myOrders(request):
    cartValue = int(Cart.objects.filter(userId_id = request.session['id']).count())
    if(Orders.objects.filter(userId_id = request.session['id'])):
        orders = Orders.objects.all()
        return render(request, 'myOrder.html',{'cartValue':cartValue,'sessions':request.session,'AllOrders':orders,'session':request.session})
    else:
        messages.info(request,'Nothing to display in orders')
        return redirect('/')

@login_required(login_url='/login')
def comments(request):
    if(request.method == 'POST'):
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        comment = request.POST['comment']
        user = request.POST['user']
        userId = request.session['id']
        comments = Comments.objects.create(name=name, email=email, phone=phone, comment=comment, user=user, userId_id=userId)
        comments.save()
        return redirect('/')
    else:
        messages.info(request,'Sorry Some error occured')
        return redirect('/')