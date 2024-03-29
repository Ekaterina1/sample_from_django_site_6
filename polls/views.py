# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.utils import timezone
from django.views import generic
from polls.models import Poll, Choice

from django.shortcuts import render, get_object_or_404
#autocomplete works
#def index(request):
#    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
#    context = {'latest_poll_list': latest_poll_list}
#    return render(request, 'index.html', context)

#no autocomplete here
# def index(request):
#     latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('index.html')
#     context = RequestContext(request, {
#         'latest_poll_list': latest_poll_list,
#     })
#     return HttpResponse(template.render(context))

#def detail(request, poll_id):
#    poll = get_object_or_404(Poll, pk=poll_id)
#    return render(request, 'detail.html', {'poll': poll})

# def results(request, poll_id):
#     return HttpResponse("You're looking at the results of poll %s." % poll_id)

#def results(request, poll_id):
#    poll = get_object_or_404(Poll, pk=poll_id)
#    return render(request, 'results.html', {'poll': poll})

# def vote(request, poll_id):
#     return HttpResponse("You're voting on poll %s." % poll_id)

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_poll_list'

    #"""
    #Return the last five published polls (not including those set to be
    #published in the future).
    #"""
    def get_queryset(self):
        return Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'detail.html'
    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'results.html'

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

