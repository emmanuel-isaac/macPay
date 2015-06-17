from django.db import models


class ComputerImage(models.Model):
    secure_url = models.URLField(max_length=500)
    public_id = models.TextField()
    height = models.IntegerField()
    width = models.IntegerField()
    original_filename = models.TextField()

    def __unicode__(self):
        return self.original_filename

class Computer(models.Model):
    name = models.CharField(max_length=100, blank=False)
    model = models.CharField(max_length=100, blank=False)
    cost = models.PositiveIntegerField(blank=False, null=False)
    comp_img = models.OneToOneField(ComputerImage, null=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.model)