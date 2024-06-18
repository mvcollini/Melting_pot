from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static


class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def get_profile_picture_url(self):
        if self.profile_image:
            return self.profile_image.url
        return static('images/defaultprofile.jpg')

    def count_recipes(self):
        return self.recipe_set.count()

    def count_followers(self):
        return self.followers.count()

    # count the instances where user is the followee

    def count_following(self):
        return self.following.count()

    # count the instances where user is the follower

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='recipes_photos/', blank=True, null=True)
    preparationtime = models.CharField(help_text="Totale tempo di preparazione (es: 1 hour 30 minutes)", max_length=200,
                                       blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    ingredients = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.title


class SavedRecipe(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class Follow(models.Model):
    # questo è il seguace
    utente = models.ForeignKey('CustomUser', related_name='following', on_delete=models.CASCADE)
    # questo è il seguito
    followee = models.ForeignKey('CustomUser', related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('utente', 'followee')

