import logging
import os

import facebook
import shopify

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from hackathon.decorators import shop_login_required


logger = logging.getLogger(__name__)
shopify.Session.setup(
    api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)


def shopify_connect(request):
    """Redirects to the Shopify OAuth endpoint."""
    logger.info("Redirecting user to the Shopify OAuth endpoint.")
    shop = 'narrowcast'
    scope = settings.SHOPIFY_API_SCOPE
    redirect_uri = request.build_absolute_uri(reverse('shopify_connected'))
    permission_url = shopify.Session.create_permission_url(
        shop.strip(), scope, redirect_uri)
    return redirect(permission_url)


def shopify_connected(request):
    """Receives code from Shopify and exchanges it for access token."""
    logger.info("Received redirect from Shopify OAuth endpoint.")
    shop_url = request.REQUEST.get('shop')
    try:
        shopify_session = shopify.Session(shop_url, request.REQUEST)
    except shopify.ValidationException:
        messages.error(request, "Could not log in to Shopify store.")
        return redirect(reverse('shopify'))

    request.session['shopify'] = {
        "shop_url": shop_url,
        "access_token": shopify_session.token
    }
    messages.info(request, "Logged in to shopify store.")
    response = redirect(reverse('shopify_demo'))
    return response


@shop_login_required
def shopify_demo(request):
    """Renders the view for the Shopify demo."""
    products = shopify.Product.find()

    api = facebook.AdsAPI(
        os.environ['FACEBOOK_ACCESS_TOKEN'],
        settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
    ad_stats = api.get_stats_by_adaccount('16565898')

    return render_to_response('shopify_demo.html', {
        'products': products,
        'ad_stats': ad_stats['data'],
    }, context_instance=RequestContext(request))
