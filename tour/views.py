from django.shortcuts import render
from tour.forms import EventForm
from tour.models import Event
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
        return render(request, 'tour/index.html', {})


def events_index(request):
    events = Event.objects.all
    return render(request, 'tour/events-index.html', {
        'events': events,
        'event_obj': Event
    })


def patients_new(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('events-show', kwargs={'id': event.id}))

        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = EventForm()
    return render(request, 'events/new.html', {
        'form': form,
    })


def events_edit(request, id):
    event = Event.objects.get(id=id)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('events-show', kwargs={'id': event.id}))
    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit.html', {
        'form': form,
        'event': event
    })


def events_show(request, id):
    event = Event.objects.get(id=id)

    return render(request, 'patients/show.html', {
        'event': event,
        'event_obj': Event,
    })


def events_delete(request, id):
    event = Event.objects.get(id=id)
    event.delete()
    is_exist = Event.objects.filter(id=id).exists()

    if is_exist:
        message = 'No se pudo eliminar'
        messages.add_message(request, messages.ERROR, message)
    else:
        message = 'Eliminado!'
        messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(events_index))


def  restaurant_index(request):
    events = Event.objects.all
    return render(request, 'tour/events-index.html', {
        'events': events,
        'event_obj': Event
    })

