from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.utils.text import slugify
from books.validators import validate_pdf_size
import uuid
import fitz
import base64



    

class PublicsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(public = True)

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=255,null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    pages = models.IntegerField(null=True, blank=True)
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

    class Meta:
        ordering = ['-posted_at']
    
    @property
    def size(self):
        kb = 1024
        return f"{self.pdf.size/(kb*kb):.2f} mb"
    

    def get_images(self,offset=0):

        images = []
        with fitz.Document(filename=self.pdf.path, filetype='pdf') as pdf:
            for i in range(offset, offset + 4):
                if i >= self.pages: break
                image = pdf.get_page_pixmap(i)
                stream = image.tobytes(output="png")
                # Convert image data to a base64-encoded string
                image_data_base64 = base64.b64encode(stream).decode("utf-8")
                images.append(image_data_base64)
        return images
        
        
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    book = models.ForeignKey(Book, on_delete=models.CASCADE) 
