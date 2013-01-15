from django.template import RequestContext
from quiz.models import Country, Site, Quiz, Question, Choice, Guess
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from random import randint, shuffle
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

def index(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    try:
        qz = Quiz.objects.filter(session_key=request.session.session_key).order_by('-created_at')[0]
        try:
            q = Question.objects.filter(quiz_id=qz.id, answered=False).order_by('-id')[0]
            return render_to_response('unesco/index.html', {
                'returning': True,
                'quiz_id': qz.id,
                'current_question': q.id,
                })
        except IndexError:
            return render_to_response('unesco/index.html', {
                'returning': True,
                'quiz_id': qz.id,
                })
    except IndexError:
        return render_to_response('unesco/index.html', {
            'returning': False,
            })


def new_quiz(request):
    qz = Quiz.objects.create(created_at=timezone.now(), session_key=request.session.session_key)
    return HttpResponseRedirect(reverse('quiz.views.new_question', args=(qz.id,)))

def new_question(request, quiz_id):
    number_of_questions = len(Question.objects.filter(quiz_id=quiz_id))
    if number_of_questions >= 10:
        return HttpResponseRedirect(reverse('quiz.views.score_report', args=(quiz_id,)))
    else:
        q = Question.objects.create(created_at=timezone.now(), site_id=randint(1, 776), question_number=number_of_questions + 1, quiz_id=quiz_id, answered=False)
        s = q.site

        choice_numbers = range(1, 5)
        shuffle(choice_numbers)

        country_ids = range(1, 138)
        shuffle(country_ids)
        country_ids.remove(s.country_id)

        q.choice_set.create(created_at=timezone.now(), choice_number=choice_numbers.pop(), country_id=s.country_id)  # Answer
        q.choice_set.create(created_at=timezone.now(), choice_number=choice_numbers.pop(), country_id=country_ids.pop())
        q.choice_set.create(created_at=timezone.now(), choice_number=choice_numbers.pop(), country_id=country_ids.pop())
        q.choice_set.create(created_at=timezone.now(), choice_number=choice_numbers.pop(), country_id=country_ids.pop())

        return HttpResponseRedirect(reverse('quiz.views.question', args=(q.id,)))

def question(request, question_id):
    q = Question.objects.get(pk=question_id)
    b = q.site.brief_desc.replace(q.site.country.name, '____________')
    c = q.choice_set.order_by('choice_number')
    return render_to_response('unesco/question.html', {
        'question': q,
        'brief_desc': b,
        'choices': c
        }, context_instance=RequestContext(request))

def submit(request, question_id):
    g = Guess.objects.create(created_at=timezone.now(), choice_id=request.POST['choice'])
    if g.choice.question.answered:
        try:
            q = Question.objects.filter(quiz_id=g.choice.question.quiz.id, answered=False).order_by('-id')[0]
            return HttpResponseRedirect(reverse('quiz.views.question', args=(q.id,)))
        except IndexError:
            return HttpResponseRedirect(reverse('quiz.views.new_question', args=(q.quiz.id,)))
    else:
        return HttpResponseRedirect(reverse('quiz.views.answer', args=(g.id,)))

def answer(request, guess_id):
    g = Guess.objects.get(pk=guess_id)
    c = g.choice.question.choice_set.order_by('choice_number')
    q = Question.objects.get(id=g.choice.question.id)
    q.answered = True
    q.save()
    if g.choice.question.site.country.id == g.choice.country.id:
        q.correct = True
        q.save()
    else:
        pass
    if len(Question.objects.filter(quiz_id=g.choice.question.quiz.id)) >= 10:
        finished = True
    else:
        finished = False
    return render_to_response('unesco/answer.html', {
        'guess': g,
        'choices': c,
        'finished': finished,
        })
def score_report(request, quiz_id):
    questions_answered = len(Question.objects.filter(quiz_id=quiz_id, answered=True))
    correct_answers = len(Question.objects.filter(quiz_id=quiz_id, correct=True))
    return render_to_response('unesco/score_report.html', {
        'questions_answered': questions_answered,
        'correct_answers': correct_answers,
        })
