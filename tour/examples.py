# SERVICIOS DE RESTAURANTES
@permission_required('tour.index_restaurantservice', login_url='/accounts/login/')
def restaurant_service_index_admin(request):
    services_list = RestaurantService.objects.all()
    query = request.GET.get('q')
    if query:
        services_list = services_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(services_list, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    services = paginator.get_page(page)
    return render(request, 'admin_page/restaurants/services/index.html', {
        'services': services,
        'service_obj': RestaurantService,
    })

# SERVICIO DE TRANSPORTES
@permission_required('tour.index_transportservice', login_url='/accounts/login/')
def transport_service_index_admin(request):
    services_list = TransportService.objects.all()
    query = request.GET.get('q')
    if query:
        services_list = services_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(services_list, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    services = paginator.get_page(page)
    return render(request, 'admin_page/transports/services/index.html', {
        'services': services,
        'service_obj': TransportService,
    })


