from django.contrib import admin
from .models import Book,Saved,SavedBook , Genre

class BookAdmin(admin.ModelAdmin):
    list_display= ('title','user','author','is_visible','size')
    
admin.site.register(Book,BookAdmin)

admin.site.register(Genre)


class SavedBookInline(admin.TabularInline):
    model=SavedBook

class SavedAdmin(admin.ModelAdmin):
    inlines=[SavedBookInline]
    list_display= ['id','user','at']
    
admin.site.register(Saved,SavedAdmin)
