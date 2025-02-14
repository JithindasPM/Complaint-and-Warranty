"""
URL configuration for clamie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import LoginView,RegisterView,CustomerDashboardView,ShopOwnerDashboardView,SubmitComplaintView,SubmitWarrantyClaimView,UpdateComplaintStatusView,UpdateWarrantyClaimStatusView,ShopOwnerClaimDeleteView,LogoutView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),  # Add this line to include the Django admin interface
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('customer_dashboard/', CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('shop_owner_dashboard/', ShopOwnerDashboardView.as_view(), name='shop_owner_dashboard'),
    path('submit_complaint/', SubmitComplaintView.as_view(), name='submit_complaint'),
    path('submit_warranty_claim/', SubmitWarrantyClaimView.as_view(), name='submit_warranty_claim'),

    path('shop_owner_dashboard/', ShopOwnerDashboardView.as_view(), name='shop_owner_dashboard'),
    path('update_complaint_status/<int:pk>/', UpdateComplaintStatusView.as_view(), name='update_complaint_status'),
    path('update_warranty_claim_status/<int:pk>/', UpdateWarrantyClaimStatusView.as_view(), name='update_warranty_claim_status'),
    path("delete/<str:claim_type>/<int:claim_id>/", ShopOwnerClaimDeleteView.as_view(), name="claim_delete"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



