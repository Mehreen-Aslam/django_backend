# from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import serializers
from .serializers import UserSerializer, LoginSerializer

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully",
                "token": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Serializer for Login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Check if user exists
        email = data.get("email", "")
        password = data.get("password", "")
        if not email or not password:
            raise serializers.ValidationError("Email and password are required")
        return data


# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            # Authenticate user
            user = authenticate(username=email, password=password)
            if user is not None:
                # User authenticated, generate tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful",
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                }, status=status.HTTP_200_OK)
            else:
                # Invalid credentials
                return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # If the data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # slider/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Slider
from .serializers import SliderSerializer

class CreateSlider(APIView):
    permission_classes = [AllowAny]  # Ensure this is correctly applied

    def post(self, request):
        image = request.data.get('image')
        if not image:
            return Response(
                {'status': 'failed', 'message': 'Image URL is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = SliderSerializer(data={'image': image})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': 'success', 'message': 'Image saved successfully'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'status': 'failed', 'message': 'Failed to save image'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetSliderAll(APIView):
    permission_classes = [AllowAny]  # Ensure this is correctly applied

    def get(self, request):
        sliders = Slider.objects.all()
        serializer = SliderSerializer(sliders, many=True)
        return Response(
            {'status': 'success', 'data': serializer.data},
            status=status.HTTP_200_OK
        )

class GetSlider(APIView):
    permission_classes = [AllowAny]  # Ensure this is correctly applied

    def get(self, request, id):
        # Validate MongoDB ObjectId
        if not Slider.objects.filter(id=id).exists():
            return Response(
                {'status': 'failed', 'message': 'Slider image not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        slider = get_object_or_404(Slider, id=id)
        serializer = SliderSerializer(slider)
        return Response(
            {'status': 'success', 'data': serializer.data},
            status=status.HTTP_200_OK
        )

#contct
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ContactUs
import json

@csrf_exempt
def new_contact_us(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name', '')
        country = data.get('country', '')
        email = data.get('email', '')
        phoneno = data.get('phoneno', '')
        message = data.get('message', '')

        # Validation checks for required fields
        if not all([name, country, email, phoneno, message]):
            return JsonResponse({
                'status': 'failed',
                'message': 'All fields are required (name, country, email, phoneno, message)'
            }, status=400)

        try:
            new_message = ContactUs.objects.create(
                name=name,
                country=country,
                email=email,
                phoneno=phoneno,
                message=message
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Message saved successfully'
            }, status=201)

        except Exception as e:
            return JsonResponse({
                'status': 'failed',
                'message': 'Failed to save message'
            }, status=500)

@csrf_exempt
def get_contact_all(request):
    if request.method == 'GET':
        try:
            contactus_data = ContactUs.objects.all().values()
            return JsonResponse({
                'status': 'success',
                'data': list(contactus_data)
            }, status=200)
        except Exception as e:
            return JsonResponse({
                'status': 'failed',
                'message': 'Failed to get messages'
            }, status=500)

@csrf_exempt
def get_contact_us(request, id):
    if request.method == 'GET':
        try:
            contactus_data = ContactUs.objects.get(id=id)
            return JsonResponse({
                'status': 'success',
                'data': {
                    'id': contactus_data.id,
                    'name': contactus_data.name,
                    'country': contactus_data.country,
                    'email': contactus_data.email,
                    'phoneno': contactus_data.phoneno,
                    'message': contactus_data.message,
                    'created_at': contactus_data.created_at
                }
            }, status=200)
        except ContactUs.DoesNotExist:
            return JsonResponse({
                'status': 'failed',
                'message': 'Message not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'failed',
                'message': 'Failed to get message'
            }, status=500)

# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Blog
import json

# Create a new blog (POST request)
@csrf_exempt
def create_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            blog = Blog.objects.create(
                image=data.get('image'),
                heading=data.get('heading'),
                category=data.get('category'),
                writtenby=data.get('writtenby'),
                content=data.get('content')
            )
            return JsonResponse({"status": "success", "message": "Blog created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"status": "failed", "message": str(e)}, status=500)
    return JsonResponse({"status": "failed", "message": "Invalid request method"}, status=405)

# Get all blogs (GET request)
def get_blog_all(request):
    if request.method == 'GET':
        blogs = Blog.objects.all().values()
        return JsonResponse({"status": "success", "data": list(blogs)}, status=200)
    return JsonResponse({"status": "failed", "message": "Invalid request method"}, status=405)

# Get a single blog by ID (GET request)
def get_blog(request, id):
    try:
        blog = Blog.objects.filter(id=id).values().first()
        if blog:
            return JsonResponse({"status": "success", "data": blog}, status=200)
        return JsonResponse({"status": "failed", "message": "Blog not found"}, status=404)
    except Exception as e:
        return JsonResponse({"status": "failed", "message": str(e)}, status=500)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from .serializers import JobSerializer
from django.shortcuts import get_object_or_404

class JobController(APIView):
    
    # Create a new job
    def post(self, request):
        serializer = JobSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Job saved successfully'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'failed', 'message': 'Failed to save job'}, status=status.HTTP_400_BAD_REQUEST)

    # Get all jobs
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

class SingleJobController(APIView):
    
    # Get a job by ID
    def get(self, request, id):
        job = get_object_or_404(Job, id=id)
        serializer = JobSerializer(job)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)


from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Team
from .serializers import TeamSerializer
from django.shortcuts import get_object_or_404

class ClientPartner(APIView):
    permission_classes = [AllowAny]  # Allow public access without authentication

    # Create a new team member with image
    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Team member saved successfully'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'failed', 'message': 'Failed to save team member'}, status=status.HTTP_400_BAD_REQUEST)

    # Get all team members
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

class SingleClientPartner(APIView):
    permission_classes = [AllowAny]  # Allow public access without authentication

    # Get a single team member by ID
    def get(self, request, id):
        team = get_object_or_404(Team, id=id)
        serializer = TeamSerializer(team)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import FAQ
from .serializers import FAQSerializer

class FAQView(APIView):
    
    # Create a new FAQ
    def post(self, request):
        serializer = FAQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'FAQ saved successfully'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'failed', 'message': 'Failed to save FAQ'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get all FAQs
    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)


class SingleFAQView(APIView):
    
    # Get a single FAQ by ID
    def get(self, request, id):
        faq = get_object_or_404(FAQ, id=id)
        serializer = FAQSerializer(faq)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User

@api_view(['POST'])
def send_otp(request):
    email = request.data.get('email')
    # Use filter() and first() to avoid MultipleObjectsReturned
    user = User.objects.filter(email=email).first()  # Returns None if no user is found
    if user is None:
        return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

    otp = random.randint(1000, 9999)
    user.otp = otp
    user.save()

    # Send OTP via email
    send_mail(
        'Your OTP',
        f'Your OTP is {otp}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return Response({'message': 'OTP sent'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    
    user = User.objects.filter(email=email).first()  # Use first() to avoid exceptions
    if user is None:
        return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    if user.otp == otp:
        user.is_verified = True
        user.save()
        return Response({'message': 'OTP verified'}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
