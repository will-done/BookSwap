
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="books")
    description = RichTextField()
    is_active = models.BooleanField(default=False)
    is_home = models.BooleanField(default=False)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True, editable=False)
    categories = models.ManyToManyField(Category, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # 🔥 EKLENDİ

    def save(self, *args, **kwargs):
        if not self.slug:  # Yalnızca slug boşsa oluştur
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Book.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class TradeOffer(models.Model):
    sender = models.ForeignKey(User, related_name='sent_offers', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_offers', on_delete=models.CASCADE)
    sender_book = models.ForeignKey(Book, related_name='sent_books', on_delete=models.CASCADE)
    receiver_book = models.ForeignKey(Book, related_name='received_books', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted')], default='pending')
    approved_by_admin = models.BooleanField(default=False)  # Yeni eklenen alan
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'TradeOffer from {self.sender.username} to {self.receiver.username}'
