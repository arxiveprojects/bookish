from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.utils.text import slugify
from books.validators import validate_pdf_size
import uuid

class PublicsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(public = True)

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=255,null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    pages = models.IntegerField(null=True, blank=True)
    cover = models.ImageField(upload_to="book/covers", null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])
    pdf = models.FileField(upload_to="book/pdfs", validators=[ validate_pdf_size, FileExtensionValidator(allowed_extensions=['pdf'])])
    posted_at = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)
  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='book')
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='books_liked',blank=True)
  
    objects = models.Manager()
    publics = PublicsManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])
    @property
    def size(self):
        kb = 1024
        return f"{self.pdf.size/(kb*kb):.2f} mb"

    class Meta:
        ordering = ['-posted_at']
    
        
class Message(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    query = models.TextField()
    response = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.user.username}: {self.query[:30]}"