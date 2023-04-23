from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent')
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect) 
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), max_length=500)

    class Meta:
        model = Review
        fields = ('rating', 'comment',)
    
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if int(rating) not in [choice[0] for choice in self.RATING_CHOICES]:
            raise forms.ValidationError("Invalid rating value")
        return rating
    
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if not comment:
            raise forms.ValidationError("Comment cannot be empty")
        return comment