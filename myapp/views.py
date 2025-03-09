from django.shortcuts import render,redirect
from django.views import View
from myapp.forms import RegisterForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings



from .forms import ComplaintForm, WarrantyClaimForm
from .models import Complaint, WarrantyClaim


class Home(View):
    def get(self,request):
        return render(request,'index.html')

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
        return redirect('home')  


class SubmitComplaintView(View):
    def get(self, request):
        form = ComplaintForm()
        complaints = Complaint.objects.filter(user=request.user)
        return render(request, 'submit_complaint.html', {'form': form,'complaints':complaints})

    def post(self, request):
        complaints = Complaint.objects.filter(user=request.user)
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, "Your complaint has been submitted.")
            return redirect('customer_dashboard')  # Redirect to dashboard or status page
        return render(request, 'submit_complaint.html', {'form': form,'complaints':complaints})

class DeleteComplaintView(View):
    def post(self, request, pk):
        complaint = get_object_or_404(Complaint, pk=pk, user=request.user)
        if complaint.status == "submitted":
            complaint.delete()
            messages.success(request, "Your complaint has been deleted.")
        else:
            messages.error(request, "You can only delete complaints with 'submitted' status.")
        return redirect('submit_complaint')  # Redirect back to the dashboard


class SubmitWarrantyClaimView(View):
    def get(self, request):
        form = WarrantyClaimForm()
        warranty_claims = WarrantyClaim.objects.filter(user=request.user)
        return render(request, 'submit_warranty_claim.html', {'form': form,'warranty_claims':warranty_claims})

    def post(self, request):
        warranty_claims = WarrantyClaim.objects.filter(user=request.user)
        form = WarrantyClaimForm(request.POST, request.FILES)
        if form.is_valid():
            warranty_claim = form.save(commit=False)
            warranty_claim.user = request.user
            warranty_claim.save()
            messages.success(request, "Your warranty claim has been submitted.")
            return redirect('submit_warranty_claim')
        return render(request, 'submit_warranty_claim.html', {'form': form,'warranty_claims':warranty_claims})


class DeleteWarrantyClaimView(View):
    def post(self, request, pk):
        claim = get_object_or_404(WarrantyClaim, pk=pk, user=request.user)
        if claim.claim_status == "submitted":
            claim.delete()
            messages.success(request, "Your warranty claim has been deleted.")
        else:
            messages.error(request, "You can only delete claims with 'submitted' status.")
        return redirect('submit_warranty_claim')  # Redirect back to the dashboard


class CustomerDashboardView(View):
    def get(self, request):
        return render(request, 'customer_dashboard.html')
    

class Complaint_View(View):
    def get(self, request):
        complaints = Complaint.objects.all()
        total_complaints = complaints.count()
        status_counts = complaints.values('status').annotate(count=Count('status'))
        status_summary = {item['status']: item['count'] for item in status_counts}

        return render(request, 'complaints.html', {
            'complaints': complaints,
            'total_complaints': total_complaints,
            'status_summary': status_summary
        })
    
class Warranty_View(View):
    def get(self, request):
        warranty_claims = WarrantyClaim.objects.all()
        total_claims = warranty_claims.count()
        status_counts = warranty_claims.values('claim_status').annotate(count=Count('claim_status'))
        status_summary = {item['claim_status']: item['count'] for item in status_counts}

        return render(request, 'warranty.html', {
            'warranty_claims': warranty_claims,
            'total_claims': total_claims,
            'status_summary': status_summary
        })


from django.db.models import Count, Max
from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import ChatMessage

User = get_user_model()

class ShopOwnerDashboardView(View):
    def get(self, request):
        # Fetch users sorted by the latest chat time
        users = User.objects.filter(is_superuser=False).annotate(
            last_chat_time=Max('sent_warranty_messages__timestamp')
        ).order_by('-last_chat_time')

        # Calculate totals
        total_users = User.objects.filter(is_superuser=False).count()
        total_complaints = Complaint.objects.count()
        total_warranties = WarrantyClaim.objects.count()

        context = {
            'users': users,
            'total_users': total_users,
            'total_complaints': total_complaints,
            'total_warranties': total_warranties,
        }
        
        return render(request, 'shop_owner_dashboard.html', context)



class UpdateComplaintStatusView(View):
    def post(self, request, pk):
        complaint = get_object_or_404(Complaint, pk=pk)
        mail = complaint.user.email
        new_status = request.POST.get('status')

        if new_status and new_status != complaint.status and new_status in dict(Complaint.status_choices):
            # Update the status
            complaint.status = new_status
            complaint.save()
            messages.success(request, f"Complaint status updated to {new_status}.")
            
            # Email subject and message based on status
            subject = 'ElectroClaim - Complaint Status Update'
            status_messages = {
                'submitted': "Your complaint has been submitted successfully. Our team will review it soon.",
                'in_progress': "Your complaint is currently being processed. We will update you once it's resolved.",
                'resolved': "Great news! Your complaint has been resolved.",
                'rejected': "Unfortunately, your complaint has been rejected. Please contact support if you need further assistance."
            }
            message = f"Dear {complaint.user},\n\n{status_messages.get(new_status, 'Your complaint status has been updated.')}\n\nBest regards,\nElectroClaim Team"

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [mail]
            send_mail(subject, message, email_from, recipient_list)

        return redirect('complaints')



class UpdateWarrantyClaimStatusView(View):
    def post(self, request, pk):
        warranty_claim = get_object_or_404(WarrantyClaim, pk=pk)
        mail = warranty_claim.user.email
        new_status = request.POST.get('status')

        if new_status and new_status != warranty_claim.claim_status:
            # Update the status
            warranty_claim.claim_status = new_status
            warranty_claim.save()
            messages.success(request, f"Warranty claim status updated to {new_status}.")
            
            # Email subject and message based on status
            subject = 'ElectroClaim - Warranty Claim Update'
            status_messages = {
                'submitted': "Your warranty claim has been submitted successfully. We will review it soon.",
                'under_review': "Your warranty claim is now under review. We will update you once the process is complete.",
                'approved': "Congratulations! Your warranty claim has been approved.",
                'denied': "We regret to inform you that your warranty claim has been denied."
            }
            message = f"Dear {warranty_claim.user},\n\n{status_messages.get(new_status, 'Your claim status has been updated.')}\n\nBest regards,\nElectroClaim Team"

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [mail]
            send_mail(subject, message, email_from, recipient_list)

        return redirect('warranty')
            

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
    


from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ChatMessage
from .forms import ChatForm

User = get_user_model()

class ChatView(LoginRequiredMixin, View):
    def get(self, request, user_id=None):
        if request.user.is_superuser:
            if not user_id:
                return redirect('admin-dashboard')  # Redirect to admin dashboard if no user_id
            chat_user = get_object_or_404(User, id=user_id)
        else:
            chat_user = User.objects.filter(is_superuser=True).first()
            if not chat_user:
                return render(request, 'chat.html', {'error': "No admin found."})

        chats = ChatMessage.objects.filter(
            sender=request.user, receiver=chat_user
        ) | ChatMessage.objects.filter(
            sender=chat_user, receiver=request.user
        ).order_by("timestamp")

        return render(request, 'chat.html', {'chats': chats, 'chat_user': chat_user, 'form': ChatForm()})

    def post(self, request, user_id=None):
        if request.user.is_superuser:
            if not user_id:
                return redirect('admin-dashboard')  # Redirect if no user_id is provided
            chat_user = get_object_or_404(User, id=user_id)
        else:
            chat_user = User.objects.filter(is_superuser=True).first()
            if not chat_user:
                return render(request, 'chat.html', {'error': "No admin found."})

        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender = request.user
            chat.receiver = chat_user
            chat.save()
            return redirect('chat', user_id=chat_user.id)  # Fixed redirection

        chats = ChatMessage.objects.filter(
            sender=request.user, receiver=chat_user
        ) | ChatMessage.objects.filter(
            sender=chat_user, receiver=request.user
        ).order_by("timestamp")

        return render(request, 'chat.html', {'chats': chats, 'chat_user': chat_user, 'form': form})






