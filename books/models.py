from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from books.validators import validate_pdf_size
import uuid

    
class Genre(models.Model):
    name = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(max_length=255,unique=True,null=True,blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("books_by_genre", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']


    

class PublicsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(public = True)

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=255,null=True, blank=True)

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True, null=True)
    summary = models.TextField(null=True,blank=True)
    genre = models.ForeignKey(Genre,on_delete=models.PROTECT,related_name='book')
    pages = models.IntegerField(null=True, blank=True)
    cover = models.ImageField(upload_to='book/covers', null=True, blank=True)
    pdf = models.FileField(upload_to="book/pdfs", validators=[
                           validate_pdf_size, FileExtensionValidator(allowed_extensions=['pdf'])])
    posted_at = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name='book')
    users_like = models.ManyToManyField(get_user_model(),
                                        related_name='books_liked',
                                        blank=True)

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

    class Meta:
        ordering = ['-posted_at']
    
    @property
    def size(self):
        kb = 1024
        return f"{self.pdf.size/(kb*kb):.2f} mb"

class Saved(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='favorite', null=True, blank=True, unique=True)

class SavedBook(models.Model):
    saved = models.ForeignKey(Saved, on_delete=models.CASCADE, related_name='saved_book')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='saved_book')

    class Meta:
        unique_together = [['saved', 'book']]
