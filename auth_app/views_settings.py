from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import UserProfile
from .forms import UserProfileForm, NotificationSettingsForm, CustomPasswordChangeForm
from products.models import UserPreference

@login_required
def settings_profile(request):
    """View for user profile settings"""
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('settings_profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    
    context = {
        'form': form,
        'profile': profile,
        'active_tab': 'profile'
    }
    
    return render(request, 'auth/settings/profile.html', context)

@login_required
def settings_appearance(request):
    """View for appearance settings"""
    # Get or create user preference
    preference, created = UserPreference.objects.get_or_create(user=request.user)
    
    context = {
        'preference': preference,
        'active_tab': 'appearance'
    }
    
    return render(request, 'auth/settings/appearance.html', context)

@login_required
@require_POST
def save_appearance_settings(request):
    """Save appearance settings"""
    try:
        data = json.loads(request.body)
        theme = data.get('theme')
        
        if theme not in ['light', 'dark']:
            return JsonResponse({'success': False, 'error': 'Invalid theme'})
        
        # Update or create user preference
        preference, created = UserPreference.objects.update_or_create(
            user=request.user,
            defaults={'theme': theme}
        )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def settings_notifications(request):
    """View for notification settings"""
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your notification settings have been updated successfully.')
            return redirect('settings_notifications')
    else:
        form = NotificationSettingsForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        'active_tab': 'notifications'
    }
    
    return render(request, 'auth/settings/notifications.html', context)

@login_required
def settings_security(request):
    """View for security settings (password change)"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('settings_security')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'active_tab': 'security'
    }
    
    return render(request, 'auth/settings/security.html', context)

@login_required
def send_test_email(request):
    """Send a test email to the user"""
    try:
        # Get user email
        email = request.user.email
        
        if not email:
            return JsonResponse({'success': False, 'error': 'No email address found for your account.'})
        
        # Import here to avoid circular imports
        from django.core.mail import send_mail
        from django.conf import settings
        
        # Send test email
        subject = 'Test Email from Inventory Management System'
        message = f'Hello {request.user.first_name or request.user.username},\n\nThis is a test email to confirm your notification settings are working correctly.\n\nRegards,\nInventory Management System'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        
        send_mail(subject, message, from_email, recipient_list)
        
        return JsonResponse({'success': True, 'message': f'Test email sent to {email}'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
