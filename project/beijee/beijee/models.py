from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save ,pre_save
from django.dispatch import receiver



class CustomUser(models.Model):
    
    user = models.OneToOneField(User , on_delete=models.CASCADE) 

    Subscription = models.ForeignKey('Subscription', on_delete=models.SET_NULL, null=True, blank=True)
    
    

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address_line = models.CharField(max_length=255)
    

    def __str__(self):
        return f"{self.address_line}" 
    
class Subscription(models.Model):

    CHOICES = (
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
        ('Ultimate' ,'Ultimate'),

    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type =  models.CharField(max_length=255, choices=CHOICES, default='Basic')
    expiration_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ({self.start_date} - {self.end_date})"

    
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription} - {self.payment_date}"
    
@receiver(post_save, sender=CustomUser)  
def create_subscription(sender, instance, *args, **kwargs):
    if instance:
        print(instance)
        #create Subscription for user

        #Subscription.objects.create(user=instance, expiration_date=datetime.now()+datetime.timedelta(days=60))

@receiver(post_save, sender=Subscription)
def update_subscription(sender, instance, *args, **kwargs):
    if instance.expiration_date < datetime.now():
        Subscription.objects.get(id=instance.id).delete()
    else:
        instance.active = True
        
    