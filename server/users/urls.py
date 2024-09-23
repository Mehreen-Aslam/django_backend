# # users/urls.py
# from django.urls import path
# from .views import UserSignupAPI, UserLoginAPI, UserProfileAPI, ForgotPasswordAPI, UpdateVerificationAPI

# urlpatterns = [
#     path('signup/', UserSignupAPI.as_view(), name='signup'),
#     path('login/', UserLoginAPI.as_view(), name='login'),
#     path('profile/', UserProfileAPI.as_view(), name='profile'),
#     path('forgot-password/', ForgotPasswordAPI.as_view(), name='forgot_password'),
#     path('update-verification/', UpdateVerificationAPI.as_view(), name='update_verification'),
# ]

# users/urls.py


from django.urls import path
from . import views
from .views import SignupView, LoginView, CreateSlider, GetSliderAll, GetSlider,JobController, SingleJobController, ClientPartner, SingleClientPartner,FAQView, SingleFAQView, send_otp, verify_otp

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('add-slider/', CreateSlider.as_view(), name='add_slider'),
    path('get-slider/', GetSliderAll.as_view(), name='get_slider_all'),
    path('get-slider/<str:id>/', GetSlider.as_view(), name='get_slider'),
    path('send-message/', views.new_contact_us, name='new_contact_us'),
    path('get-messages/', views.get_contact_all, name='get_contact_all'),
    path('get-message/<int:id>/', views.get_contact_us, name='get_contact_us'),
   path('blog/create-blog/', views.create_blog, name='create_blog'),
    path('blog/get-blog/', views.get_blog_all, name='get_blog_all'),
    path('blog/get-blog/<int:id>/', views.get_blog, name='get_blog'),
    path('jobs/', JobController.as_view(), name='post_get_jobs'),  # For both POST and GET all jobs
    path('jobs/<int:id>/', SingleJobController.as_view(), name='get_job'), 
    path('team/add-partner/', ClientPartner.as_view(), name='add_partner'),  # POST for adding new team member
    path('team/get-partners/', ClientPartner.as_view(), name='get_all_partners'),  # GET for all team members
    path('team/get-partner/<int:id>/', SingleClientPartner.as_view(), name='get_partner'),  # GET a single team member by ID
    path('post-faqs/', FAQView.as_view()),  # POST route for creating FAQ
    path('get-faqs/', FAQView.as_view()),   # GET route for fetching all FAQs
    path('get-faqs/<int:id>/', SingleFAQView.as_view()),  # 
     path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    
]


