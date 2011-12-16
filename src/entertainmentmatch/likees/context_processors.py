from django.conf import settings # import the settings file

def template_domain(context):
    return {'TEMPLATE_DOMAIN': settings.TEMPLATE_DOMAIN, 'COVER_DOMAIN':settings.COVER_DOMAIN}
