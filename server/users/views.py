# from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Slider, ContactUs, Job, ForgetPassword, FAQ, Team, Blog
from .serializers import (
    UserSerializer, LoginSerializer, SliderSerializer, 
    JobSerializer, FAQSerializer, TeamSerializer, UserProfileSerializer
)

import json
import random
import smtplib

def generate_otp():
    """Generates a 4-digit OTP."""
    return str(random.randint(1000, 9999))



@csrf_exempt
def user_registration(request):
    """Handles user registration and OTP sending."""
    if request.method == 'POST':
        try:
            # Parse request data
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            username = data.get('username')  # Use 'username' consistently

            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'User already exists.'}, status=400)

            # Generate OTP
            otp = generate_otp()

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password, otp=otp)

            # Send OTP via email
            send_otp_email(email, otp)

            return JsonResponse({'status': 'success', 'message': 'User created successfully. OTP sent.'}, status=201)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def send_otp_email(email, otp):
    """Sends OTP via email."""
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(subject, message, from_email, [email])
    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")


@csrf_exempt
def verify_otp(request):
    """Verifies the OTP for a given user."""
    if request.method == 'POST':
        try:
            # Parse request data
            data = json.loads(request.body)
            email = data.get('email')
            otp = data.get('otp')

            # Find the user by email
            user = User.objects.get(email=email)

            # Check if the user is already verified
            if user.is_verified:
                return JsonResponse({'status': 'error', 'message': 'User already verified.'}, status=400)

            # Check if the OTP matches
            if user.otp == otp:
                user.is_verified = True
                user.save()
                return JsonResponse({'status': 'success', 'message': 'Account verified successfully!'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Incorrect OTP.'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


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


class CreateSlider(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        image = request.data.get('image')  # Get the image URL from the request data
        if not image:
            return Response(
                {'status': 'failed', 'message': 'Image URL is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = SliderSerializer(data={'image': image})  # Use the serializer to validate data
        if serializer.is_valid():
            serializer.save()  # Save the new slider instance
            return Response(
                {'status': 'success', 'message': 'Image saved successfully'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'status': 'failed', 'message': 'Failed to save image', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST  # Return validation errors
            )

class GetSliderAll(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def get(self, request):
        sliders = Slider.objects.all()  # Retrieve all slider objects
        serializer = SliderSerializer(sliders, many=True)  # Serialize the slider objects
        return Response(
            {'status': 'success', 'data': serializer.data},  # Return the serialized data
            status=status.HTTP_200_OK
        )

class GetSlider(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def get(self, request, id):
        slider = get_object_or_404(Slider, id=id)  # Get the slider or return 404 if not found
        serializer = SliderSerializer(slider)  # Serialize the slider object
        return Response(
            {'status': 'success', 'data': serializer.data},  # Return the serialized data
            status=status.HTTP_200_OK
        )

#contct

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

    return JsonResponse({
        'status': 'failed',
        'message': 'Invalid request method. Only POST is allowed.'
    }, status=405)  # Handle invalid request methods


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

    return JsonResponse({
        'status': 'failed',
        'message': 'Invalid request method. Only GET is allowed.'
    }, status=405)  # Handle invalid request methods


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

    return JsonResponse({
        'status': 'failed',
        'message': 'Invalid request method. Only GET is allowed.'
    }, status=405)  # Handle invalid request methods



# Create a new blog (POST request)
@csrf_exempt
def create_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Validate required fields
            required_fields = ['image', 'heading', 'category', 'writtenby', 'content']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"status": "failed", "message": f"{field} is required"}, status=400)
            
            # Create the blog entry
            blog = Blog.objects.create(
                image=data.get('image'),
                heading=data.get('heading'),
                category=data.get('category'),
                written_by=data.get('writtenby'),  # Corrected field name
                content=data.get('content')
            )
            return JsonResponse({"status": "success", "message": "Blog created successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "message": str(e)}, status=500)
    
    return JsonResponse({"status": "failed", "message": "Invalid request method"}, status=405)

# Get all blogs (GET request)
def get_all_blogs(request):
    if request.method == 'GET':
        blogs = Blog.objects.all().values()
        return JsonResponse({"status": "success", "data": list(blogs)}, status=200)
    
    return JsonResponse({"status": "failed", "message": "Invalid request method"}, status=405)




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


class ClientPartner(APIView):
    permission_classes = [AllowAny]  # Allow public access without authentication

    # Create a new team member with image
    def post(self, request):
        serializer = TeamSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Team member saved successfully'}, status=status.HTTP_201_CREATED)
        
        # Return detailed error messages
        return Response({
            'status': 'failed',
            'message': 'Failed to save team member',
            'errors': serializer.errors  # Include specific error messages
        }, status=status.HTTP_400_BAD_REQUEST)

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




@api_view(['GET'])
def get_user_profile(request):
    try:
        # Retrieve all user records
        users = User.objects.all()  # Fetch all users
        serializer = UserProfileSerializer(users, many=True)  # Serialize all user records
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Use  custom User model
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found with the provided email.'}, status=400)
        
        # Generate a 4-digit OTP and update or create an entry in ForgetPassword model
        otp = str(random.randint(1000, 9999))  # 4-digit OTP generation
        forget_password_instance, created = ForgetPassword.objects.get_or_create(email=email)
        forget_password_instance.otp = otp  # Set the OTP
        forget_password_instance.save()
        
        # Send OTP via email
        subject = 'OTP for Password Reset'
        message = f'Your OTP is {otp}.'
        try:
            send_mail(subject, message, 'admin@example.com', [email])
            return JsonResponse({'status': 'success', 'message': 'OTP sent successfully to your email.'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Failed to send OTP email.'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)



@csrf_exempt
def update_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        
        # Check if password and confirm password match
        if password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Password and Confirm Password don\'t match'}, status=422)
        
        try:
            # Use  custom User model to find the user by email
            user = User.objects.get(email=email)
            # Hash the new password
            user.password = make_password(password)
            user.save()
            return JsonResponse({'status': 'success', 'message': 'Password updated successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'No user found with email: {email}'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
