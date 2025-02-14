from django.shortcuts import render,redirect

from django.views import View

from myapp.forms import RegisterForm,LoginForm

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages
from django.shortcuts import get_object_or_404

from .forms import ComplaintForm, WarrantyClaimForm
from .models import Complaint, WarrantyClaim




class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        return render(request, 'register.html', {'form': form})
    




class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user:
                login(request, user)
                
                # If the user is a superuser (admin), redirect to admin dashboard
                if user.is_superuser:
                    return redirect('shop_owner_dashboard')  # Admin dashboard
                else:
                    role = user.role.lower()
                    if role == 'customer':
                        return redirect('customer_dashboard')
                    
            
            messages.error(request, "Invalid username or password.")
        
        return render(request, 'login.html', {'form': form})








class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')  # Redirect to the login page after logout








class SubmitComplaintView(View):
    def get(self, request):
        form = ComplaintForm()
        return render(request, 'submit_complaint.html', {'form': form})

    def post(self, request):
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, "Your complaint has been submitted.")
            return redirect('customer_dashboard')  # Redirect to dashboard or status page
        return render(request, 'submit_complaint.html', {'form': form})









class SubmitWarrantyClaimView(View):
    def get(self, request):
        form = WarrantyClaimForm()
        return render(request, 'submit_warranty_claim.html', {'form': form})

    def post(self, request):
        form = WarrantyClaimForm(request.POST, request.FILES)
        if form.is_valid():
            warranty_claim = form.save(commit=False)
            warranty_claim.user = request.user
            warranty_claim.save()
            messages.success(request, "Your warranty claim has been submitted.")
            return redirect('customer_dashboard')
        return render(request, 'submit_warranty_claim.html', {'form': form})






class SubmitWarrantyClaimView(View):
    def get(self, request):
        form = WarrantyClaimForm()
        return render(request, 'submit_warranty_claim.html', {'form': form})

    def post(self, request):
        form = WarrantyClaimForm(request.POST, request.FILES)
        if form.is_valid():
            warranty_claim = form.save(commit=False)
            warranty_claim.user = request.user
            warranty_claim.save()
            messages.success(request, "Your warranty claim has been submitted.")
            return redirect('customer_dashboard')
        return render(request, 'submit_warranty_claim.html', {'form': form})





class CustomerDashboardView(View):
    def get(self, request):
        complaints = Complaint.objects.filter(user=request.user)
        warranty_claims = WarrantyClaim.objects.filter(user=request.user)
        return render(request, 'customer_dashboard.html', {
            'complaints': complaints,
            'warranty_claims': warranty_claims,
        })






class ShopOwnerDashboardView(View):
    def get(self, request):
        complaints = Complaint.objects.all()
        warranty_claims = WarrantyClaim.objects.all()
        return render(request, 'shop_owner_dashboard.html', {
            'complaints': complaints,
            'warranty_claims': warranty_claims,
        })





class UpdateComplaintStatusView(View):
    def post(self, request, pk):
        complaint = get_object_or_404(Complaint, pk=pk)
        status = request.POST.get('status')
        if status:
            complaint.status = status
            complaint.save()
            messages.success(request, f"Complaint status updated to {status}.")
        return redirect('shop_owner_dashboard')





class UpdateWarrantyClaimStatusView(View):
    def post(self, request, pk):
        warranty_claim = get_object_or_404(WarrantyClaim, pk=pk)
        status = request.POST.get('claim_status')
        if status:
            warranty_claim.claim_status = status
            warranty_claim.save()
            messages.success(request, f"Warranty claim status updated to {status}.")
        return redirect('shop_owner_dashboard')







class ShopOwnerClaimDeleteView(View):
    def post(self, request, claim_type, claim_id):
        # Check if the user is a shop owner based on role
        if not request.user.role == "shop_owner":  # Change this line
            messages.error(request, "You do not have permission to perform this action.")
            return redirect("shop_owner_dashboard")

        if claim_type == "warranty":
            claim = get_object_or_404(WarrantyClaim, id=claim_id)
        elif claim_type == "complaint":
            claim = get_object_or_404(Complaint, id=claim_id)
        else:
            messages.error(request, "Invalid claim type.")
            return redirect("shop_owner_dashboard")

        claim.delete()
        messages.success(request, f"{claim_type.capitalize()} deleted successfully.")
        return redirect("shop_owner_dashboard")