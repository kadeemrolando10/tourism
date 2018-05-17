from django.db import models
from django.http import HttpResponse


class Event(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    file = models.FileField(upload_to='media/', null='true', verbose_name='Imagen o Video')
    description = models.TextField(verbose_name='Descripcion')
    location = models.URLField(max_length=500, blank=True, default='', verbose_name='Ubicacion')
    event_date = models.DateField(verbose_name='Fecha de Evento')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['event_date']


class Schedule(models.Model):
    day = models.CharField(max_length=150, default='NA', verbose_name='Dia')
    description = models.CharField(max_length=150, default='NA', verbose_name='Descripcion')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return "%s %s" % (self.day, self.description)

    class Meta:
        verbose_name = 'Horario de Atencion'
        verbose_name_plural = 'Horarios de Atencion'
        ordering = ['published_date']


class RestaurantMenu(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=5.1, verbose_name='Precio')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Menu de Restaurante'
        verbose_name_plural = 'Menus de Restaurantes'
        ordering = ['price']


class RestaurantService(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Servicio de Restaurante'
        verbose_name_plural = 'Servicios de Restaurantes'
        ordering = ['title']


class Restaurant(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    service = models.ManyToManyField(RestaurantService, verbose_name='Servicios')
    menu = models.ManyToManyField(RestaurantMenu, verbose_name='Menu')
    schedule = models.ManyToManyField(Schedule, verbose_name='Horario')
    address = models.CharField(max_length=150, unique=True, default='S/N', verbose_name='Direccion')
    location = models.URLField(max_length=500, blank=True, default='', verbose_name='Ubicacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', default='nn')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'
        ordering = ['rating']


class Transport(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    schedule = models.ManyToManyField(Schedule, verbose_name='Horario')
    address = models.CharField(max_length=150, unique=True, default='S/N', verbose_name='Direccion')
    location = models.URLField(max_length=500, blank=True, default='', verbose_name='Ubicacion')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', default='nn')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Transporte'
        verbose_name_plural = 'Transportes'
        ordering = ['rating']


class TransportDestination(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, verbose_name='Transporte')
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    schedules_out = models.CharField(max_length=150, default='NA', verbose_name='Horarios de salida')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return "%s %s" % (self.title, self.transport.title)

    class Meta:
        verbose_name = 'Destino de Transporte'
        verbose_name_plural = 'Destinos de Transportes'
        ordering = ['title']


class TransportService(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Item de servicio')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Servicio de Transporte'
        verbose_name_plural = 'Servicios  de Transportes'
        ordering = ['title']


class TransportTypeService(models.Model):
    destination = models.ForeignKey(TransportDestination, on_delete=models.CASCADE, verbose_name='Destino')
    title = models.CharField(max_length=150, default='NA', verbose_name='Tipo de Servicio')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=5.1, verbose_name='Precio')
    service = models.ManyToManyField(TransportService, verbose_name='Servicios')
    image_bus = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen de Bus')
    image_seat = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen de Butacas')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return "%s %s %s" % (self.title, self.destination.title, self.destination.transport.title)

    class Meta:
        verbose_name = 'Tipo de Servicio de Transporte'
        verbose_name_plural = 'Tipos de Servicios de Transportes'
        ordering = ['title']


class LodgingType(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripcion')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tipo de Hospedaje'
        verbose_name_plural = 'Tipos de Hospedajes'
        ordering = ['title']


class LodgingService(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Servicio de Hospedaje'
        verbose_name_plural = 'Servicios de Hospedajes'
        ordering = ['title']


class Lodging(models.Model):
    type = models.ForeignKey(LodgingType, on_delete=models.CASCADE, verbose_name='Tipo')
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    schedule = models.ManyToManyField(Schedule, verbose_name='Horario')
    service = models.ManyToManyField(LodgingService, verbose_name='Servicio')
    address = models.CharField(max_length=150, unique=True, default='S/N', verbose_name='Direccion')
    location = models.URLField(max_length=500, blank=True, default='', verbose_name='Ubicacion')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', default='nn')

    def __str__(self):
        return "%s %s" % (self.title, self.type.title)

    class Meta:
        verbose_name = 'Hospedaje'
        verbose_name_plural = 'Hospedajes'
        ordering = ['rating']


class LodgingRoom(models.Model):
    lodging = models.ForeignKey(Lodging, on_delete=models.CASCADE, verbose_name='Tipo')
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=5.1, verbose_name='Precio')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return "%s %s %s" % (self.title, self.lodging.title, self.lodging.type.title)

    class Meta:
        verbose_name = 'Cuarto de Hospedaje'
        verbose_name_plural = 'Cuartos de Hospedajes'
        ordering = ['price']


class AgencyService(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    duration = models.CharField(max_length=150, default='S/N', verbose_name='Duracion')
    departures = models.CharField(max_length=150, default='S/N', verbose_name='Salidas')
    schedule = models.CharField(max_length=150, default='S/N', verbose_name='Horas de Expedicion')
    place_start = models.CharField(max_length=150, default='S/N', verbose_name='Lugar de Inicio')
    places_to_known = models.CharField(max_length=500, default='S/N', verbose_name='Lugares a conocer')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Paquete de Agencia'
        verbose_name_plural = 'Paquetes de Agencias'
        ordering = ['title']


class Agency(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    service = models.ManyToManyField(AgencyService, verbose_name='Paquetes de turismo')
    schedule = models.ManyToManyField(Schedule, verbose_name='Horario')
    address = models.CharField(max_length=150, default='S/N', verbose_name='Direccion')
    location = models.URLField(max_length=500, default='', verbose_name='Ubicacion')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', default='nn')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Agencia de turismo'
        verbose_name_plural = 'Agencias de turismo'
        ordering = ['rating']


class TourismSiteDestiny(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Destino de Sitio Turistico'
        verbose_name_plural = 'Destinos de Sitios Turisticos'
        ordering = ['title']


class TourismSiteType(models.Model):
    destination = models.ForeignKey(TourismSiteDestiny, on_delete=models.CASCADE, verbose_name='Tipo')
    title = models.CharField(max_length=150, verbose_name='Titulo')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tipo de Sitio Turistico'
        verbose_name_plural = 'Tipos de Sitios Turisticos'
        ordering = ['title']


class TourismSiteService(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Item de servicio')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Servicio de Sitio Turistico'
        verbose_name_plural = 'Servicios  de Sitios Turisticos'
        ordering = ['title']


class TourismSite(models.Model):
    type = models.ForeignKey(TourismSiteType, on_delete=models.CASCADE, verbose_name='Tipo')
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion')
    schedule = models.ManyToManyField(Schedule, verbose_name='Horarios')
    service = models.ManyToManyField(TourismSiteService, verbose_name='Servicios')
    location = models.URLField(max_length=500, blank=True, default='', verbose_name='Ubicacion')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.1, verbose_name='Calificacion')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')
    address = models.CharField(max_length=150, verbose_name='Direccion', default='sn')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', default='nn')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Sitio turistico'
        verbose_name_plural = 'Sitios turisticos'
        ordering = ['rating']


class TourismSiteMenu(models.Model):
    site = models.ForeignKey(TourismSite, on_delete=models.CASCADE, verbose_name='Sitio')
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.CharField(max_length=150, default='NA', verbose_name='Descripcion')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Menu de Sitio Turistico'
        verbose_name_plural = 'Menu  de Sitios Turisticos'
        ordering = ['title']


class Objective(models.Model):
    description = models.TextField(verbose_name='Descripcion', unique=True)
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Objetivo'
        verbose_name_plural = 'Objetivos'
        ordering = ['description']


class Function(models.Model):
    description = models.TextField(verbose_name='Descripcion', unique=True)
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Funcion'
        verbose_name_plural = 'Funciones'
        ordering = ['description']


class Document(models.Model):
    title = models.CharField(max_length=100, null=True, verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripcion', unique=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d', null=True, verbose_name='Archivo pdf')
    published_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de Publicacion')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['file']
