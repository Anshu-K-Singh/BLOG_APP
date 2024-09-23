from django.contrib import admin
from .models import Post
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author', 'publish', 'status', 'created']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish"
    ordering = ("status", "publish")
    raw_id_fields = ['author']
    #show_facets = admin.ShowFacets.ALWAYS 

