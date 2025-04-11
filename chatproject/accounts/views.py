# Create your views here.
# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in immediately after signup
            messages.success(request, 'Account created successfully!')
            return redirect('home')  # Make sure this matches your URL name
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

# accounts/views.py

from .utils import upload_profile_picture, delete_profile_picture
from django.core.files.storage import default_storage

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                # Delete old picture if it exists
                if request.user.profile_picture:
                    try:
                        if request.user.profile_picture.name.startswith('http'):
                            delete_profile_picture(request.user.profile_picture.url)
                        else:
                            default_storage.delete(request.user.profile_picture.name)
                    except:
                        pass
                
                # Upload new picture to Firebase
                file = request.FILES['profile_picture']
                picture_url = upload_profile_picture(request.user, file)
                request.user.profile_picture = picture_url
            
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})