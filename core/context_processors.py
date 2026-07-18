from .service.event import EventService

def unread_event_count(request):
    if not request.user.is_authenticated:
        return {
            "unread_event_count": 0,
        }
    
    return {
        "unread_event_count": EventService.get_unread_events(user=request.user).count(),
    }