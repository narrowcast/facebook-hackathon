/**
* shopify.js v0.1.0 by Chee-Hyung Yoon
* Copyright 2013 Narrowcast, Inc.
*
* Script for Shopify plugin.
*/
(function() {
  console.log("Shopify script tag is working on " + Shopify.shop + ".");

  function isCheckoutComplete() {
    // Check if checkout process is complete
    return (window.location.href.indexOf("checkout.shopify.com/orders") > -1);
  }

  function insertOffsitePixelFor(product) {
    // Send AJAX request to the Vimote server to get the pixel snippet
    var snippet = $.get("//facebook/snippet.js", product);

    if (snippet != null) {
      // Then append the offsite conversion pixel to the head
      var head = document.getElementsByTagName('head')[0];
      head.appendChild(snippet);
    }
  }

  if (typeof product !== 'undefined') {
    console.log("We are looking at product " + product.className + ".");
    // Insert Javascript code for key page view conversion
    //insertOffsitePixelFor(product, 'KEY_PAGE_VIEW');
  }
  if (isCheckoutComplete()) {
    // Insert Javascript code for checkout conversion
    console.log("A checkout conversion has occured!");
    //insertOffsitePixelFor(product, 'CHECKOUT');
  }
  $("form#add-item-form").submit(function(e) {
    // Product is added to cart, so register ADD_TO_CART conversion
    console.log("Product " + product.className + " is added to cart.");
    //insertOffsitePixelFor(product, 'ADD_TO_CART');
  });
})();
