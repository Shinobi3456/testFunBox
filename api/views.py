import json
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import time
from urllib.parse import urlparse

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


@api_view(['POST'])
def visited_links(request, *args, **kwargs):
    try:
        incorrect_link = []
        data = json.loads(request.body)

        links = data.get('links', [])
        if len(links) == 0:
            raise Exception("Not find 'links'.")

        if not isinstance(links, list):
            raise Exception("Links must be of type list.")

        for link in links:
            parse = urlparse(link)
            if len(parse.netloc) == 0:
                incorrect_link.append(link)
                continue

            redis_instance.zadd('visited', {f'{str(time.time())}--{link}': 0})

        if len(incorrect_link) > 0:
            raise Exception(f"Incorrect links: {','.join(incorrect_link)}")

    except Exception as e:
        return Response({'status': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'status': 'ok'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def visited_domains(request, *args, **kwargs):
    from_time = request.GET.get('from', None)
    to_time = request.GET.get('to', None)

    try:
        if from_time is None or to_time is None:
            raise Exception('No "from" or "to" parameters specified')

        if not from_time.isdigit():
            raise Exception('From must be a number')

        if not to_time.isdigit():
            raise Exception('To must be a number')

        domains = set()
        visited = redis_instance.zrangebylex('visited', f'[{from_time}', f'[{to_time}')
        for row in visited:
            link = str(row).split('--')[1][:-1]
            parse = urlparse(link)
            domains.add(parse.netloc)

    except Exception as e:
        return Response({'status': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    response = {
        'domains': domains,
        'status': 'ok'
    }
    return Response(response, status=status.HTTP_200_OK)
