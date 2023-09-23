from django.conf import settings # import the settings file

def rest_url(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'REST_URL': settings.REST_URL}