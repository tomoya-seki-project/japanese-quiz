import logging
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError

from ..models import UserProfile

logger = logging.getLogger(__name__)
User = get_user_model()

class AccountService():

    @staticmethod
    def update_user_record(*, request, user_id, quiz_result):
        if request.user.pk != user_id:
            return
        user_profile = UserProfile.objects.select_for_update().get(user_id=user_id)
        try:
            with transaction.atomic():
                if quiz_result is True:
                    user_profile.total_answered += 1
                    user_profile.total_correct += 1
                    if user_profile.global_streak > 0:
                        user_profile.global_streak += 1
                    else:
                        user_profile.global_streak = 1
                    if user_profile.global_streak > user_profile.most_correct:
                        user_profile.most_correct = user_profile.global_streak
                elif quiz_result is False:
                    user_profile.total_answered += 1
                    user_profile.total_wrong += 1
                    if user_profile.global_streak < 0:
                        user_profile.global_streak -= 1
                    else:
                        user_profile.global_streak = -1
                    if abs(user_profile.global_streak) > user_profile.most_wrong:
                        user_profile.most_wrong = abs(user_profile.global_streak)

                user_profile.save(update_fields=["total_answered",
                                                 "total_correct",
                                                 "total_wrong",
                                                 "most_correct,"
                                                 "most_wrong",
                                                 "global_streak"
                                                 ])
        except IntegrityError:
            raise ValidationError("something")
