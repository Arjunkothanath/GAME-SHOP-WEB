from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.hashers import make_password
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404


def register(request):
    if request.method == 'POST':
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        mail=request.POST.get('email')
        password=request.POST.get('password')
        if Register.objects.filter(email=mail).exists():
            messages.error(request,f"Email already exist")
        else:
            password=make_password(password)
            Register.objects.create(first_name=fname,last_name=lname,email=mail,password=password,username=mail,usertype="user")
            messages.success(request,f"Register successfull")
            print("success")
            return redirect('login')
    return render(request,'register.html')

def signin(request):
    if request.method == 'POST':
        mail=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,username=mail,password=password)
        if user:
            login(request,user)
            request.session['ut']=user.usertype
            request.session['uid']=user.id
            request.session['uname']=user.username
            request.session['fname']=user.first_name
            messages.success(request,"login successfull")
            if user.usertype == "user":
                return redirect('home')
            else:
                return redirect('admin')
        else:
            messages.error(request,"login failed")
    return render(request,'login.html')


def home(request):
    games=game.objects.all()
    return render(request,'home.html',{'games':games})


def query(request):
    queries = UserQuery.objects.all()
    return render(request, 'queries.html', {'queries': queries})

def contact_view(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        UserQuery.objects.create(subject=subject, message=message,user_id=request.user)
        return render(request, "contact.html", {"success": True})
    return render(request, "contact.html")


def addgame(request):
    if request.method == 'POST':
        gname=request.POST.get('title')
        desc=request.POST.get('description')
        price=request.POST.get('price')
        img=request.FILES.get('image')
        if game.objects.filter(title=gname).exists():
            messages.error(request,f"game already exist")
        else:
            game.objects.create(title=gname,description=desc,price=price,image=img)
            messages.success(request,f"added successfull")
            return redirect('admin')
    return render(request,'addgame.html')


def admin(request):
    games=game.objects.all()
    return render(request,'admin.html',{'games':games})

def chatadmin(request, receiver_id=None):
    users = Register.objects.filter(usertype="user")
    receiver = None
    messages_list = []

    if receiver_id:
        receiver = Register.objects.get(id=receiver_id)
        messages_list = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=receiver)) |
            (Q(sender=receiver) & Q(receiver=request.user))
        ).order_by('created_at')
    elif users.exists():
        return redirect('chatadmin', receiver_id=users.first().id)

    if request.method == "POST" and receiver:
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(sender=request.user, receiver=receiver, chat=message_text)
            return redirect('chatadmin', receiver_id=receiver.id)

    return render(request, 'chatadmin.html', {
    'users': users,
    'receiver': receiver,
    'messages': messages_list,   # Must be present
    'user': request.user         # Needed for `message.sender == user`
})


   

def userchat(request):
    admin_user = Register.objects.filter(usertype='admin').first()
    messages_list = []

    if admin_user:
        messages_list = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=admin_user)) |
            (Q(sender=admin_user) & Q(receiver=request.user))
        ).order_by('created_at')

        if request.method == "POST":
            message_text = request.POST.get('message')
            if message_text:
                Message.objects.create(sender=request.user, receiver=admin_user, chat=message_text)
                return redirect('userchat')

    return render(request, 'userchat.html', {
        'receiver': admin_user,
        'messages': messages_list,
        'user': request.user
    })


def manage(request):
    orders=Order.objects.all()

     # Get the distinct game titles and their counts
    game_counts = Order.objects.values('game_id__title').annotate(total_orders=Count('game_id__title'),total_amount=Sum('game_id__price'))
    
    # Calculate the total sum of the prices
    total = Order.objects.aggregate(total_price=Sum('game_id__price'))['total_price'] or 0
    return render(request,'manage.html',{'orders':orders,'game_counts': game_counts, 'total': total})


def addcart(request,id):
    gm = game.objects.get(id=id)
    if gm:
        Cart.objects.create(game_id = gm,user_id=request.user)
    return redirect('cart')


def cart(request):
    games = Cart.objects.filter(user_id=request.user)
    total = 0
    for gm in games:
        total += gm.game_id.price
    return render(request,'cart.html',{'games':games,'total':total})


def checkout(request):
    carts = Cart.objects.filter(user_id=request.user)
    orders = Order.objects.filter(user_id=request.user)
    print(orders)
    if request.method == "POST":
        for cart in carts:
            Order.objects.create(game_id = cart.game_id,user_id=request.user)
            cart.delete()

    return render(request,'orders.html',{'carts':carts,'orders':orders})


def order(request):
    orders = Order.objects.filter(user_id=request.user) 
    total = 0
    for gm in orders:
        total += gm.game_id.price
    return render(request,'orders.html',{'orders':orders,'total':total})

def update(request, id):
    gm = game.objects.get(id=id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        # Debug
        print("Title:", title)
        print("Description:", description)
        print("Price:", price)
        print("Image:", image)

        if title and description and price:
            gm.title = title
            gm.description = description
            gm.price = price
            if image:
                gm.image = image
            gm.save()
            messages.success(request, "Game updated successfully!")
            return redirect('admin')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'update.html', {'game': gm})

def delgame(request, id):
    if request.method == 'POST':
        print(f"Deleting game with ID: {id}")
        gm = game.objects.get(id=id)
        gm.delete()
        messages.success(request, "Game deleted successfully!")
    return redirect('admin')


def search_suggestions(request):
    query = request.GET.get('q', '')
    games = game.objects.filter(title__icontains=query)[:5]
    results = [{'id': g.id, 'title': g.title} for g in games]
    return JsonResponse(results, safe=False)

def forgot(request):
    return render(request,'forgot.html')


def remove_from_cart(request, id):
    cart_item = Cart.objects.get(id=id)
    if cart_item.user_id == request.user:
        cart_item.delete()
    return redirect('cart')



# Create your views here.

