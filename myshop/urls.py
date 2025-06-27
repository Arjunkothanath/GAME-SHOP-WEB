from django.urls import path
from . import views
urlpatterns=[
    path('',views.signin,name='login'),
    path('login/',views.signin,name='login'),
    path('register',views.register,name='register'),
    path('forgot',views.forgot,name='forgot'),
    path('cart',views.cart,name='cart'),
    path('add_to_cart/<int:id>/',views.addcart,name='add_to_cart'),
    path('orders',views.order,name='orders'),
    path('home',views.home,name='home'),
    path('admin',views.admin,name='admin'),
    path('addgame',views.addgame,name='addgame'),
    path('checkout',views.checkout,name='checkout'),
    path('manage',views.manage,name='manage'),
    path('queries',views.query,name='queries'),
    path('contact/', views.contact_view, name='contact'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:id>/',views.update,name='update'),
    path('delete_game/<int:id>/',views.delgame,name='delete_game'),
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),
    path('chatadmin/', views.chatadmin, name='chatadmin_no_id'),
    path('chatadmin/<int:receiver_id>/', views.chatadmin, name='chatadmin'),
    path('userchat/', views.userchat, name='userchat'),

]