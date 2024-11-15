from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def detalle_profile(request, id):
    return render(request, 'userProfile/detalle_profile.html', {'uid': id})
