from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# from ..models import Nurse

def index(Request):
    #Id will get from session once login completed
    id = 1
    context = {'id': id}
    return render(Request, 'nurse/index.html', context)
    pass

# def vote(request, question_id):
#     question = get_object_or_404(Nurse, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))