from django.shortcuts import render

from .models import Profile, Status


def index(request):
    status = Status.get()
    active_profile = status.active_profile
    isOn = False if active_profile is None else active_profile.ap.is_running() 

    if request.method == 'POST':
        if isOn:
            isOn = not active_profile.ap.stop()
            status.changeActiveProfile(None)
            status.save()
        else:
            selected_profile = Profile.objects.filter(name=request.POST.dict()['profile']).first()
            active_profile = selected_profile
            status.changeActiveProfile(active_profile)
            isOn = active_profile.ap.start()

    submitText = 'Off' if isOn else 'On'
    profiles = list(Profile.objects.values_list('name', flat=True))
  
    context = {
        'isOn': isOn, 
        'profiles': profiles, 
        'submitText': submitText, 
        'activeProfile': '' if active_profile is None else active_profile.name
    }
    
    return render(request, 'index.html', context)