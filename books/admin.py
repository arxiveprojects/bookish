from django.contrib import admin
from .models import Book,Favorite,FavoriteBook , Genre

class BookAdmin(admin.ModelAdmin):
    list_display= ('title','user','author','is_visible','size')
    
admin.site.register(Book,BookAdmin)

admin.site.register(Genre)


class FavoriteBookInline(admin.TabularInline):
    model=FavoriteBook

class FavoriteAdmin(admin.ModelAdmin):
    inlines=[FavoriteBookInline]
    list_display= ['id','user','at']
    
admin.site.register(Favorite,FavoriteAdmin)
