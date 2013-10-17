import json
import logging
import os

import facebook
import shopify

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from hackathon.decorators import shop_login_required

logger = logging.getLogger(__name__)


class AdvertiseView(TemplateView):
    """View for rendering the advertise button page."""
    template_name = "advertise.html"

def advertise_demo(request):
    return render_to_response('qbrandagency_mod.html', {
    }, context_instance=RequestContext(request))

def advertise_demo_success(request):
    return render_to_response('qbrandagency_mod_success.html', {
    }, context_instance=RequestContext(request))

def facebook_pages(request):
    """Returns the pages data for the given user as JSON."""
    logger.info("Returning the Facebook pages for the user.")
    api = facebook.AdsAPI(
        os.environ['FACEBOOK_ACCESS_TOKEN'],
        settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
    user_pages = api.get_user_pages(
        '214012', ['category', 'name', 'picture', 'likes', 'access_token'])
    for page in user_pages['data']:
        page['tokens'] = page['name'].split()
    json_data = json.dumps(user_pages['data'])
    return HttpResponse(json_data, mimetype='application/json')


def facebook_snippets(request):
    """Returns the offsite pixel code with the given name and the tag."""
    logger.info("Getting conversion pixel from Facebook.")
    if  'name' not in request.GET or 'tag' not in request.GET:
        raise Http404
    name = request.GET['name']
    tag = request.GET['tag']
    api = facebook.AdsAPI(
        os.environ['FACEBOOK_ACCESS_TOKEN'],
        settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
    offsite_pixels = api.get_offsite_pixels('16565898')
    for pixel in offsite_pixels['data']:
        if pixel['name'] == name and pixel['tag'] == tag:
            json_data = json.dumps(pixel['js_pixel'])
            return HttpResponse(json_data, mimetype='application/json')
    raise Http404


def create_product_ad(account_id, page_id, link, message, picture, name,
                      caption, description, product_id, daily_budget,
                      targeting):
    """
    Creates an unpublished page post and an ad campaign and ads for it. It also
    creates offsite conversion pixels for the ads.
    """
    logger.info("Creating page post link ad for the product %s" % product_id)
    api = facebook.AdsAPI(
        os.environ['FACEBOOK_ACCESS_TOKEN'],
        settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)

    # 1. Creates an unpublished link page post
    response = api.create_link_page_post(
        page_id, link, message.encode('utf-8'), picture, name,
        caption.encode('utf-8'), description.encode('utf-8'))
    logger.info("Got response %s while creating link page post" % response)
    page_post_id = response['id']
    story_id = page_post_id.split('_')[-1]

    # 2. Creates offsite conversion pixels for the campaign
    response = api.create_offsite_pixel(account_id, link, 'KEY_PAGE_VIEW')
    logger.info("Got response %s while creating offsite pixel" % response)
    offsite_pixel_id = response
    conversion_specs = [{"action.type": ["offsite_conversion"],
                         "offsite_pixel": [offsite_pixel_id]}]

    # 3. Creates an ad campaign and ads using the link page post
    response = api.create_adcampaign(account_id, link, 1, daily_budget)
    logger.info("Got response %s while creating ad campaign" % response)
    adcampaign_id = response['id']
    response = api.create_adcreative_type_27(
        account_id, page_id, story_id=story_id, name=link)
    logger.info("Got response %s while creating ad creative" % response)
    adcreative_id = response['id']
    response = api.create_adgroup(
        account_id, link, 'ABSOLUTE_OCPM', {'ACTIONS': 1000},
        adcampaign_id, adcreative_id, targeting, conversion_specs)
    logger.info("Got response %s while creating ad group" % response)
    return response


@csrf_exempt
def facebook_advertise(request):
    """On advertising form submit, creates the page post and the ad."""
    if request.method == 'POST':
        link_url = request.POST['link_url']
        page_id = request.POST['page_id']
        post_text = request.POST['post_text']
        post_image_url = request.POST['post_image_url']
        post_headline = request.POST['post_headline']
        post_caption = request.POST['post_caption']
        post_description = request.POST['post_description']
        audience = request.POST['audience']
        budget = request.POST['budget']
        targeting = {'countries': ['KR']}
        response = create_product_ad(
            '16565898', page_id, link_url, post_text, post_image_url,
            post_headline, post_caption, post_description,
            'product_id', 1000, targeting)
        return HttpResponseRedirect('/thanks/')
    else:
        raise Http404


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
    # Activate session and install script tag at this point
    shopify.ShopifyResource.activate_session(shopify_session)
    script_tag = shopify.ScriptTag()
    script_tag.event = 'onload'
    script_tag.src = '//localhost:8000/static/js/shopify.js'
    if script_tag.save():
        logger.info("Successfully installed script tag: %s" % script_tag)
    else:
        logger.error("Error while installing script tag: %s" % script_tag)

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
