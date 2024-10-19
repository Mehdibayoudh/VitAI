from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=[
        ('cardio', 'Cardio'),
        ('strength', 'Strength'),
        ('flexibility', 'Flexibility')
    ])
    muscles_targeted = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    calories_burned_per_minute = models.FloatField()
    image = models.ImageField(upload_to='exercises/', blank=True, null=True , default='../../static/assets/img/blog/img_04.png')

    def __str__(self):
        return self.name
