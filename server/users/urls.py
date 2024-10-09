from django.urls import path
from . import views
from .views import (
    LoginView, CreateSlider, GetSliderAll, GetSlider, 
    JobController, SingleJobController, ClientPartner, 
    SingleClientPartner, FAQView, SingleFAQView,
    create_blog, get_all_blogs, user_registration, 
    verify_otp, get_user_profile, forget_password, 
    update_password
)

urlpatterns = [
    path('register/', user_registration, name='user_registration'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('add-slider/', CreateSlider.as_view(), name='add_slider'),
    path('get-slider/', GetSliderAll.as_view(), name='get_slider_all'),
    path('get-slider/<str:id>/', GetSlider.as_view(), name='get_slider'),
    path('send-message/', views.new_contact_us, name='new_contact_us'),
    path('get-messages/', views.get_contact_all, name='get_contact_all'),
    path('get-message/<int:id>/', views.get_contact_us, name='get_contact_us'),
    path('create-blog/', create_blog, name='create_blog'),  # For blog creation
    path('blogs/', get_all_blogs, name='get_all_blogs'),
    path('jobs/', JobController.as_view(), name='post_get_jobs'),  # For both POST and GET all jobs
    path('jobs/<int:id>/', SingleJobController.as_view(), name='get_job'),
    path('team/add-partner/', ClientPartner.as_view(), name='add_partner'),  # POST for adding new team member
    path('team/get-partners/', ClientPartner.as_view(), name='get_all_partners'),  # GET for all team members
    path('team/get-partner/<int:id>/', SingleClientPartner.as_view(), name='get_partner'),  # GET a single team member by ID
    path('post-faqs/', FAQView.as_view()),  # POST route for creating FAQ
    path('get-faqs/', FAQView.as_view()),   # GET route for fetching all FAQs
    path('get-faqs/<int:id>/', SingleFAQView.as_view()),  # GET a single FAQ by ID
    path('profile/', get_user_profile, name='get_user_profile'),  # GET user profile
    path('profile/<int:user_id>/', get_user_profile, name='get_user_profile_by_id'),  # GET user profile by ID
    path('forget-password/', forget_password, name='forget_password'),  # Forget password route
    path('update-password/', update_password, name='update_password'),  # Update password route
]
