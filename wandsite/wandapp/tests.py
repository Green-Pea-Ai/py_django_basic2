from django.test import TestCase

import datetime
from django.utils import timezone

from .models import Question

from django.urls import reverse

# Create your tests here.
class QuestionModelTests(TestCase):
	
	# Old
	def test_was_published_recently_with_old_question(self):
		"""
		was_published_recently() returns False for questions whose pub_date
		is older than 1 day.
		게시한 설문이 old 상태일 때 False를 반환하는지 테스트.
		"""
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	# Recent
	def test_was_published_recently_with_recent_question(self):
		"""
		was_published_recently() returns True for questions whose pub_date
		is within the last day.
		게시한 설문이 recent 상태일 때 True를 반환하는지 테스트.
		"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)

	# Future
	def test_was_published_recently_with_future_question(self):
		"""
		was_published_recently() returns False for questions whose pub_date
		is in the future.
		게시한 설문이 future 상태일 때 False를 반환하는지 테스트.
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)


def create_question(question_text, days):
	"""
	Create a question with the given `question_text` and published the
	given number of `days` offset to now (negative for questions published
	in the past, positive for questions that have yet to be published).
	`question_text`로 질문을 만들고 `days` 오프셋을 통해 테스트용 설문을 게시하는데 반복 사용된다.
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):

	def test_no_questions(self):
		"""
		If no questions exist, an appropriate message is displayed.
		질문이 존재하지 않는 경우 적절한 메시지 표시가 정상적으로 되는지 테스트.
		"""
		response = self.client.get(reverse('wandapp:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_past_question(self):
		"""
		Questions with a pub_date in the past are
		displayed on the index page.
		pub_date가 과거인 질문이 index page에 표시되는지 테스트.
		"""
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('wandapp:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)
	
	def test_future_question(self):
		"""
		Questions with a pub_date in the future aren't
		displayed on the index page.
		pub_date가 미래인 질문이 index page에 표시가 안되는 것을 테스트.
		"""
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('wandapp:index'))
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_future_question_and_past_question(self):
		"""
		Even if both past and future questions exist,
		only past questions are displayed.
		과거와 미래의 질문이 둘 다 있더라도 과거 질문만 표시되는지 테스트.
		"""
		create_question(question_text="Past question.", days=-30)
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('wandapp:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)

	def test_two_past_questions(self):
		"""
		The questions index page may display multiple questions.
		index page에 여러 질문들이 표시되는지 테스트.
		"""
		create_question(question_text="Past question 1.", days=-30)
		create_question(question_text="Past question 2.", days=-5)
		response = self.client.get(reverse('wandapp:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			[
				'<Question: Past question 2.>', 
				'<Question: Past question 1.>'
			]
		)


class QuestionDetailViewTests(TestCase):

	def test_future_question(self):
		"""
		The detail view of a question with a pub_date in the future
		returns a 404 not found.
		pub_date가 미래인 질문의 상세보기 페이지에서 404를 return하는지 테스트.
		사용자가 하드 코딩으로 페이지에 접근했을 때 페이지를 띄우면 안된다. 
		"""
		future_question = create_question(question_text='Future question.', days=5)
		url = reverse('wandapp:detail', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_past_question(self):
		"""
		The detail view of a question with a pub_date in the past
		displays the question's text.
		pub_date가 과거인 질문이 상세보기 페이지에 표시되는지 테스트.
		"""
		past_question = create_question(question_text='Past Question.', days=-5)
		url = reverse('wandapp:detail', args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)