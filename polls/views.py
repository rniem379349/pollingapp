import traceback

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.forms.models import modelformset_factory

from .models import Question, Choice, Comment
from .forms import QuestionCreationForm, ChoiceCreationForm

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    

class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'polls/newquestion.html'
    model = Question
    form_class = QuestionCreationForm

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank creation form for a question and its choices
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ChoiceFormSet = modelformset_factory(Choice, form=ChoiceCreationForm, extra=10, max_num=10)
        formset = ChoiceFormSet(queryset=Choice.objects.none())
        # print(formset)
        return self.render_to_response(
            self.get_context_data(
                form=form,
                formset=formset,
            )
        )
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        ChoiceFormSet = modelformset_factory(Choice, form=ChoiceCreationForm, extra=10, max_num=10)
        # form_class = self.get_form_class()
        form = self.get_form()
        # print(form)
        # print("------")
        formset = ChoiceFormSet(self.request.POST)
        # for form in formset:
        #     print(form)
        # print("------")
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, formset):
        try:
            # check if there are at least two choices
            if self.less_than_two_choices(formset):
                messages.info(self.request, 'Please provide at least two choices.')
                return HttpResponseRedirect(reverse('polls:create-question'))

            q = Question.objects.create(question_text=form.cleaned_data['question_text'], pub_date=timezone.now())

            # print(formset.cleaned_data)
            for form in formset.cleaned_data:
                # print(form.get('choice_text'))
                if form.get('choice_text'):
                    Choice.objects.create(votes=0, question=q, choice_text=form['choice_text'])
        except Exception:
            traceback.print_exc()
            messages.info(self.request, 'Could not create question.')
            return HttpResponseRedirect(reverse('polls:new-question'))
        messages.success(self.request, 'Question added successfully!')
        return HttpResponseRedirect(reverse('polls:index'))
    
    def less_than_two_choices(self, formset):
        """
        Simple check to see if a user filled in one or none of the choice fields.
        If true, the question should not be added, and an error message displayed.
        """
        filled_in_choices = 0
        for form in formset.cleaned_data:
            if form.get('choice_text'):
                filled_in_choices += 1
            if filled_in_choices >= 2:
                return False
        return True


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(question=self.kwargs.get('pk'))
        return context
    

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class CommentListView(generic.ListView):
    model = Comment
    context_object_name = 'comments'

    def get_queryset(self):
        return Comment.objects.filter(question=self.kwargs.get('pk'))
        

class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    fields = ['content']
    template_name = 'polls/comment.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        question_id = self.kwargs.get('question_id')
        Comment.objects.create(question=Question.objects.get(pk=question_id), user=self.request.user, content=form.cleaned_data['content'])
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))