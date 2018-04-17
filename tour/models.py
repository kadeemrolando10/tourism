from django.db import models
from multiselectfield import MultiSelectField


class Event(models.Model):
    title = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='media/', verbose_name='Image')
    description = models.TextField()
    location = models.URLField()
    published_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Service_Restaurant(models.Model):
    title = models.CharField(max_length=150, default='NA')
    description = models.TextField()

    def __str__(self):
        return self.title


class Restaurant(models.Model):
    title = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='media/', verbose_name='Image')
    service = models.ManyToManyField(Service_Restaurant)
    address = models.CharField(max_length=150, unique=True, default='S/N',)
    location = models.URLField()
    rating_data = (
        (u'1', u'✭'),
        (u'2', u'✭✭'),
        (u'3', u'✭✭✭'),
        (u'4', u'✭✭✭✭'),
        (u'5', u'✭✭✭✭✭'),
    )
    rating = models.CharField(max_length=100, choices=rating_data, default=1, )
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Service_Transport(models.Model):
    title = models.CharField(max_length=150, default='NA')
    description = models.TextField()

    def __str__(self):
        return self.title


class Transport(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='media/', verbose_name='Image')
    service = models.ManyToManyField(Service_Transport)
    address = models.CharField(max_length=150, unique=True, default='S/N',)
    location = models.URLField()
    DESTINY = ((1, 'SUCRE'),
               (2, 'LA PAZ'),
               (3, 'ORURO'),
               (4, 'SANTA CRUZ'),
               (5, 'TARIJA'),
               (6, 'COCHABAMBA'),
               (7, 'BENI'),
               (8, 'PANDO'),)
    destination = MultiSelectField(choices=DESTINY, max_choices=100, max_length=100, default=1,)
    rating_data = (
        (u'1', u'✭'),
        (u'2', u'✭✭'),
        (u'3', u'✭✭✭'),
        (u'4', u'✭✭✭✭'),
        (u'5', u'✭✭✭✭✭'),
    )
    rating = models.CharField(max_length=100, choices=rating_data, default=1, )
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Lodgment_type(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.title


class Service_Lodgment(models.Model):
    title = models.CharField(max_length=150, default='NA')
    description = models.TextField()

    def __str__(self):
        return self.title


class Lodgment(models.Model):
    type = models.ForeignKey(Lodgment_type, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='media/', verbose_name='Image')
    service = models.ManyToManyField(Service_Lodgment)
    address = models.CharField(max_length=150, unique=True, default='S/N',)
    location = models.URLField()
    rating_data = (
        (u'1', u'✭'),
        (u'2', u'✭✭'),
        (u'3', u'✭✭✭'),
        (u'4', u'✭✭✭✭'),
        (u'5', u'✭✭✭✭✭'),
    )
    rating = models.CharField(max_length=100, choices=rating_data, default=1, )
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Service_Agency(models.Model):
    title = models.CharField(max_length=150, default='NA')
    description = models.TextField()

    def __str__(self):
        return self.title


class Agency(models.Model):
    title = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='media/', verbose_name='Image')
    service = models.ManyToManyField(Service_Agency)
    address = models.CharField(max_length=150, unique=True, default='S/N',)
    location = models.URLField()
    rating_data = (
        (u'1', u'✭'),
        (u'2', u'✭✭'),
        (u'3', u'✭✭✭'),
        (u'4', u'✭✭✭✭'),
        (u'5', u'✭✭✭✭✭'),
    )
    rating = models.CharField(max_length=100, choices=rating_data, default=1, )
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Tourism_site(models.Model):
    title = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='media/', verbose_name='Image')
    description = models.TextField()
    location = models.URLField()
    rating_data = (
        (u'1', u'✭'),
        (u'2', u'✭✭'),
        (u'3', u'✭✭✭'),
        (u'4', u'✭✭✭✭'),
        (u'5', u'✭✭✭✭✭'),
    )
    rating = models.CharField(max_length=100, choices=rating_data, default=1, )
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.title
