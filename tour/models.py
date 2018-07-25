from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

DAYS = (
    ('LU', 'LUNES'),
    ('MA', u'MARTES'),
    ('MI', u'MIERCOLES'),
    ('JU', u'JUEVES'),
    ('VI', u'VIERNES'),
    ('SA', u'SABADO'),
    ('DO', u'DOMINGO'),
)


class Agency(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    address = models.CharField(max_length=150, default=' ', verbose_name='Direccion')
    score = models.DecimalField(decimal_places=1, max_digits=2, verbose_name='Calificacion', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', blank=True)
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    lat = models.CharField(max_length=50, verbose_name='Latitud')
    lng = models.CharField(max_length=50, verbose_name='Longitud')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Agencia de turismo'
        verbose_name_plural = 'Agencias de turismo'
        ordering = ['score']


class AgencyService(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, verbose_name='Agencia')
    title = models.CharField(max_length=150, verbose_name='Titulo')
    duration = models.CharField(max_length=150, default='S/N', verbose_name='Duracion', blank=True)
    departures = models.CharField(max_length=150, default='S/N', verbose_name='Dias de expedicion')
    schedule = models.CharField(max_length=150, default='S/N', verbose_name='Horas de Expedicion', blank=True)
    place_start = models.CharField(max_length=150, default='S/N', verbose_name='Lugar de Inicio')
    places_to_known = models.CharField(max_length=500, default='S/N', verbose_name='Lugares a conocer')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Paquete de Agencia'
        verbose_name_plural = 'Paquetes de Agencias'
        ordering = ['title']


class AgencySchedule(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, verbose_name='Agencia')
    day = models.CharField(max_length=2, choices=DAYS, default='1', verbose_name='Dia')
    schedule = models.CharField(max_length=50, default='8:00 - 22:00', verbose_name='Horario')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'Horario de Atencion'
        verbose_name_plural = 'Horarios de Atencion'
        ordering = ['register_at']


class Event(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    file = models.FileField(upload_to='media/', null='true', verbose_name='Imagen o Video')
    description = models.TextField(verbose_name='Descripcion')
    lat = models.CharField(max_length=50, verbose_name='Latitud')
    lng = models.CharField(max_length=50, verbose_name='Longitud')
    event_date = models.DateField(verbose_name='Fecha de Evento')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['event_date']


class RestaurantService(models.Model):
    title = models.TextField(max_length=150, default='NA', verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Servicio de Restaurante'
        verbose_name_plural = 'Servicios de Restaurantes'
        ordering = ['title']


class Restaurant(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    service = models.ManyToManyField(RestaurantService, verbose_name='Servicios', null=True, blank=True)
    address = models.CharField(max_length=150, unique=True, default='S/N', verbose_name='Direccion')
    lat = models.CharField(max_length=50, verbose_name='Latitud')
    lng = models.CharField(max_length=50, verbose_name='Longitud')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    score = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Calificacion', blank=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'
        ordering = ['score']


class RestaurantSchedule(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Restaurant')
    day = models.CharField(max_length=2, choices=DAYS, default='1', verbose_name='Dia')
    schedule = models.CharField(max_length=50, default='NA', verbose_name='Horario')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'Horario de Atencion de Restaurant'
        verbose_name_plural = 'Horarios de Atencion de Restaurantes'
        ordering = ['register_at']


class RestaurantMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Restaurant')
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=5.1, verbose_name='Precio')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Menu de Restaurante'
        verbose_name_plural = 'Menus de Restaurantes'
        ordering = ['price']


class Transport(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    address = models.CharField(max_length=150, unique=True, default='S/N', verbose_name='Direccion')
    lat = models.CharField(max_length=50, verbose_name='Latitud')
    lng = models.CharField(max_length=50, verbose_name='Longitud')
    score = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Calificacion' , blank=True)
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Transporte'
        verbose_name_plural = 'Transportes'
        ordering = ['score']


class TransportDestination(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, verbose_name='Transporte')
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    schedules_out = models.CharField(max_length=150, default='NA', verbose_name='Horarios de salida', blank=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Destino de Transporte'
        verbose_name_plural = 'Destinos de Transportes'
        ordering = ['title']


class TransportService(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Item de servicio')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Servicio de Transporte'
        verbose_name_plural = 'Servicios  de Transportes'
        ordering = ['title']


class TransportTypeService(models.Model):
    destination = models.ForeignKey(TransportDestination, on_delete=models.CASCADE, verbose_name='Destino')
    title = models.CharField(max_length=150, default='NA', verbose_name='Tipo de Servicio')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=5.1, verbose_name='Precio')
    service = models.ManyToManyField(TransportService, verbose_name='Servicios', null=True, blank=True)
    image_bus = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen de Bus')
    image_seat = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen de Butacas')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tipo de Servicio de Transporte'
        verbose_name_plural = 'Tipos de Servicios de Transportes'
        ordering = ['title']


class TransportSchedule(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, verbose_name='Transporte')
    day = models.CharField(max_length=2, choices=DAYS, default='1', verbose_name='Dia')
    schedule = models.CharField(max_length=50, default='NA', verbose_name='Horario')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'Horario de Atencion de Transporte'
        verbose_name_plural = 'Horarios de Atencion de Transportes'
        ordering = ['register_at']


class LodgingType(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tipo de Hospedaje'
        verbose_name_plural = 'Tipos de Hospedajes'
        ordering = ['title']


class LodgingService(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

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
    service = models.ManyToManyField(LodgingService, verbose_name='Servicio', null=True, blank=True)
    address = models.CharField(max_length=150, unique=True, default='S/N', verbose_name='Direccion')
    lat = models.CharField(max_length=50, verbose_name='Latitud')
    lng = models.CharField(max_length=50, verbose_name='Longitud')
    score = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Calificacion', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Hospedaje'
        verbose_name_plural = 'Hospedajes'
        ordering = ['score']


class LodgingRoom(models.Model):
    lodging = models.ForeignKey(Lodging, on_delete=models.CASCADE, verbose_name='Tipo')
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100, verbose_name='Precio')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Cuarto de Hospedaje'
        verbose_name_plural = 'Cuartos de Hospedajes'
        ordering = ['price']


class LodgingSchedule(models.Model):
    lodging = models.ForeignKey(Lodging, on_delete=models.CASCADE, verbose_name='Hospedaje')
    day = models.CharField(max_length=2, choices=DAYS, default='1', verbose_name='Dia')
    schedule = models.CharField(max_length=50, default='7:00 - 23:00', verbose_name='Horario')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'Horario de Atencion de Hospedaje'
        verbose_name_plural = 'Horarios de Atencion de Hospedajes'
        ordering = ['register_at']


class TourismSiteDestiny(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Destino de Sitio Turistico'
        verbose_name_plural = 'Destinos de Sitios Turisticos'
        ordering = ['title']


class TourismSiteType(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tipo de Sitio Turistico'
        verbose_name_plural = 'Tipos de Sitios Turisticos'
        ordering = ['title']


class TourismSiteService(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Item de servicio')
    image = models.ImageField(upload_to='media/',verbose_name='Imagen')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Servicio de Sitio Turistico'
        verbose_name_plural = 'Servicios  de Sitios Turisticos'
        ordering = ['title']


class TourismSite(models.Model):
    destination = models.ForeignKey(TourismSiteDestiny, on_delete=models.CASCADE, verbose_name='Localizacion')
    type = models.ForeignKey(TourismSiteType, on_delete=models.CASCADE, verbose_name='Tipo')
    service = models.ManyToManyField(TourismSiteService, verbose_name='Servicios', null=True, blank=True)
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion', blank=True)
    lat = models.CharField(max_length=50, verbose_name='Latitud')
    lng = models.CharField(max_length=50, verbose_name='Longitud')
    score = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Calificacion', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    address = models.CharField(max_length=150, verbose_name='Direccion', default=' ')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Sitio turistico'
        verbose_name_plural = 'Sitios turisticos'
        ordering = ['score']


class TourismSiteMenu(models.Model):
    site = models.ForeignKey(TourismSite, on_delete=models.CASCADE, verbose_name='Sitio Turistico')
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion', blank=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Menu de Sitio Turistico'
        verbose_name_plural = 'Menu  de Sitios Turisticos'
        ordering = ['title']


class TourismSiteSchedule(models.Model):
    site = models.ForeignKey(TourismSite, on_delete=models.CASCADE, verbose_name='Sitio Turistico')
    day = models.CharField(max_length=2, choices=DAYS, default='1', verbose_name='Dia')
    schedule = models.CharField(max_length=50, default='NA', verbose_name='Horario')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'Horario de Atencion de Sitio Turistico'
        verbose_name_plural = 'Horarios de Atencion de Sitios Turisticos'
        ordering = ['register_at']


class TourismRouteDestiny(models.Model):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Destino de Ruta Turistica'
        verbose_name_plural = 'Destinos de Rutas Turisticas'
        ordering = ['title']


class TourismRoute(models.Model):
    destination = models.ForeignKey(TourismRouteDestiny, on_delete=models.CASCADE, verbose_name='Destino')
    title = models.CharField(max_length=150, unique=True, verbose_name='Titulo')
    lat_origin = models.CharField(max_length=50, verbose_name='Latitud de Origen')
    lng_origin = models.CharField(max_length=50, verbose_name='Longitud de Origen')
    lat_destination = models.CharField(max_length=50, verbose_name='Latitud de Destino')
    lng_destination = models.CharField(max_length=50, verbose_name='Longitud de Destino')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion', blank=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Calificacion', blank=True)
    date = models.DateField (verbose_name='Fecha de Evento', blank=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ruta turistica'
        verbose_name_plural = 'Rutas turisticas'
        ordering = ['score']


class TourismRouteMenu(models.Model):
    route = models.ForeignKey(TourismRoute, on_delete=models.CASCADE, verbose_name='Ruta Turistica')
    title = models.CharField(max_length=150, default='NA', verbose_name='Titulo')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(default='NA', verbose_name='Descripcion', blank=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Menu de Ruta Turistica'
        verbose_name_plural = 'Menu  de Rutas Turisticas'
        ordering = ['title']


class Objective(models.Model):
    description = models.TextField(verbose_name='Descripcion', unique=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Objetivo'
        verbose_name_plural = 'Objetivos'
        ordering = ['description']


class Function(models.Model):
    description = models.TextField(verbose_name='Descripcion', unique=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Funcion'
        verbose_name_plural = 'Funciones'
        ordering = ['description']


class Law(models.Model):
    title = models.CharField(max_length=100, verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripcion', unique=True, blank=True,)
    file = models.FileField(upload_to='documents/%Y/%m/%d', null=True, verbose_name='Archivo pdf')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['title']


GENDER = (('F', 'FEMENINO'), ('M', 'MASCULINO'))

ROLE_USERS = (
    ('AD', 'ADMINISTRADOR'),
    ('US', 'USUARIO'),
)


class Client(models.Model):
    user = models.OneToOneField(User, unique=True, blank=True, null=True, on_delete=models.CASCADE)
    ci = models.CharField(max_length=12, unique=True, verbose_name='CI')
    first_name = models.CharField(max_length=100, default='', verbose_name='Nombres')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Apellidos')
    gender = models.CharField(max_length=2, choices=GENDER, verbose_name=u'Género')
    rol = models.CharField(max_length=2, choices=ROLE_USERS, default='R', verbose_name='Rol')
    register_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    def __unicode__(self):
        return "%s %s" % (self.last_name, self.first_name)

    def __str__(self):
        return "%s %s" % (self.last_name, self.first_name)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['last_name', 'first_name']
