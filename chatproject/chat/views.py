# chat/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from accounts.models import CustomUser
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@login_required
def home(request):
    chat_rooms = request.user.chat_rooms.all()
    other_users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'chat/home.html', {
        'chat_rooms': chat_rooms,
        'other_users': other_users
    })

@login_required
def room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    messages = room.messages.all().order_by('timestamp')[:50]
    return render(request, 'chat/room.html', {
        'room': room,
        'messages': messages
    })

@login_required
@require_GET
def get_or_create_private_room(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)
    # Check if a private room already exists between these users
    existing_rooms = ChatRoom.objects.filter(is_group=False, participants=request.user).filter(participants=other_user)
    if existing_rooms.exists():
        room = existing_rooms.first()
    else:
        room = ChatRoom.objects.create(is_group=False)
        room.participants.add(request.user, other_user)
    return JsonResponse({'room_id': room.id})

def home(request):
    return render(request, 'home.html')