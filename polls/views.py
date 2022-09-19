from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from .models import Choice, Question, Vote
from django.contrib.auth.decorators import login_required


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


class DetailView(generic.DetailView):
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
        if request.user.is_anonymous:
            return redirect(to='http://127.0.0.1:8000/accounts/login')
        question = get_object_or_404(Question, pk=kwargs['pk'])
        user = request.user
        if not question.is_published():
            messages.error(request, 'This poll is not publish.')
            return HttpResponseRedirect(reverse('polls:index'))
        elif not question.can_vote():
            messages.error(request, 'This poll is over.')
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            choice = ""
            user_vote = Vote.objects.filter(user=user)
            for select in user_vote:
                if select.question == question:
                    choice = select.choice.choice_text
            return render(request, 'polls/detail.html', {'question': question, 'check': choice, })


class ResultsView(generic.DetailView):
    """View for result.html"""
    model = Question
    template_name = 'polls/results.html'

    def get(self, request,  *args, **kwargs):
        """Check if the question is in polling period if not return result.
        Arguments:
            request
        Returns:
            httpresponse
        """
        question = get_object_or_404(Question, pk=kwargs['pk'])
        if not question.is_published():
            messages.error(request, 'This poll is not publish.')
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return render(request, 'polls/results.html', {'question': question})



@login_required
def vote(request, question_id):
    """Vote for voting button."""
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        vote = Vote.objects.filter(user=user)
        for select in vote:
            if select.question == question:
                select.choice = selected_choice
                select.save()
                return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        new_vote = Vote.objects.create(user=user, choice=selected_choice)
        new_vote.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
