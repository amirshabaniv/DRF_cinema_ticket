from django.db import models
from accounts.models import User
from home.models import Movie


class PlayTime(models.Model):
    from_to = models.CharField(max_length=50)
    ticket_price = models.PositiveIntegerField()
    movie = models.ManyToManyField(Movie, related_name='m_play_time')

    def __str__(self):
        return self.from_to


class Cinema(models.Model):
    name = models.CharField(max_length=50)
    movie = models.ManyToManyField(Movie, related_name='m_cinema')
    address = models.CharField(max_length=100)
    buffet = models.BooleanField(default=False, null=True)
    cart_reader = models.BooleanField(default=False, null=True)
    ticket_print = models.BooleanField(default=False, null=True)
    accessible = models.BooleanField(default=False, null=True)
    libary = models.BooleanField(default=False, null=True)
    resturant = models.BooleanField(default=False, null=True)
    coffe_shop = models.BooleanField(default=False, null=True)
    ATM = models.BooleanField(default=False, null=True)
    elevator = models.BooleanField(default=False, null=True)
    parking = models.BooleanField(default=False, null=True)
    image = models.ImageField(upload_to='cinema_images')
    description = models.TextField(max_length=800)
    phone = models.CharField(max_length=15)
    carwash = models.BooleanField(default=False, null=True, blank=True)
    play_time = models.ManyToManyField(PlayTime, related_name='pt_cinemas')

    def __str__(self):
        return self.name


class DayAndDate(models.Model):
    day_name = models.CharField(max_length=30)
    date_name = models.CharField(max_length=20)

    def __str__(self):
        return f'day: {self.day_name} | date: {self.date_name}'


class Schedule(models.Model):
    cinema = models.OneToOneField(Cinema, on_delete=models.CASCADE, related_name='c_times')
    movie = models.ManyToManyField(Movie, related_name='m_times')
    day_and_date = models.ManyToManyField(DayAndDate, related_name='dd_schedule')

    def __str__(self):
        return f'This schedule is for {self.cinema}'


class CinemaRating(models.Model):
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars')
    )
    
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name = 'c_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cinema', 'user')

    def __str__(self):
        return f"{self.user}'s {self.rating}-star rating for {self.cinema}"
    

class CinemaComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_cinemacomments')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='c_cinemacomments')
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    @property
    def comment_likes_count(self):
        return self.cc_likes.count()
    
    @property
    def comment_dislikes_count(self):
        return self.cc_dislikes.count()
    
    """
    The following method is used in the front-end for conditions and restricting user access:
    user can not like this movie again if user liked this movie.
    user can not dislike this movie if user liked this movie.
    """
    def user_did_like(self, user):
        user_like = user.u_cc_likes.filter(comment=self)
        if user_like.exists():
            return True
        return False

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'
    

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_cc_likes')
    comment = models.ForeignKey(CinemaComment, on_delete=models.CASCADE, related_name='cc_likes')

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f'{self.user} liked {self.comment.body[:10]}'
    

class CommentDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_cc_dislikes')
    comment = models.ForeignKey(CinemaComment, on_delete=models.CASCADE, related_name='cc_dislikes')

    class Meta:
        unique_together = ('comment', 'user')
    
    def __str__(self):
        return f'{self.user} disliked {self.comment.body[:10]}'