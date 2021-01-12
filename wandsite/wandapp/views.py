from django.shortcuts import render

from django.http import HttpResponse

from .models import Question
from django.template import loader
from django.shortcuts import render

from django.http import Http404
from django.shortcuts import get_object_or_404

from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Choice

# Create your views here.
# def index(request):
# 	return HttpResponse("Hello, world. You're at the wandapp index.")


def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {
		'latest_question_list': latest_question_list,
	}
	return render(request, 'wandapp/index.html', context)

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)	
	return render(request, 'wandapp/detail.html', {'question': question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'wandapp/results.html', {'question': question})
	# response = "You're looking at the results of question %s."
	# return HttpResponse(response % question_id)

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'wandapp/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()

		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
	return HttpResponseRedirect(reverse('wandapp:results', args=(question.id,)))

