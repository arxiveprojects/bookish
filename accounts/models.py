from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(null=True,blank=True,)
    email= models.EmailField(unique=True)
    image = models.ImageField(upload_to='profile', null=True, blank=True)
    following = models.ManyToManyField('self',through="Network",related_name='followers', symmetrical=False)
    def __str__(self) -> str:
        return self.username

class Network(models.Model):
    user_from = models.ForeignKey(CustomUser,related_name='rel_from_set',on_delete=models.CASCADE)
    user_to = models.ForeignKey(CustomUser,related_name='rel_to_set',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [models.Index(fields=["-created"])]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'