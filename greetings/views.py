from django.shortcuts import render
from contact.models import Contact
from .models import VisitTracking, GameInteraction, DiyaLightTracking
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.http import HttpResponse

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_device_type(request):
    """Detect device type from user agent"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    
    if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
        return 'mobile'
    elif 'tablet' in user_agent or 'ipad' in user_agent:
        return 'tablet'
    else:
        return 'desktop'

def get_greeting_occasion():
    """Automatically detect event based on current date"""
    today = timezone.localtime(timezone.now())
    
    # Define event date ranges (you can customize these)
    # Format: (start_month, start_day, end_month, end_day, event_name)
    event_dates = [
        (10, 20, 10, 20, 'diwali'),      # Diwali: Oct 20 - Nov 5
        (10, 21, 11, 5, 'newyear'),      # New Year: Dec 25 - Jan 7
        (10, 28, 11, 3, 'bhaidooj'),    # Bhai Dooj: Oct 28 - Nov 3
    ]
    
    current_date = (today.month, today.day)
    
    for start_month, start_day, end_month, end_day, event in event_dates:
        if start_month == end_month:
            if current_date >= (start_month, start_day) and current_date <= (end_month, end_day):
                return event, today
        else:
            # Handle events that span across months
            if (current_date >= (start_month, start_day)) or (current_date <= (end_month, end_day)):
                return event, today
    
    # Default to diwali if no event matches
    return 'diwali', today

def date(request):
    """View to return current date and occasion"""
    occasion, today = get_greeting_occasion()
    return HttpResponse(f"Today's date is {today.strftime('%Y-%m-%d')}, Occasion: {occasion}")

def get_event_config(event_type, greeting_name=None):
    """Get event-specific configuration"""
    name = greeting_name or "Friend"
    
    configs = {
        'diwali': {
            'event': 'diwali',
            'title': f'Happy Diwali {name}! 🪔',
            'subtitle': 'Festival of Lights',
            'welcome_message': f'Wishing you a sparkling Diwali filled with joy, prosperity, and endless happiness!',
            'button_text': 'Light the Diyas ✨',
            'theme_color': '#ff6b35',
            'secondary_color': '#ffa500',
            'diyas_count': 7,
            'messages': [
                "May the divine light of Diwali spread peace, prosperity, and happiness in your life! 🪔",
                "Wishing you a bright and beautiful Diwali filled with love and laughter! ✨",
                "May this Diwali bring new smiles, unforgettable memories, and eternal happiness! 🎆",
                "Let's celebrate the victory of light over darkness. Happy Diwali! 🌟",
                "May the festival of lights illuminate your life with endless joy! 💫",
                "Wishing you and your family a blessed Diwali filled with warmth! ❤️",
                "May Goddess Lakshmi bless you with wealth and prosperity! 🙏"
            ]
        },
        'newyear': {
            'event': 'newyear',
            'title': f'Happy New Year {name}! 🎉',
            'subtitle': 'Welcome 2026',
            'welcome_message': f'Wishing you a fantastic New Year filled with new opportunities and wonderful moments!',
            'button_text': 'Celebrate with Fireworks 🎆',
            'theme_color': '#4ecdc4',
            'secondary_color': '#3498db',
            'messages': [
                "Cheers to a new year and another chance for us to get it right! 🥂",
                "May this year bring you success, happiness, and prosperity! 🌟",
                "New year, new beginnings, new opportunities! 🎊",
                "Wishing you 365 days of success and happiness! 🎉"
            ]
        },
        'bhaidooj': {
            'event': 'bhaidooj',
            'title': f'Happy Bhai Dooj {name}! 👫',
            'subtitle': 'Celebrating Sibling Bond',
            'welcome_message': f'Celebrating the beautiful bond between siblings with love and blessings!',
            'button_text': 'Collect Blessings 💖',
            'theme_color': '#ff6b9d',
            'secondary_color': '#e91e63',
            'messages': [
                "May the bond between siblings grow stronger with each passing day! ❤️",
                "Blessed Bhai Dooj to you and your siblings! 🙏",
                "Celebrating the precious bond of love and care! 💫",
                "May you always be there for each other! 👫"
            ]
        }
    }
    
    return configs.get(event_type, configs['diwali'])

def greet_contact(request, unique_id):
    """Main greeting view with personalized content"""
    occasion, today = get_greeting_occasion()
    contact = Contact.objects.filter(unique_id=unique_id).first()
    
    if contact is None:
        config = get_event_config(occasion)
        return render(request, 'greetings/landing_page.html', {
            'contact': None, 
            'occasion': occasion,
            'config': config
        })
    else:
        # Track visit
        VisitTracking.objects.create(
            contact=contact,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            device_type=get_device_type(request)
        )
        
        config = get_event_config(occasion, contact.greeting_name)
        return render(request, 'greetings/landing_page.html', {
            'contact': contact, 
            'occasion': occasion,
            'config': config
        })

def interactive_page(request, unique_id):
    """Interactive game page"""
    occasion, today = get_greeting_occasion()
    contact = Contact.objects.filter(unique_id=unique_id).first()
    
    if contact:
        config = get_event_config(occasion, contact.greeting_name)
        
        # Create game interaction tracking
        game_interaction = GameInteraction.objects.create(
            contact=contact,
            event_type=occasion,
            device_type=get_device_type(request),
            ip_address=get_client_ip(request),
            total_diyas=len(config.get('messages', []))
        )
        
        return render(request, 'greetings/interactive_page.html', {
            'contact': contact,
            'occasion': occasion,
            'config': config,
            'game_id': game_interaction.id
        })
    else:
        config = get_event_config(occasion)
        return render(request, 'greetings/interactive_page.html', {
            'contact': None,
            'occasion': occasion,
            'config': config,
            'game_id': None
        })


@csrf_exempt
def track_diya_light(request):
    """API endpoint to track diya lighting"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            game_id = data.get('game_id')
            diya_number = data.get('diya_number')
            time_from_start = data.get('time_from_start', 0)
            
            if game_id:
                game = GameInteraction.objects.get(id=game_id)
                game.diyas_lit = data.get('diyas_lit', game.diyas_lit)
                
                # Track individual diya
                DiyaLightTracking.objects.create(
                    game_interaction=game,
                    diya_number=diya_number,
                    time_from_start=time_from_start
                )
                
                # Check if completed
                if game.diyas_lit >= game.total_diyas:
                    game.is_completed = True
                    game.completed_at = timezone.now()
                    game.time_taken_seconds = int(time_from_start)
                    game.score = game.calculate_score()
                
                game.save()
                
                return JsonResponse({
                    'success': True,
                    'diyas_lit': game.diyas_lit,
                    'is_completed': game.is_completed,
                    'score': game.score
                })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@staff_member_required
def analytics_dashboard(request):
    """Analytics dashboard for tracking"""
    contacts = Contact.objects.all()
    
    # Gather statistics
    stats = {
        'total_contacts': contacts.count(),
        'total_visits': VisitTracking.objects.count(),
        'total_games_started': GameInteraction.objects.count(),
        'total_games_completed': GameInteraction.objects.filter(is_completed=True).count(),
        'unique_visitors': VisitTracking.objects.values('contact').distinct().count(),
    }
    
    # Recent activities
    recent_visits = VisitTracking.objects.select_related('contact')[:20]
    recent_games = GameInteraction.objects.select_related('contact')[:20]
    
    # Top performers
    top_scores = GameInteraction.objects.filter(is_completed=True).order_by('-score')[:10]
    
    # Device breakdown
    device_stats = VisitTracking.objects.values('device_type').annotate(
        count=models.Count('id')
    )
    
    context = {
        'stats': stats,
        'recent_visits': recent_visits,
        'recent_games': recent_games,
        'top_scores': top_scores,
        'device_stats': device_stats,
    }
    
    return render(request, 'greetings/analytics_dashboard.html', context)

def greet_contact_general(request):
    """General greeting without specific contact"""
    occasion, today = get_greeting_occasion()
    config = get_event_config(occasion)
    return render(request, 'greetings/landing_page.html', {
        'contact': None, 
        'occasion': occasion,
        'config': config
    })