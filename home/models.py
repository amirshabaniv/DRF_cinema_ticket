from django.db import models
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    image1 = models.ImageField(upload_to='actors_images')
    image2 = models.ImageField(null=True, blank=True, upload_to='actors_images')
    image3 = models.ImageField(null=True, blank=True, upload_to='actors_images')
    image4 = models.ImageField(null=True, blank=True, upload_to='actors_images')

    def __str__(self):
        return self.name



class Movie(models.Model):
    category = models.ManyToManyField(Category, related_name='c_movies')
    actor = models.ManyToManyField(Actor, related_name='a_movies')
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    director = models.CharField(max_length=80)
    description = models.TextField(max_length=2000)
    coming_soon = models.BooleanField(null=True, blank=True)
    image1 = models.ImageField(upload_to='movies_images')
    image2 = models.ImageField(null=True, blank=True, upload_to='movies_images')
    image3 = models.ImageField(null=True, blank=True, upload_to='movies_images')
    image4 = models.ImageField(null=True, blank=True, upload_to='movies_images')
    is_availabe = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_comments')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='m_comments', null=True)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    @property
    def comment_likes_count(self):
        return self.c_likes.count()
    
    @property
    def comment_dislikes_count(self):
        return self.c_dislikes.count()
    
    """
    The following method is used in the front-end for conditions and restricting user access:
    user can not like this movie again if user liked this movie.
    user can not dislike this movie if user liked this movie.
    """
    def user_did_like(self, user):
        user_like = user.u_c_likes.filter(comment=self)
        if user_like.exists():
            return True
        return False

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'
    

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_c_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='c_likes')

    class Meta:
        unique_together = ('comment', 'user')

    
    def __str__(self):
        return f'{self.user} liked {self.comment.body[:10]}'
    

class CommentDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_c_dislikes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='c_dislikes')

    class Meta:
        unique_together = ('comment', 'user')
    
    def __str__(self):
        return f'{self.user} disliked {self.comment.body[:10]}'


class MovieRating(models.Model):
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars')
    )
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name = 'm_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return f"{self.user}'s {self.rating}-star rating for {self.movie}"


class ContactUs(models.Model):
    phone_number = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Call Us'
        verbose_name_plural = 'Call Us'

    def __str__(self):
        return self.phone_number 

