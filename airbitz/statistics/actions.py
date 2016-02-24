from django.http import HttpResponse
import csv

def export_buysell_action(description="Buy/Sell Report"):
    from statistics.models import Event
    def export_buysell(modeladmin, request, qs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=buysell.csv'

        writer = csv.writer(response)
        writer.writerow([
            "Created",
            "Event Type",
            "Network",
            "Btc",
            "Partner",
            "User",
        ])

        for e in Event.objects.all().order_by('-created'):
            row=[
                e.created.strftime('%Y-%m-%d %H:%M'),
                e.event_type,
                e.event_network,
                e.btc(),
                e.partner(),
                e.user(),
            ]
            writer.writerow(row)
        return response

    export_buysell.short_description = description
    return export_buysell
