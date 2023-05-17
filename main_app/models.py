from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
    
class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.TextField()
    book_slug = models.SlugField("Book Slug", max_length=255, blank=False, null=False)
    ISBN = models.CharField(max_length=255, unique=True)
    year_of_publication = models.CharField(max_length=255)
    total_rating = models.CharField(max_length=255, null=True)
    img_s = models.CharField(max_length=255)
    img_m = models.CharField(max_length=255)
    img_l = models.CharField(max_length=255)

    def __str__(self):
        return self.ISBN
    # def __str__(self):
    #     return "%s %s" % (self.title, self.ISBN)
    
    @property
    def slug(self):
        return self.book_slug    

    # def get_absolute_url(self):
    #     return reverse('book_detail', args=[str(self.id)])
    
class Ratings(models.Model):
    # user_id = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    user_id = models.CharField(max_length=255)
    # ISBN = models.ForeignKey('Books', on_delete=models.CASCADE)
    ISBN = models.CharField(max_length=255)

    # rating = IntegerRangeField(default=0, min_value=0, max_value=10)
    rating = models.IntegerField(default=0, validators=[ MaxValueValidator(10), MinValueValidator(0)])

    def __str__(self):
        return self.pk