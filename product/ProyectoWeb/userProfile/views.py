from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileForm


@login_required
def detalle_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user) 
            return redirect('detalle_profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'userProfile/detalle_profile.html', {'form': form, 'user': user})
