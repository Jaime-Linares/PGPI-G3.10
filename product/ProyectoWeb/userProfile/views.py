from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout
from .forms import ProfileForm



@login_required
def detalle_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user) 
            return redirect('Home')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'userProfile/detalle_profile.html', {'form': form, 'user': user})


@login_required
def eliminar_cuenta(request):
    user = request.user
    user.delete() 
    logout(request)
    return redirect('Home')

