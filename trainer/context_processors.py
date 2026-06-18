"""Inject the Brain Quest player dashboard into every template so the app
shell (header profile chip + bottom nav) is data-driven everywhere."""
from . import mission_service


def brainquest_shell(request):
    # Skip admin / non-relevant paths cheaply
    path = request.path or ""
    if path.startswith("/admin") or path.startswith("/static") or path.startswith("/media"):
        return {}
    try:
        player = mission_service.get_player(request)
        dash = mission_service.player_dashboard(player)
        return {"shell": dash}
    except Exception:
        return {}
