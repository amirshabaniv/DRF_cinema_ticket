from django.contrib import admin
from .models import Actor, Movie, Category, Comment, CommentLike, CommentDislike, MovieRating, ContactUs

admin.site.register(Actor)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name']
    raw_id_fields = ('category', 'actor')

admin.site.register(Category)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'created']
    raw_id_fields = ('user',)

admin.site.register(CommentLike)

admin.site.register(CommentDislike)

admin.site.register(MovieRating)

admin.site.register(ContactUs)





