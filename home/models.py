from django.db import models

class Feature(models.Model):
    icon = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.title

class AboutBullet(models.Model):
    icon = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.title

class OverviewStep(models.Model):
    order = models.PositiveIntegerField(default=0)
    icon = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    desc = models.TextField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.title}"

class Testimonial(models.Model):
    quote = models.TextField()
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} - {self.role}"


class PricingOption(models.Model):
    title = models.CharField(max_length=100)
    headline = models.CharField(max_length=200)
    description = models.TextField()
    features = models.TextField(help_text="Use newline-separated features")
    cta_text = models.CharField(max_length=100)
    cta_link = models.URLField(blank=True)  # Could also be a CharField if you want template tags
    
    def get_features_list(self):
        return self.features.splitlines()

    def __str__(self):
        return self.title