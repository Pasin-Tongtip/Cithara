import json
import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from io import BytesIO
from pydub import AudioSegment
from .forms import SongForm
from .generators import SongGenerationRequest, MockSongGeneratorStrategy, SunoSongGeneratorStrategy
from .models import GoogleAccount, SongCreator, Library, Song

GOOGLE_CLIENT_ID = "1088900671763-5r9derdbne2q2nvab6psh24go0tlljph.apps.googleusercontent.com"

def login_view(request):
    if request.method == 'GET' and 'next' in request.GET:
        request.session['saved_next_url'] = request.GET.get('next')

    if request.method == 'POST':
        token = request.POST.get('credential')
        manual_email = request.POST.get('email')
        
        email_to_use = None
        first_name = None

        if token:
            try:
                idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
                email_to_use = idinfo['email']
                first_name = idinfo.get('given_name', email_to_use.split('@')[0])
            except ValueError:
                return render(request, 'cithara_app/login.html', {"error": "Google authentication failed."})
                
        elif manual_email:
            email_to_use = manual_email
            first_name = manual_email.split('@')[0]
            
        else:
            return render(request, 'cithara_app/login.html', {"error": "Please provide an email or use Google."})

        google_acc, account_created = GoogleAccount.objects.get_or_create(email=email_to_use)
        
        if account_created:
            creator = SongCreator.objects.create(google_account=google_acc, name=first_name)
            Library.objects.create(owner=creator)
        else:
            creator = SongCreator.objects.get(google_account=google_acc)

        request.session['creator_id'] = creator.id

        next_url = request.session.pop('saved_next_url', None)
        
        if next_url:
            return redirect(next_url)
        else:
            return redirect('library')

    return render(request, 'cithara_app/login.html')


def library_view(request):
    creator_id = request.session.get('creator_id')
    
    if not creator_id:
        return redirect('login')
        
    try:
        user_library = Library.objects.get(owner__id=creator_id)
        user_songs = Song.objects.filter(library=user_library)
    except Library.DoesNotExist:
        user_songs = []
        
    return render(request, 'cithara_app/library.html', {'songs': user_songs})


def custom_logout(request):
    request.session.flush()
    return redirect('login')


# --- Placeholders to stop the HTML from crashing ---
def dummy_view(request, song_id=None):
    from django.http import HttpResponse
    return HttpResponse("This page is under construction!")


def create_song(request):
    creator_id = request.session.get('creator_id')
    if not creator_id:
        return redirect('login')

    if request.method == 'POST':
        user_library = get_object_or_404(Library, owner__id=creator_id)
        
        new_song = Song.objects.create(
            library=user_library,
            title=request.POST.get('title'),
            occasion=request.POST.get('occasion'),
            genre=request.POST.get('genre'),
            voice_type=request.POST.get('voice_type'),
            mood=request.POST.get('mood'),
            story=request.POST.get('story'),
            suno_status='DRAFT'
        )
        
        return redirect('review_song', song_id=new_song.id)

    context = {
        'occasion_choices': Song._meta.get_field('occasion').choices,
        'genre_choices': Song._meta.get_field('genre').choices,
        'voice_type_choices': Song._meta.get_field('voice_type').choices,
        'mood_choices': Song._meta.get_field('mood').choices,
    }
    
    return render(request, 'cithara_app/create_song.html', context)


def review_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    creator_id = request.session.get('creator_id')
    if not creator_id:
        return redirect('login')

    if request.method == 'POST':
        tags = f"{song.genre}, {song.mood}, {song.voice_type} voice"
        gen_request = SongGenerationRequest(
            title=song.title, 
            tags=tags, 
            prompt=song.story
        )
        
        if getattr(settings, 'USE_MOCK_GENERATOR', True):
            generator = MockSongGeneratorStrategy()
        else:
            generator = SunoSongGeneratorStrategy(api_key=settings.SUNO_API_KEY)
            
        result = generator.generate(gen_request)

        song.suno_task_id = result.task_id
        song.suno_status = result.status
        song.save()
        
        if 'song_draft' in request.session:
            del request.session['song_draft']
            
        return redirect('library')

    return render(request, 'cithara_app/review_song.html', {'song': song})


def check_song_status(request, song_id):
    """Called by Javascript to check if a song is done generating."""
    try:
        song = Song.objects.get(id=song_id)
        
        if song.suno_status in ['SUCCESS', 'FAILED', 'TEXT_SUCCESS', 'FIRST_SUCCESS']:
            return JsonResponse({'status': song.suno_status, 'audio_url': song.audio_url})
            
        if getattr(settings, 'USE_MOCK_GENERATOR', True):
            generator = MockSongGeneratorStrategy()
        else:
            generator = SunoSongGeneratorStrategy(api_key=settings.SUNO_API_KEY)
            
        result = generator.check_status(song.suno_task_id)
        
        if result.status != song.suno_status:
            song.suno_status = result.status
            if result.audio_url:
                song.audio_url = result.audio_url
            song.save()
            
        return JsonResponse({'status': song.suno_status, 'audio_url': song.audio_url})
    except Song.DoesNotExist:
        return JsonResponse({'error': 'Song not found'}, status=404)


def share_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    creator_id = request.session.get('creator_id')
    if not creator_id:
        login_url = reverse('login')
        share_url = reverse('share_song', args=[song.id])
        
        return redirect(f"{login_url}?next={share_url}")

    return render(request, 'cithara_app/shared_song.html', {'song': song})


def delete_song(request, song_id):
    """Deletes a song from the database when the user confirms."""
    if request.method == 'POST':
        song = get_object_or_404(Song, id=song_id)
        song.delete()
    
    return redirect('library')

def edit_song(request, song_id):
    """Loads the edit page with existing data, and saves changes on submit."""
    song = get_object_or_404(Song, id=song_id)
    
    if request.method == 'POST':
        song.title = request.POST.get('title')
        song.occasion = request.POST.get('occasion')
        song.genre = request.POST.get('genre')
        song.voice_type = request.POST.get('voice_type')
        song.mood = request.POST.get('mood')
        song.story = request.POST.get('story')
        
        song.save()
        return redirect('review_song', song_id=song.id)
        
    context = {
        'song': song,
        'occasion_choices': Song._meta.get_field('occasion').choices,
        'genre_choices': Song._meta.get_field('genre').choices,
        'voice_type_choices': Song._meta.get_field('voice_type').choices,
        'mood_choices': Song._meta.get_field('mood').choices,
    }
    
    return render(request, 'cithara_app/edit_song.html', context)


def download_song(request, song_id, format='mp3'):
    """Fetches the audio and downloads it as either MP3 or M4A."""
    song = get_object_or_404(Song, id=song_id)
    
    if not song.audio_url:
        return redirect('library')

    try:
        r = requests.get(song.audio_url, stream=True)
        r.raise_for_status()
        
        safe_title = "".join(x for x in song.title if x.isalnum() or x in " -_").strip()
        if not safe_title:
            safe_title = f"cithara_song_{song.id}"

        if format == 'm4a':
            audio_data = BytesIO(r.content)
            
            audio = AudioSegment.from_file(audio_data)
            
            output_buffer = BytesIO()
            
            audio.export(output_buffer, format="ipod")
            output_buffer.seek(0)
            
            response = HttpResponse(output_buffer, content_type='audio/mp4')
            response['Content-Disposition'] = f'attachment; filename="{safe_title}.m4a"'
            return response
            
        else:
            response = StreamingHttpResponse(r.iter_content(chunk_size=8192), content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{safe_title}.mp3"'
            return response
            
    except Exception as e:
        print(f"Download Error: {e}")
        return redirect('library')


def generate_song_api(request, song_id):
    if request.method == 'POST':
        song = get_object_or_404(Song, id=song_id)
        
        raw_prompt = (
            f"Style: {song.genre}, {song.mood}. "
            f"Vocals: {song.voice_type}. "
            f"Topic: {song.story}"
        )
        master_prompt = raw_prompt[:500] 
        
        url = "https://api.sunoapi.org/api/v1/generate"
        headers = {
            "Authorization": f"Bearer {settings.SUNO_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": master_prompt,
            "model": "V4_5ALL", 
            "customMode": False,
            "instrumental": False,
            "callBackUrl": "https://yourdomain.com/callback"
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            
            print(f"SUNO DEBUG: {response.status_code} - {response_data}")

            if response.status_code == 200 and response_data.get('code') == 200:
                task_id = response_data['data']['taskId']
                song.suno_task_id = task_id
                song.save()
                return JsonResponse({'status': 'success', 'task_id': task_id})
            else:
                error_msg = response_data.get('msg', 'Suno API rejected the request.')
                return JsonResponse({'status': 'error', 'message': error_msg})
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'invalid_method'})


def check_suno_status(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    
    if not song.suno_task_id:
        return JsonResponse({'status': 'error', 'message': 'No task ID found.'})
        
    url = f"https://api.sunoapi.org/api/v1/feed/{song.suno_task_id}"
    headers = {"Authorization": f"Bearer {settings.SUNO_API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return JsonResponse({'status': 'generating'}) 

        response_data = response.json()
        
        if response_data.get('code') == 200:
            clips = response_data.get('data', [])
            
            if clips and clips[0].get('status') == 'complete':
                song.audio_url = clips[0].get('audio_url')
                song.lyrics = clips[0].get('lyric', '')
                song.save()
                return JsonResponse({'status': 'completed'})
            else:
                return JsonResponse({'status': 'generating'})
        else:
            return JsonResponse({'status': 'generating'})
            
    except Exception as e:
        return JsonResponse({'status': 'generating'})

