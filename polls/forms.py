from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Question, Choice
from flatpickr import DateTimePickerInput

# Put all the forms which are to inherit from the main forms here.

class QuestionCreationForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'ends_on']
        widgets = {
            'ends_on': DateTimePickerInput()
        }
    
    def clean_ends_on(self):
        timestamp = self.cleaned_data['ends_on']
        now = timezone.now()
        if timestamp:
            if timestamp < now + timezone.timedelta(hours=2):
                raise ValidationError("The minimum duration of a poll is two hours.")
        
            return timestamp
        return None


class QuestionEditForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']


class ChoiceCreationForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']


class ChoiceEditForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
