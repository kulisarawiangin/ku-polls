from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from .models import Choice, Question
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
        return redirect('polls')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


class IndexView(generic.ListView):
    """View for index.html"""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin,generic.DetailView):
    """View for detail.html"""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request,  *args, **kwargs):
        """Check if the question is in polling period.
        Arguments:
            request
        Returns:
            httpresponse
        """
        question = get_object_or_404(Question, pk=kwargs['pk'])
        if not question.is_published():
            messages.error(request, 'This poll is not publish.')
            return HttpResponseRedirect(reverse('polls:index'))
        elif not question.can_vote():
            messages.error(request, 'This poll is over.')
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return render(request, 'polls/detail.html', {'question': question, })


class ResultsView(generic.DetailView):
    """View for result.html"""
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """Vote for a choice on a question (poll)."""
    user = request.user
    if not user.is_authenticated:
       return redirect('login')
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if question.can_vote():
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
        else:
            messages.error(request, "Can't vote this poll")
            return HttpResponseRedirect(reverse('polls:index'))



