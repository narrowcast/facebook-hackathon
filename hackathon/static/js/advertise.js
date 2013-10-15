/**
* advertise.js v0.1.0 by Chee-Hyung Yoon, Taenyon Kim
* Copyright 2013 Narrowcast, Inc.
*
* Script for Facebook advertise button.
*/
function advertise() {
  // Make an Ajax call to the server to create a page post and an ad
  //call create_product_ad(account_id, page_id, link, product_id, daily_budget, targeting):
}

$(document).ready(function() {
  var images = $('img');
  var image_index = 0;

  // X-editable: turn to inline mode
  //$.fn.editable.defaults.mode = 'inline';
  // Make elements editable with X-editable
  $('.editable').editable();

  // Enable typeahead for connecting a Facebook page
  $("#facebook-page").typeahead({
    name: 'facebook-pages',
    prefetch: '/facebook/pages.json',
    valueKey: 'name',
    template: [
      '<div class="page-typeahead">',
      '<img class="page-picture" src="{{picture.data.url}}" />',
      '<p class="page-name">{{name}}</p>',
      '<p class="page-category">{{category}}</p>',
      '<p class="page-likes">{{likes}}</p>',
      '</div>'
    ].join(''),
    engine: Hogan,
  });

  // Set page post headline and caption
  var title = $('title').text();

  if (title.length > 0) {
    $('.post-headline a.editable').text(title.substring(0, 25));
    $('.post-headline a.editable').attr('href', document.URL);
    $('.post-caption a.editable').text(window.location.hostname);
  }
  // Set page post text
  var text = $('p').text();
  if (text.length > 0) {
    $('.post-text').text(text.substring(0, 90));
  }
  // Set page post image
  if (images.length > 0) {
    $('img.post-image').attr('src', images[image_index]['src']);
  }
  // Buttons for changing image
  $('.btn-left').click(function(){
    if (image_index > 0) {
      $('img.post-image').attr('src', images[--image_index]['src']);
    }
  });
  $('.btn-right').click(function(){
    if (image_index <= images.length) {
      $('img.post-image').attr('src', images[++image_index]['src']);
    }
  });
});
