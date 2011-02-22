from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from polls.models import Poll, Choice
from django.template import Context, RequestContext, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers

jsonSerializer = serializers.get_serializer("json")
jsonize = jsonSerializer()

def api(request):
    return render_to_response('jpolls/api.html')

def index(request):
    poll_list = jsonize.serialize(Poll.objects.all().order_by('-pub_date')[:])
    return HttpResponse(poll_list)

def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    #j = json.dumps(p)
    return render_to_response('jpolls/detail.html', {'poll': p})
    
def results(request, poll_id):
    #p = jsonize.serialize([get_object_or_404(Poll, pk=poll_id)])
    #return render_to_response('jpolls/results.html', {'poll': p})
    #return HttpResponse(p)
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('jpolls/results.html', {'poll': p})

def vote(request, poll_id, choice_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        return HttpResponse('{"error":"choice %s does not exist"}' % choice_id)
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('jpolls.views.results', args=(p.id,)))
