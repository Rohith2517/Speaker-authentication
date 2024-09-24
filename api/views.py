# Remember to add a URL pattern for this view to test it via browser.
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import speechbrain as sb
from speechbrain.inference.speaker import SpeakerRecognition
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
import os
from django.conf import settings
from .models import Speaker  
from django.urls import reverse


def enroll_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        passed = request.POST.get('passed')
        if passed=='1234':
            if '..' in name or name.startswith('/'):
                return HttpResponse("Invalid file path.")
            base_path = settings.MEDIA_ROOT
            full_path = f'{base_path}/{name}.wav'
            Speaker.objects.create(name=name, file_path=full_path)
            record_audio(5,full_path)
            return HttpResponseRedirect(reverse('enroll-user-success'))
        else:
            return HttpResponse("Failed to enroll. Please provide both name and file path.")
    else:
        return render(request, 'api/enroll_user.html')
    
def enroll_user_success(request):
    return HttpResponse("Speaker successfully enrolled.")


def audio_verification(request,name):
    context = {'submitted': False}
    if request.method == 'GET':
        audio_file = 'C:/Users/Revanth/verification/output.wav'
        user_name = name
        if audio_file and user_name:
            try:
                model_directory = r"C:\Users\Revanth\speech\pretrained_models"
                verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir=model_directory)
                speaker = Speaker.objects.get(name=user_name)
                existing_file_path = speaker.file_path
                
                score, prediction = verification.verify_files(audio_file, existing_file_path)
                context.update({
                    'score': int(score * 100),
                    'prediction': prediction,
                    'submitted': True
                })
                if prediction.item():
                    return render(request, 'api/results.html', context) 
                else:
                    return redirect('failure_url') 
            except Speaker.DoesNotExist:
                return render(request, 'api/button_page.html', {'error': 'Speaker not found'})
        else:
            return render(request, 'api/button_page.html', {'error': 'Please provide both user name and audio file'})
    return render(request, 'api/results.html', context)


def button_page(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        return redirect('audio-verification', name=user_name)
    else:
        return render(request, 'api/button_page.html')

import subprocess

from django.http import JsonResponse, HttpResponse
from .utils import record_audio

def start_recording(request):
    if request.method == 'POST':
        try:
            record_audio(5,'output.wav')
            return redirect('button-page')
        except Exception as e: 
            return HttpResponse(f"Error: {str(e)}")
    else:
        return render(request, 'api/start_recording.html')


def failure_view(request):
    if request.method == 'GET':
        return render(request, 'api/failure_page.html')
    else:
        return redirect('enroll-user')
        password = request.POST.get('password')
        if password == '1234':
            return render(request, 'api/success_page.html')
        else:
            return HttpResponse('Unauthorized')

def success_view(request):
    if request.method == 'GET':
        return render(request, 'api/success_page.html', context)