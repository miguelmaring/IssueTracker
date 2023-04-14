from django.shortcuts import render, redirect
from django.contrib import messages

from users.forms import UserForm


# Create your views here.
def profile_view(request):
    context = {}
    context['issues'] = request.user.issues_watched.all()
    context['logs'] = request.user.logs.all()
    return render(request, 'profile_view.html', context)

def edit_profile_view(request):
    context = {}
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User actualizado con éxito')

            return redirect('view_profile')  # O redirige a la vista deseada
        else:
            context['profile_form'] = form
    else:
        form = UserForm(instance=request.user)
        context['profile_form'] = form
    return render(request, 'edit_profile.html', context)