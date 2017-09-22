from django.shortcuts import render
from django.http import HttpResponse
import re

requests = []
# Create your views here.
def index(request):
    global requests

    data = get_data(request)
    requests.append(data)

    output = ''

    for item in requests:
        output += item + '<br><br><br>'

    
    return HttpResponse(output)


def clear(request):
    global requests
    requests = []
    return HttpResponse('Removed')


def get_data(request):
    output = str(request.get_host())
    headers = get_headers(request)
    for k in headers:
        output += '<br>' + k + ': ' + headers[k]

    return output


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_headers(request):
    regex_http_          = re.compile(r'^HTTP_.+$')
    regex_content_type   = re.compile(r'^CONTENT_TYPE$')
    regex_content_length = re.compile(r'^CONTENT_LENGTH$')

    request_headers = {}
    for header in request.META:
        if regex_http_.match(header) or regex_content_type.match(header) or regex_content_length.match(header):
            request_headers[header] = request.META[header]
    
    return request_headers