import logging

import facebook
import shopify

logger = logging.getLogger(__name__)


def create_product_ad(account_id, page_id, link, product_id, daily_budget,
                      targeting):
    """
    Creates an unpublished page post and an ad campaign and ads for it. It also
    creates offsite conversion pixels for the ads.
    """
    logging.info("Creating page post link ad for the product %s" % product_id)

    # 1. Creates an unpublished link page post
    response = api.create_link_page_post(page_id, link)
    story_id = response['id']

    # 2. Creates offsite conversion pixels for the campaign
    response = api.create_offsite_pixel(account_id, name, tag)
    offsite_pixel_id = response['id']
    conversion_specs = [{"action.type": ["offsite_conversion"],
                         "offsite_pixel": [offsite_pixel_id]}]

    # 3. Creates an ad campaign and ads using the link page post
    response = api.create_adcamapign(account_id, name, 1, daily_budget)
    adcampaign_id = response['id']    
    response = api.create_adcreative_type_27(
        account_id, page_id, story_id=story_id, name=name)
    adcreative_id = response['id']    
    response = api.create_adgroup(
        account_id, name, 'ABSOLUTE_OCPM', {'ACTIONS': 1000},
        adcampaign_id, adcreative_id, targeting, conversion_specs)
    return response
