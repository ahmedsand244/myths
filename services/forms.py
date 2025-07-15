

from django import forms
from .models import OrganizerReview

class OrganizerReviewForm(forms.ModelForm):
    class Meta:
        model = OrganizerReview
        fields = ['name', 'rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }





from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']





