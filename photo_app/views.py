from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

from photo_app.models import Photo
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Photo

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
   photos = Photo.objects.all().order_by("-created_at")
   return render(request, "home.html", {"photos": photos})
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