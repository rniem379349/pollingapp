from django import forms
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
