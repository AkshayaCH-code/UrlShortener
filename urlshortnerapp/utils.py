import hashlib


def generate_short_url(original_url):
    """Generate a hash-based short URL."""
    return hashlib.md5(original_url.encode()).hexdigest()[:6]

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip