from django.db import models
from django.contrib.auth.models import AbstractUser
class Register(AbstractUser):
    usertype=models.CharField(max_length=10,default="admin")
    
class game(models.Model):
    image=models.ImageField(upload_to='uplods/')
    title=models.CharField(max_length=10,default=" ")
    description=models.CharField(max_length=200)
    price=models.DecimalField(default=0.0,decimal_places=2,max_digits=6)

class Cart(models.Model):
    game_id = models.ForeignKey(game,on_delete=models.CASCADE,related_name="games")
    user_id = models.ForeignKey(Register,on_delete=models.CASCADE,related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    game_id = models.ForeignKey(game,on_delete=models.CASCADE,related_name="orders")
    user_id = models.ForeignKey(Register,on_delete=models.CASCADE,related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)

class UserQuery(models.Model):
    user_id = models.ForeignKey(Register,on_delete=models.CASCADE,related_name="name")
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender  = models.ForeignKey(Register,on_delete=models.CASCADE,related_name="sent_messages")
    receiver  = models.ForeignKey(Register,on_delete=models.CASCADE,related_name="received_messages")
    chat = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
