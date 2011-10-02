from events.models import Event, Attendance
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from events.forms import EventForm
from dateutil.parser import parse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

def tonight(request):
    events = Event.objects.today().filter(latest=True)
    attending = []
    for event in events:
        try:
            Attendance.objects.get(event=event, user=request.user)
            attending.append(True)
        except Attendance.DoesNotExist:
            attending.append(False)
    context = {
        'events' : zip(events, attending),
    }
    return render_to_response(
        'events/tonight.html',
        context,
        context_instance = RequestContext(request),
    )

@login_required()
def create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        event = form.save(commit=False)
        event.creator = request.user
        guessed_date = None
        for word in event.description.split():
            try:
                guessed_date = parse(word)
                break
            except ValueError:
                continue
        event.start_date = guessed_date
        event.save()
        request.user.message_set.create(message='event posted')
        if 'next' in request.POST:
            next = request.POST['next']
        else:
            next = reverse('ev_tonight')
        return HttpResponseRedirect(next)
    
    return render_to_response(
        'events/create.html',
        {'form' : form},
        context_instance = RequestContext(request),
    )
#create = login_required(create)

@login_required()
def toggle_attendance(request):
    try:
        event_id = int(request.POST['event_id'])
    except (KeyError, ValueError):
        raise Http404
    event = get_object_or_404(Event, id=event_id)
    attendance, created = Attendance.objects.get_or_create(user = request.user, event = event)

    if created:
        request.user.message_set.create(message = 'You are now attending "%s"' % event)
    else:
        attendance.delete()
        request.user.message_set.create(message = 'You are no longer attending "%s"' % event)
    next = request.POST.get('next','')
    if not next:
        next = reverse('ev_tonight')
    return HttpResponseRedirect(next)