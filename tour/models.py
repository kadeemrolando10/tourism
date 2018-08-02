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

MENU = (
    ('EN', 'ENTRADAS'),
    ('PO', u'POSTRES'),
    ('DE', u'DESAYUNO'),
    ('SE', u'SEGUNDOS'),
    ('BE', u'BEBIDAS'),
    ('CV', u'CARTA DE VINOS'),
    ('SO', u'SOPAS'),
)


class Location(models.Model):
    title = models.CharField(max_length=150, verbose_name='Nombre')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ubicacion'
        verbose_name_plural = 'Ubicaciones'
        ordering = ['title']
        permissions = (
            ('show_location', 'Can Details Location'),
            ('index_location', 'Can List Location'),
        )


class Agency(models.Model):
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Localizacion')
    title = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
    address = models.CharField(max_length=150, default=' ', verbose_name='Direccion')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    lat = models.CharField(max_length=50, verbose_name='Latitud')
    lng = models.CharField(max_length=50, verbose_name='Longitud')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    web = models.CharField(max_length=150, verbose_name='Pagina Web', blank=True)
    score = models.DecimalField(decimal_places=1, max_digits=2, verbose_name='Calificacion', blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Agencia de turismo'
        verbose_name_plural = 'Agencias de turismo'
        ordering = ['score']
        permissions = (
            ('show_agency', 'Can Details Agency'),
            ('index_agency', 'Can List Agency'),
        )


class AgencyService(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, verbose_name='Agencia')
    title = models.CharField(max_length=150, verbose_name='Nombre')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    duration = models.IntegerField(default=1, verbose_name='Duracion', blank=True)
    departures = models.CharField(max_length=350, default=' ', verbose_name='Dias de expedicion')
    schedule = models.CharField(max_length=350, default='8:00', verbose_name='Horas de partida', blank=True)
    place_start = models.CharField(max_length=350, default=' ', verbose_name='Ubicacion')
    places_to_known = models.TextField(default=' ', verbose_name='Descripcion')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Paquete de Agencia'
        verbose_name_plural = 'Paquetes de Agencias'
        ordering = ['title']
        permissions = (
            ('show_agencyservice', 'Can Details Service Agency'),
            ('index_agencyservice', 'Can List Service Agency'),
        )


class AgencySchedule(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, verbose_name='Agencia')
    day = models.CharField(max_length=2, choices=DAYS, unique=True, default='1', verbose_name='Dia')
    schedule = models.CharField(max_length=50, default='8:00 - 22:00', verbose_name='Horario')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'Horario de Atencion'
        verbose_name_plural = 'Horarios de Atencion'
        ordering = ['register_at']
        permissions = (
            ('show_agencyschedule', 'Can Details Schedule Agency'),
            ('index_agencyschedule', 'Can List Schedule Agency'),
        )


class Event(models.Model):
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Localizacion')
    title = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
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
        permissions = (
            ('show_event', 'Can Details Event'),
            ('index_event', 'Can List Event'),
        )


class RestaurantService(models.Model):
    title = models.TextField(max_length=150, default='NA', verbose_name='Nombre')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Servicio de Restaurante'
        verbose_name_plural = 'Servicios de Restaurantes'
        ordering = ['title']
        permissions = (
            ('show_restaurantservice', 'Can Details Service Restaurant'),
            ('index_restaurantservice', 'Can List Service Restaurant'),
        )


class Restaurant(models.Model):
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Localizacion')
    title = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
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
        permissions = (
            ('show_restaurant', 'Can Details Restaurant'),
            ('index_restaurant', 'Can List Restaurant'),
        )


class RestaurantSchedule(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Restaurant')
    day = models.CharField(max_length=2, choices=DAYS, unique=True, default='1', verbose_name='Dia')
    schedule = models.CharField(max_length=50, default='NA', verbose_name='Horario')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'Horario de Atencion de Restaurant'
        verbose_name_plural = 'Horarios de Atencion de Restaurantes'
        ordering = ['register_at']
        permissions = (
            ('show_restaurantschedule', 'Can Details Schedule Restaurant'),
            ('index_restaurantschedule', 'Can List Schedule Restaurant'),
        )


class RestaurantMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Restaurant')
    title = models.CharField(max_length=150, default='NA', verbose_name='Nombre')
    category = models.CharField(max_length=2, choices=MENU, default='1', verbose_name='Categoria')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=5.1, verbose_name='Precio')
    description = models.TextField(verbose_name='Descripcion', blank=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Menu de Restaurante'
        verbose_name_plural = 'Menus de Restaurantes'
        ordering = ['price']
        permissions = (
            ('show_restaurantmeu', 'Can Details Menu Restaurant'),
            ('index_restaurantmenu', 'Can List Menu Restaurant'),
        )


class Transport(models.Model):
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Localizacion')
    title = models.CharField(max_length=150, verbose_name='Nombre')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
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
        verbose_name = 'Transporte'
        verbose_name_plural = 'Transportes'
        ordering = ['score']
        permissions = (
            ('show_transport', 'Can Details Transport'),
            ('index_transport', 'Can List Transport'),
        )


class TransportDestination(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, verbose_name='Transporte')
    title = models.CharField(max_length=150, default='NA', verbose_name='Nombre')
    schedules_out = models.CharField(max_length=150, default='NA', verbose_name='Horarios de salida', blank=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Destino de Transporte'
        verbose_name_plural = 'Destinos de Transportes'
        ordering = ['title']
        permissions = (
            ('show_transportdestination', 'Can Details Destination Transport'),
            ('index_transportdestination', 'Can List Destination Transport'),
        )


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
        permissions = (
            ('show_transportservice', 'Can Details Service Transport'),
            ('index_transportservice', 'Can List Service Transport'),
        )


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
        permissions = (
            ('show_transporttypeservice', 'Can Details Type Service Transport'),
            ('index_transporttypeservice', 'Can List Type Service Transport'),
        )


class TransportSchedule(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, verbose_name='Transporte')
    day = models.CharField(max_length=2, choices=DAYS, unique=True, default='1', verbose_name='Dia')
    schedule = models.CharField(max_length=50, default='NA', verbose_name='Horario')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'Horario de Atencion de Transporte'
        verbose_name_plural = 'Horarios de Atencion de Transportes'
        ordering = ['register_at']
        permissions = (
            ('show_transportschedule', 'Can Details Schedule Transport'),
            ('index_transportschedule', 'Can List Schedule Transport'),
        )


class LodgingType(models.Model):
    title = models.CharField(max_length=150, verbose_name='Nombre')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tipo de Hospedaje'
        verbose_name_plural = 'Tipos de Hospedajes'
        ordering = ['title']
        permissions = (
            ('show_lodgingtype', 'Can Details Type Lodging'),
            ('index_lodgingtype', 'Can List Type Lodging'),
        )


class LodgingService(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Nombre')
    image = models.ImageField(upload_to='media/', null='true', verbose_name='Imagen')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Servicio de Hospedaje'
        verbose_name_plural = 'Servicios de Hospedajes'
        ordering = ['title']
        permissions = (
            ('show_lodgingservice', 'Can Details Service Lodging'),
            ('index_lodgingservice', 'Can List Service Lodging'),
        )


class Lodging(models.Model):
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Localizacion')
    type = models.ForeignKey(LodgingType, on_delete=models.CASCADE, verbose_name='Tipo')
    title = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
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
        permissions = (
            ('show_lodging', 'Can Details Lodging'),
            ('index_lodging', 'Can List Lodging'),
        )


class LodgingRoom(models.Model):
    lodging = models.ForeignKey(Lodging, on_delete=models.CASCADE, verbose_name='Tipo')
    title = models.CharField(max_length=150, default='NA', verbose_name='Nombre')
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
        permissions = (
            ('show_lodgingroom', 'Can Details Room Lodging'),
            ('index_lodgingroom', 'Can List Room Lodging'),
        )


class LodgingSchedule(models.Model):
    lodging = models.ForeignKey(Lodging, on_delete=models.CASCADE, verbose_name='Hospedaje')
    day = models.CharField(max_length=2, choices=DAYS, unique=True, default='1', verbose_name='Dia')
    schedule = models.CharField(max_length=50, default='7:00 - 23:00', verbose_name='Horario')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'Horario de Atencion de Hospedaje'
        verbose_name_plural = 'Horarios de Atencion de Hospedajes'
        ordering = ['register_at']
        permissions = (
            ('show_lodgingschedule', 'Can Details Schedule Lodging'),
            ('index_lodgingschedule', 'Can List Schedule Lodging'),
        )


class TourismSiteType(models.Model):
    title = models.CharField(max_length=150, verbose_name='Nombre')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tipo de Sitio Turistico'
        verbose_name_plural = 'Tipos de Sitios Turisticos'
        ordering = ['title']
        permissions = (
            ('show_tourismsitetype', 'Can Details Type Tourism Site'),
            ('index_tourismsitetype', 'Can List Type Tourism Site'),
        )


class TourismSiteService(models.Model):
    title = models.CharField(max_length=150, default='NA', verbose_name='Item de servicio')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Servicio de Sitio Turistico'
        verbose_name_plural = 'Servicios  de Sitios Turisticos'
        ordering = ['title']
        permissions = (
            ('show_tourismsiteservice', 'Can Details Service Tourism Site'),
            ('index_tourismsiteservice', 'Can List Service Tourism Site'),
        )


class TourismSite(models.Model):
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Localizacion')
    type = models.ForeignKey(TourismSiteType, on_delete=models.CASCADE, verbose_name='Tipo')
    service = models.ManyToManyField(TourismSiteService, verbose_name='Servicios', null=True, blank=True)
    title = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
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
        permissions = (
            ('show_tourismsite', 'Can Details Tourism Site'),
            ('index_tourismsite', 'Can List Tourism Site'),
        )


class TourismSiteMenu(models.Model):
    site = models.ForeignKey(TourismSite, on_delete=models.CASCADE, verbose_name='Sitio Turistico')
    title = models.CharField(max_length=150, default='NA', verbose_name='Nombre')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion', blank=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Menu de Sitio Turistico'
        verbose_name_plural = 'Menu  de Sitios Turisticos'
        ordering = ['title']
        permissions = (
            ('show_tourismsitemenu', 'Can Details Menu Tourism Site'),
            ('index_tourismsitemenu', 'Can List Menu Tourism Site'),
        )


class TourismSiteSchedule(models.Model):
    site = models.ForeignKey(TourismSite, on_delete=models.CASCADE, verbose_name='Sitio Turistico')
    day = models.CharField(max_length=2, choices=DAYS, unique=True, default='1', verbose_name='Dia')
    schedule = models.CharField(max_length=50, default='NA', verbose_name='Horario')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'Horario de Atencion de Sitio Turistico'
        verbose_name_plural = 'Horarios de Atencion de Sitios Turisticos'
        ordering = ['register_at']
        permissions = (
            ('show_tourismsiteschedule', 'Can Details Schedule Tourism Site'),
            ('index_tourismsiteschedule', 'Can List Schedule Tourism Site'),
        )


class TourismRoute(models.Model):
    destination = models.ForeignKey(Location, on_delete=models.CASCADE,verbose_name='Localizacion')
    title = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
    lat_origin = models.CharField(max_length=50, verbose_name='Latitud de Origen')
    lng_origin = models.CharField(max_length=50, verbose_name='Longitud de Origen')
    lat_destination = models.CharField(max_length=50, verbose_name='Latitud de Destino')
    lng_destination = models.CharField(max_length=50, verbose_name='Longitud de Destino')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(verbose_name='Descripcion', blank=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Calificacion', blank=True)
    date = models.DateField(verbose_name='Fecha de Evento', blank=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ruta turistica'
        verbose_name_plural = 'Rutas turisticas'
        ordering = ['score']
        permissions = (
            ('show_tourismroute', 'Can Details Service Tourism Route'),
            ('index_tourismroute', 'Can List Service Tourism Route'),
        )


class TourismRouteMenu(models.Model):
    route = models.ForeignKey(TourismRoute, on_delete=models.CASCADE, verbose_name='Ruta Turistica')
    title = models.CharField(max_length=150, default='NA', verbose_name='Nombre')
    image = models.ImageField(upload_to='media/', verbose_name='Imagen')
    description = models.TextField(default='NA', verbose_name='Descripcion', blank=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Menu de Ruta Turistica'
        verbose_name_plural = 'Menu  de Rutas Turisticas'
        ordering = ['title']
        permissions = (
            ('show_tourismroutemenu', 'Can Details Tourism Route Menu'),
            ('index_tourismroutemenu', 'Can List Tourism Route Menu'),
        )


class Objective(models.Model):
    description = models.TextField(verbose_name='Descripcion', unique=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Objetivo'
        verbose_name_plural = 'Objetivos'
        ordering = ['description']
        permissions = (
            ('show_objective', 'Can Details Objective'),
            ('index_objective', 'Can List Objective'),
        )


class Function(models.Model):
    description = models.TextField(verbose_name='Descripcion', unique=True)
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Funcion'
        verbose_name_plural = 'Funciones'
        ordering = ['description']
        permissions = (
            ('show_fucntion', 'Can Details Function'),
            ('index_function', 'Can List Function'),
        )


class Law(models.Model):
    title = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripcion', unique=True, blank=True, )
    file = models.FileField(upload_to='documents/%Y/%m/%d', null=True, verbose_name='Archivo pdf')
    register_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['title']
        permissions = (
            ('show_law', 'Can Details Law'),
            ('index_law', 'Can List Law'),
        )


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
        permissions = (
            ('show_client', 'Can Details Client'),
            ('index_client', 'Can List Client'),
        )
