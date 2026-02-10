from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import PhotoForm

from django.contrib.auth.decorators import login_required
from .models import Photo
from .models import Profile
from django import forms
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages


class MyPasswordChangeView(PasswordChangeView):
    template_name = "password_change.html"  
    success_url = reverse_lazy("profile")  

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully!")
        return super().form_valid(form)
    

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("home")  # we’ll define this later

    return render(request, "register.html")

def home(request):
    tag = request.GET.get("tag")

    photos = Photo.objects.all()

    if tag:
        photos = photos.filter(tags__icontains=tag)

    photos = photos.order_by("-created_at")

    return render(request, "home.html", {"photos": photos, "tag": tag})
# View for photo detail and like/unlike functionality
def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    is_liked = False
    if request.user.is_authenticated:
        is_liked = photo.liked_by.filter(id=request.user.id).exists()

    return render(
        request,
        "photo_detail.html",
        {
            "photo": photo,
            "is_liked": is_liked
        }
    )

# View to toggle like/unlike
@login_required
def toggle_like(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if photo.liked_by.filter(id=request.user.id).exists():
        photo.liked_by.remove(request.user)
    else:
        photo.liked_by.add(request.user)

    return redirect("photo_detail", photo_id=photo.id)

@login_required
def upload_photo(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.save()
            return redirect("home")
    else:
        form = PhotoForm()

    return render(request, "upload_photo.html", {"form": form})

@login_required
def profile_view(request):
    profile = request.user.profile
    if 'password' in request.GET:
        messages.success(request, "Password changed successfully!")
    return render(request, "profile.html", {"profile": profile})

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile_edit.html", {"form": form})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_pic"]