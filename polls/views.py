
"""This module contains the view of site page of the KU Polls application."""
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Question, Choice, Vote
from django.utils import timezone
from django.contrib import messages
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

    def get(self, request, *args, **kwargs):
        """Check if the question is in polling period.
        Arguments:
            request
        Returns:
            httpresponse
        """
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except Question.DoesNotExist:
            messages.error(request, "This poll does not exists.")
            return HttpResponseRedirect(reverse('polls:index'))
        if not question.is_published():
            messages.error(request, "This poll is not publish.")
            return HttpResponseRedirect(reverse('polls:index'))
        try:
            current_vote = Vote.objects.get(user=request.user,
                                            choice__in=question.
                                            choice_set.all())
            check = current_vote.choice.choice_text
        except (Vote.DoesNotExist, TypeError):
            check = ""
        if question.can_vote():
            return render(request, 'polls/detail.html',
                          {"question": question, "check": check})
        else:
            messages.error(request, 'This poll is over.')
            return HttpResponseRedirect(reverse('polls:index'))


class ResultsView(generic.DetailView):
    """View for result.html"""
    model = Question
    template_name = 'polls/results.html'

    def get(self, request, *args, **kwargs):
        """Check the result.
        Arguments:
            request
        Returns:
            httpresponse
        """
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except (KeyError, Question.DoesNotExist):
            messages.error(request, "This poll does not exists.")
            return HttpResponseRedirect(reverse('polls:index'))
        if question.is_published():
            return render(request, 'polls/results.html',
                          {"question": question})
        else:
            messages.error(request, "This poll result is not available.")
            return HttpResponseRedirect(reverse('polls:index'))


@login_required
def vote(request, question_id):
    """Vote for voting button."""
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        try:
            current_vote = Vote.objects.get(user=user,
                                            choice__question=question_id)
        except Vote.DoesNotExist:
            current_vote = Vote.objects.create(user=user,
                                               choice=selected_choice)
        current_vote.choice = selected_choice
        current_vote.save()
        return HttpResponseRedirect(reverse
                                    ('polls:results', args=(question.id,)))
