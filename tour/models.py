from django.db import models
from multiselectfield import MultiSelectField
from django.http import HttpResponse


class Event(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion')
    location = models.URLField(max_length=500, blank=True, default='', verbose_name='Ubicacion')
    event_date = models.DateField(verbose_name='Fecha de Evento')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', default='nn')
    schedule = models.CharField(max_length=150, verbose_name='Horarios', default='--')

    def __str__(self):
        return self.title


class Menu_Restaurant(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripcion')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=5.1, verbose_name='Precio')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title


class Schedule_Restaurant(models.Model):
    day = models.CharField(max_length=150, default='NA', verbose_name='Dia')
    description = models.CharField(max_length=150, default='NA', verbose_name='Descripcion')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return "%s %s" % (self.day, self.description)


class Service_Restaurant(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title


class Restaurant(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    service = models.ManyToManyField(Service_Restaurant, verbose_name='Servicios')
    menu = models.ManyToManyField(Menu_Restaurant, verbose_name='Menu')
    schedule = models.ManyToManyField(Schedule_Restaurant, verbose_name='Horario')
    address = models.CharField(max_length=150, unique=True, default='S/N', verbose_name='Direccion')
    location = models.URLField(max_length=500, blank=True, default='', verbose_name='Ubicacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', default='nn')

    def __str__(self):
        return self.title


class Service_Transport(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripcion')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title


class Transport(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    service = models.ManyToManyField(Service_Transport)
    address = models.CharField(max_length=150, unique=True, default='S/N', verbose_name='Direccion')
    location = models.URLField(max_length=500, blank=True, default='', verbose_name='Ubicacion')
    DESTINY = ((1, 'SUCRE'),
               (2, 'LA PAZ'),
               (3, 'ORURO'),
               (4, 'SANTA CRUZ'),
               (5, 'TARIJA'),
               (6, 'COCHABAMBA'),
               (7, 'BENI'),
               (8, 'PANDO'),)
    destination = MultiSelectField(choices=DESTINY, max_choices=100, max_length=100, default=1, verbose_name='Destinos')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', default='nn')
    schedule = models.CharField(max_length=150, verbose_name='Horarios', default='--')

    def __str__(self):
        return self.title


class Lodgment_type(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripcion')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')
    def __str__(self):
        return self.title


class Service_Lodgment(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripcion')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title


class Lodgment(models.Model):
    type = models.ForeignKey(Lodgment_type, on_delete=models.CASCADE, verbose_name='Tipo')
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    service = models.ManyToManyField(Service_Lodgment)
    address = models.CharField(max_length=150, unique=True, default='S/N', verbose_name='Direccion')
    location = models.URLField(max_length=500, blank=True, default='', verbose_name='Ubicacion')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', default='nn')
    schedule = models.CharField(max_length=150, verbose_name='Horarios', default='--')

    def __str__(self):
        return self.title


class Service_Agency(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripcion')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title


class Agency(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    service = models.ManyToManyField(Service_Agency)
    address = models.CharField(max_length=150, unique=True, default='S/N', verbose_name='Direccion')
    location = models.URLField(max_length=500, blank=True, default='', verbose_name='Ubicacion')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', default='nn')
    schedule = models.CharField(max_length=150, verbose_name='Horarios', default='--')

    def __str__(self):
        return self.title


class Tourism_site(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion')
    location = models.URLField(max_length=500, blank=True, default='', verbose_name='Ubicacion')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')
    address = models.CharField(max_length=150, verbose_name='Direccion', default='sn')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', default='nn')
    schedule = models.CharField(max_length=150, verbose_name='Horarios', default='--')

    def __str__(self):
        return self.title


class Objetive(models.Model):
    description = models.TextField(verbose_name='Descripcion', unique=True)
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.description


class Function(models.Model):
    description = models.TextField(verbose_name='Descripcion', unique=True)
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.description


class Document(models.Model):
    filename = models.CharField(max_length=100, verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripcion', unique=True)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', verbose_name='Archivo pdf')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.description
