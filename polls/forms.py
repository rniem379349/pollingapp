from django import forms

from .models import Question, Choice

# Put all the forms which are to inherit from the main forms here.

class QuestionCreationForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']


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
