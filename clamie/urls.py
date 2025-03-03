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
from django.conf import settings
from django.conf.urls.static import static

from myapp.views import LoginView
from myapp.views import RegisterView
from myapp.views import CustomerDashboardView
from myapp.views import ShopOwnerDashboardView
from myapp.views import SubmitComplaintView
from myapp.views import SubmitWarrantyClaimView
from myapp.views import UpdateComplaintStatusView
from myapp.views import UpdateWarrantyClaimStatusView
from myapp.views import ShopOwnerClaimDeleteView
from myapp.views import LogoutView
from myapp.views import Home
from myapp.views import Complaint_View
from myapp.views import Warranty_View
from myapp.views import DeleteComplaintView
from myapp.views import DeleteWarrantyClaimView


urlpatterns = [
    path('admin/', admin.site.urls),  # Add this line to include the Django admin interface
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('customer_dashboard/', CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('shop_owner_dashboard/', ShopOwnerDashboardView.as_view(), name='shop_owner_dashboard'),
    path('submit_complaint/', SubmitComplaintView.as_view(), name='submit_complaint'),
    path('submit_warranty_claim/', SubmitWarrantyClaimView.as_view(), name='submit_warranty_claim'),
    path('update_complaint_status/<int:pk>/', UpdateComplaintStatusView.as_view(), name='update_complaint_status'),
    path('update_warranty_claim_status/<int:pk>/', UpdateWarrantyClaimStatusView.as_view(), name='update_warranty_claim_status'),
    path("delete/<str:claim_type>/<int:claim_id>/", ShopOwnerClaimDeleteView.as_view(), name="claim_delete"),
    path('', Home.as_view(), name='home'),
    path('complaints', Complaint_View.as_view(), name='complaints'),
    path('warranty', Warranty_View.as_view(), name='warranty'),
    path('delete_complaint/<int:pk>/', DeleteComplaintView.as_view(), name='delete_complaint'),
    path('warranty/delete/<int:pk>/', DeleteWarrantyClaimView.as_view(), name='delete_warranty_claim'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# Client ID: ec41569ae51041eab575322a7f1ed4d7 Client Secret: 00b013e862b0441e9e32cd894e2a04ce

# eyJhbGciOiJSUzI1NiIsImtpZCI6IjEwOEFEREZGRjZBNDkxOUFBNDE4QkREQTYwMDcwQzE5NzNDRjMzMUUiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJFSXJkX19ha2tacWtHTDNhWUFjTUdYUFBNeDQifQ.eyJuYmYiOjE3NDA0ODkxODksImV4cCI6MTc0MDU3NTU4OSwiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mYXRzZWNyZXQuY29tIiwiYXVkIjoiYmFzaWMiLCJjbGllbnRfaWQiOiJlYzQxNTY5YWU1MTA0MWVhYjU3NTMyMmE3ZjFlZDRkNyIsInNjb3BlIjpbImJhc2ljIl19.hknVcQzAAKejfHUm53G4rTx5ZJ-09mjy9WEZerPne5HPGF6TS957rc7AD6-XDjV3Vi8TVD3zTFgKnIj63ZATGzQm3J5LE-TQmYrtY1L5H4_yxAR3A6TBjL8DCeA460Bh1SnYD_uQySqBod8eAUPJFExL79wTnpQUDr-VVb4WDGwogqBcOUUOZ1p0kKlavx91LsRZkCIY3OjwacPJxZxIcVBx4l-1DN0iICuyBYHon0wJLBMpfFuyEsqem0RuBZENy0goaYPvpG6YRfuWCuVaZLUQQ2lx2wgty_S-gW-tN7YOpAEr6kuoD2AGfFGlngn7H6cWzZdqbGn8yc9IFWh_P15vhvdneH_aJVt4KFO1SzgqN3A1tm_7avJaLfm8BDIKcZYSR6d3HzGEn85WYrqfzXw3gxGgY1OSnzAN6PNq0zjHHcCyeMy7qm3cHL661hDnCWIqfVkiWKy96n8mMumxo6At9BVvnTcbJ9J45hZt64OxL_a9PqQrww9PPRSX8ZHhcrAAJ_907kRt3MBPba7Jd-ek9Ca0JpMzKsNDWdJCZiChAdjB4Nn122YxLjhcGoPzYm1Y1W7T_BkxmXzbdHqRQEtljkots6VW8dsRVqUf01bM2SRhKUWNa6tzPu3vdrdlaCbH_anuVgVVyLYJ2F1prty1qaXwrBwWEv2vkk1WxkQ