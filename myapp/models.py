
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('shop_owner', 'Shop Owner'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def save(self, *args, **kwargs):
        # Automatically approve superusers as shop owners
        if self.is_superuser:
            self.role = 'shop_owner'
            self.is_approved = True  # Superuser should always be approved
        super().save(*args, **kwargs)

from django.db import models
from django.contrib.auth import get_user_model

class Complaint(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    issue_description = models.TextField()
    purchase_receipt = models.FileField(upload_to='complaints/receipts/')
    product_image = models.ImageField(upload_to='complaints/images/')
    status_choices = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Complaint by {self.user.username} on {self.created_at}'


class WarrantyClaim(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    claim_description = models.TextField()
    purchase_receipt = models.FileField(upload_to='warranty_claims/receipts/')
    product_image = models.ImageField(upload_to='warranty_claims/images/')
    claim_status_choices = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    claim_status = models.CharField(max_length=20, choices=claim_status_choices, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Warranty Claim by {self.user.username} on {self.created_at}'
