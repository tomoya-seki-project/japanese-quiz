from .service.event import EventService
from .models import Feedback, FeedbackStatus

def unread_event_count(request):
    if not request.user.is_authenticated:
        return {
            "unread_event_count": 0,
        }
    
    return {
        "unread_event_count": EventService.get_unread_events(user=request.user).count(),
    }

def unreply_feedback_count(request):
    if not request.user.is_authenticated:
        return {
            "unreply_feedback_count": 0,
        }
    
    return {
        "unreply_feedback_count": Feedback.objects.filter(status=FeedbackStatus.PENDING).count(),
    }