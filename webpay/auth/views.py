from django import http
from django.conf import settings
from django.views.decorators.http import require_POST

import commonware.log
from django_browserid import get_audience, verify as verify_assertion
from django_browserid.forms import BrowserIDForm
from session_csrf import anonymous_csrf_exempt

from webpay.base.decorators import json_view
from webpay.pin.utils import check_pin_status
from .utils import get_uuid, set_user

log = commonware.log.getLogger('w.auth')


@require_POST
def reset_user(request):
    """
    Reset the logged in Persona user.

    This is not meant as a full logout. It's meant to compliment
    navigator.id.logout() so that both Webpay and Persona think the user
    is logged out.
    """
    if request.session.get('logged_in_user'):
        log.info('Resetting Persona user %s'
                 % request.session['logged_in_user'])
        del request.session['logged_in_user']
    return http.HttpResponse('OK')


@anonymous_csrf_exempt
@require_POST
@json_view
def reverify(request):
    form = BrowserIDForm(data=request.POST)
    if form.is_valid():
        url = settings.BROWSERID_VERIFICATION_URL
        audience = get_audience(request)
        # TODO: when we want to require a forced-auth login across the
        # entire site then how do we do it?
        # See bug 836060.
        extra_params = {'experimental_forceIssuer': settings.BROWSERID_UNVERIFIED_ISSUER,
                        # TODO: how do we make sure this is a proper forced
                        #       auth assertion?
                        # This can also be addressed in bug 836060
                        'experimental_forceAuthentication': 'true',
                        'experimental_allowUnverified': 'true'}

        log.info('Re-verifying Persona assertion. url: %s, audience: %s, '
                 'extra_params: %s' % (url, audience, extra_params))
        result = verify_assertion(form.cleaned_data['assertion'], audience,
                                  extra_params)

        log.info('Reverify got result: %s')
        if result:
            logged_user = request.session.get('uuid')
            email = result.get('unverified-email', result.get('email'))
            reverified_user = get_uuid(email)
            if logged_user and logged_user != reverified_user:
                # TODO: Should we try to support this?
                raise ValueError('A user tried to reverify herself with a '
                                 'new email: %s' % email)

            return {'user_hash': reverified_user}

        log.error('Persona assertion failed.')

    request.session.clear()
    return http.HttpResponseBadRequest()


@anonymous_csrf_exempt
@require_POST
@json_view
def verify(request):
    form = BrowserIDForm(data=request.POST)
    if form.is_valid():
        url = settings.BROWSERID_VERIFICATION_URL
        audience = get_audience(request)
        extra_params = {'experimental_forceIssuer': settings.BROWSERID_UNVERIFIED_ISSUER,
                        'experimental_allowUnverified': 'true'}
        assertion = form.cleaned_data['assertion']

        log.info('verifying Persona assertion. url: %s, audience: %s, '
                 'extra_params: %s, assertion: %s' % (url, audience,
                                                      extra_params, assertion))
        result = verify_assertion(assertion, audience, extra_params)
        if result:
            log.info('Persona assertion ok: %s' % result)
            email = result.get('unverified-email', result.get('email'))
            user_hash = set_user(request, email)
            redirect_url = check_pin_status(request)
            return {
                'needs_redirect': redirect_url is not None,
                'redirect_url': redirect_url,
                'user_hash': user_hash
            }

        log.error('Persona assertion failed.')

    request.session.flush()
    return http.HttpResponseBadRequest()
