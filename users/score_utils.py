from django.contrib.auth.models import User

from lessons.models import Lesson
from users.models import Score, UserProgress


def update_score(username, score, lesson_id=None):
    user = User.objects.get(username=username)
    user_score = Score.objects.filter(user=user).first()
    if user_score is None:
        user_score = Score(user=user, score=0)
    if lesson_id is not None:
        lesson = Lesson.objects.get(pk=lesson_id)
        user_progress = UserProgress.objects.filter(user=user, lesson=lesson).first()
        if user_progress is None:
            user_progress = UserProgress(user=user, lesson=lesson, score=0)
        else:
            user_score = Score.objects.get(user=user)
            user_score.score -= user_progress.score
            user_score.save()
        user_progress.score = score
        user_progress.save()
    user_score.score += score
    user_score.save()
