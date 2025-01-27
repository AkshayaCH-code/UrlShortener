from datetime import timedelta, datetime

import pytz
from django.http import HttpResponseRedirect
from rest_framework.exceptions import NotFound

from URLShortener.settings import env
from urlshortnerapp.models import Analytics, URL
from urlshortnerapp.utils import generate_short_url, get_client_ip

from django.shortcuts import render, redirect


def shorten_url_view(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        expiration_hours = int(request.POST.get('expiration_hours', 24))

        if not original_url:
            # Fetch all shortened URLs and their analytics
            urls = URL.objects.all()
            analytics = {
                url.short_url: Analytics.objects.filter(url=url).count()
                for url in urls
            }

            # Render template with additional data
            return render(request, 'shorten_url.html', {
                'urls': urls,
                'analytics': analytics,
                'port': env('PORT')
            })

        short_url = generate_short_url(original_url)
        expiration_timestamp = datetime.now() + timedelta(hours=expiration_hours)

        url, created = URL.objects.get_or_create(
            original_url=original_url,
            defaults={
                'short_url': short_url,
                'expiration_timestamp': expiration_timestamp
            }
        )
        analytics_data = Analytics.objects.filter(url=url)
        total_views = analytics_data.count()
        access_logs = list(analytics_data.values('access_timestamp', 'ip_address'))
        for log in access_logs:
            log['access_timestamp'] = log['access_timestamp'].isoformat()

        request.session['short_url_data'] = {
            'original_url': original_url,
            'short_url': f'http://localhost:{env("PORT")}/{url.short_url}',
            'expiration_timestamp': expiration_timestamp.isoformat(),
            'access_logs': access_logs,
            'total_views': total_views
        }

        return redirect('shorten_success_view')
    else:
        urls = URL.objects.all()
        analytics = {
            url.short_url: Analytics.objects.filter(url=url).count()
            for url in urls
        }

        # Render template with additional data
        return render(request, 'shorten_url.html', {
            'urls': urls,
            'analytics': analytics,
            'port': env('PORT')
        })


def shorten_success_view(request):
    # Retrieve the shortened URL data from the session
    short_url_data = request.session.pop('short_url_data', None)
    if not short_url_data:
        return redirect('shorten_url')  # Redirect if no data is found

    return render(request, 'shorten_success.html', short_url_data)


def analytics_view(request, short_url):
    try:
        url = URL.objects.get(short_url=short_url)
    except URL.DoesNotExist:
        return render(request, 'analytics.html', {'error': 'URL not found.'})

    analytics_data = Analytics.objects.filter(url=url)
    access_logs = list(analytics_data.values('access_timestamp', 'ip_address', 'views_count'))
    for log in access_logs:
        log['access_timestamp'] = log['access_timestamp'].isoformat()

    return render(request, 'analytics.html', {
        'short_url': f'http://localhost:{env("PORT")}/{url.short_url}',
        'access_logs': access_logs,

    })


def redirect_view(request, short_url):
    # Fetch the URL object based on the short URL
    try:
        url = URL.objects.get(short_url=short_url)
    except URL.DoesNotExist:
        raise NotFound("This URL does not exist.")

    # Check if the URL has expired
    if datetime.now(tz=pytz.UTC) > url.expiration_timestamp:
        return render(request, 'url_expired.html')  # Render the expired URL template

    # Log the analytics data
    obj, created = Analytics.objects.get_or_create(
        url=url,
        ip_address=get_client_ip(request)
    )
    obj.views_count += 1
    obj.save()

    # Redirect to the original URL
    return HttpResponseRedirect(url.original_url)
