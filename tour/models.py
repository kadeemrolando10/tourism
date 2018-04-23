from django.db import models
from multiselectfield import MultiSelectField


class Event(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion')
    location = models.URLField(verbose_name='Ubicacion')
    event_date = models.DateTimeField( verbose_name='Fecha de Evento' )
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title


class Service_Restaurant(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripcion')

    def __str__(self):
        return self.title


class Restaurant(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    service = models.ManyToManyField(Service_Restaurant)
    address = models.CharField(max_length=150, unique=True, default='S/N',verbose_name='Direccion')
    location = models.URLField(verbose_name='Ubicacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    rating = models.DecimalField( max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title


class Service_Transport(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    description = models.TextField( verbose_name='Descripcion')

    def __str__(self):
        return self.title


class Transport(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    service = models.ManyToManyField(Service_Transport)
    address = models.CharField(max_length=150, unique=True, default='S/N', verbose_name='Direccion')
    location = models.URLField(verbose_name='Ubicacion')
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

    def __str__(self):
        return self.title


class Lodgment_type(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripcion')

    def __str__(self):
        return self.title


class Service_Lodgment(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    description = models.TextField( verbose_name='Descripcion')

    def __str__(self):
        return self.title


class Lodgment(models.Model):
    type = models.ForeignKey(Lodgment_type, on_delete=models.CASCADE, verbose_name='Tipo')
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    service = models.ManyToManyField(Service_Lodgment)
    address = models.CharField(max_length=150, unique=True, default='S/N',verbose_name='Direccion')
    location = models.URLField(verbose_name='Ubicacion')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title


class Service_Agency(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripcion')

    def __str__(self):
        return self.title


class Agency(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    service = models.ManyToManyField(Service_Agency)
    address = models.CharField(max_length=150, unique=True, default='S/N',verbose_name='Direccion' )
    location = models.URLField(verbose_name='Ubicacion')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title


class Tourism_site(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion')
    location = models.URLField(verbose_name='Ubicacion')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title
