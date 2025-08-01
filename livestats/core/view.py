from datetime import datetime
import os

from core.models import FSTimeResult
from django.http import Http404
from django.shortcuts import render
from django.templatetags.static import static
from django.conf import settings

from .utils import format_duration


def lap_banner(request, event):
    if event not in [choice[0].lower() for choice in FSTimeResult.FSEvent.choices]:
        raise Http404("Not found")

    today = datetime.today().date()
    last_lap = (
        FSTimeResult.objects.filter(created_at__date=today, event=event.upper())
        .order_by("-created_at")
        .first()
    )

    best_lap = (
        FSTimeResult.objects.filter(created_at__date=today, event=event.upper())
        .order_by("time_result")
        .first()
        or last_lap
    )

    filename = f'{last_lap.driver.fsbk_id if last_lap and last_lap.driver and last_lap.driver.fsbk_id else "data"}.json'
    filepath = os.path.join(settings.STATIC_ROOT, filename)
    if not os.path.exists(filepath):
        print(f"Banner file ({filename}) not found, using default.")
        filename = "data.json"
    url = static(filename)

    return render(
        request,
        "lap_banner.html",
        context={
            "best_lap": format_duration(best_lap.time_result if best_lap else None),
            "last_lap": format_duration(last_lap.time_result if last_lap else None),
            "event": event,
            "url": url,
        },
    )
