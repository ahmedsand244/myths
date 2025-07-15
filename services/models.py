from django.db import models
from django.conf import settings

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    

    
# from django.contrib.auth.models import User

class ServiceProvider(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='providers/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)


    def __str__(self):
        return self.user.username


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='services', null=True, blank=True)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='services', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            from PIL import Image
            img = Image.open(self.image.path)
            img = img.convert('RGB')
            img.thumbnail((800, 800))
            img.save(self.image.path, format='WEBP', quality=85)

    def __str__(self):
        return self.title


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='cart_items', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    @property
    def items(self):
        return self.items.all()

    
    @property
    def total_price(self):
        return sum(item.service.price * item.quantity for item in self.items.all())


    def __str__(self):
        return f"Order #{self.id} - {self.get_status_display()}"


class OrderItem(models.Model):
    # order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.service.title} × {self.quantity}"




from django.db import models

class Organizer(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='organizers/')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # ← أضف هذا
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='events/')
    organizers = models.ManyToManyField(Organizer)

    def __str__(self):
        return self.title



class EventRequest(models.Model):
    client_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_name = models.CharField(max_length=200)
    date = models.DateField()
    number_of_organizers = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_name} - {self.client_name}"



from django.db import models
from .models import Organizer  # أو import مباشر لو لازم

from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(default="test@example.com")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"رسالة من {self.name} - {self.email}"




from django.db import models

class OrganizerReview(models.Model):
    organizer = models.ForeignKey('Organizer', on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.organizer.name}"




class OrganizerWork(models.Model):
    organizer = models.ForeignKey('Organizer', on_delete=models.CASCADE, related_name='works')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='organizer_works/', null=True, blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title






class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


from django.db import models
from django.contrib.auth.models import User

class OrganizerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='organizer_profiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username









