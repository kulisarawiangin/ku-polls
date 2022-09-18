from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from .models import Choice, Question, Vote
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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

    def get(self, request, pk):
        """Return result page if can_vote method returns True. If not then redirect to results page."""
        question = get_object_or_404(Question, pk=pk)
        if not question.is_published():
            messages.error(request, 'This poll is not publish.')
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return render(request, 'polls/results.html', {'question': question})


