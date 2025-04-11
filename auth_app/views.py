from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from supabase import create_client, Client
from .models import SupabaseUser
import os

# Initialize Supabase client
SUPABASE_URL = "https://ljmzjgzbzvlhxeuwktpu.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxqbXpqZ3pienZsaHhldXdrdHB1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQxOTYwMDUsImV4cCI6MjA1OTc3MjAwNX0.G3UxJDCwtPHDIzD-OpMqptlCwnKI9YsrCfvPJuL0WyI"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'auth/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'auth/register.html')
        
        try:
            # Create user in Supabase
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
            
            if response.user:
                # Create Django user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                
                # Create SupabaseUser profile
                SupabaseUser.objects.create(
                    user=user,
                    supabase_uid=response.user.id
                )
                
                # Log the user in
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Registration failed')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'auth/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Authenticate with Supabase
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })
            
            if response.user:
                # Find the Django user associated with this Supabase user
                try:
                    supabase_user = SupabaseUser.objects.get(supabase_uid=response.user.id)
                    user = supabase_user.user
                    
                    # Log the user in
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('dashboard')
                except SupabaseUser.DoesNotExist:
                    messages.error(request, 'User not found in the system')
            else:
                messages.error(request, 'Invalid credentials')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    # Sign out from Supabase
    supabase.auth.sign_out()
    
    # Sign out from Django
    logout(request)
    
    messages.success(request, 'Logged out successfully')
    return redirect('login')