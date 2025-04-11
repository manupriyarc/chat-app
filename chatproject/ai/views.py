# ai/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AIChat, AIChatMessage
from django.http import JsonResponse
from transformers import pipeline
import threading
import time

# Load the AI model (cache it to avoid reloading)
chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

@login_required
def ai_chat(request):
    # Get or create AI chat for the user
    chat, created = AIChat.objects.get_or_create(user=request.user)
    messages = chat.messages.all().order_by('timestamp')[:50]
    
    return render(request, 'ai/chat.html', {
        'chat': chat,
        'messages': messages
    })

@login_required
def send_ai_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        chat_id = request.POST.get('chat_id')
        
        chat = get_object_or_404(AIChat, id=chat_id, user=request.user)
        
        # Save user message
        user_message = AIChatMessage.objects.create(
            chat=chat,
            message=message,
            is_user=True
        )
        
        # Start a thread to generate AI response (to avoid blocking)
        threading.Thread(target=generate_ai_response, args=(chat, message)).start()
        
        return JsonResponse({
            'success': True,
            'message_id': user_message.id
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def generate_ai_response(chat, user_message):
    # Simulate thinking time
    time.sleep(1)
    
    # Generate AI response
    response = chatbot(user_message)[0]['generated_text']
    
    # Save AI response
    AIChatMessage.objects.create(
        chat=chat,
        message=response,
        is_user=False
    )