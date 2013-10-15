/**
* advertise.js v0.1.0 by Chee-Hyung Yoon, Taenyon Kim
* Copyright 2013 Narrowcast, Inc.
*
* Script for Facebook advertise button.
*/
$(document).ready(function() {
  var images = $("img");
  var image_index = 0;

  // Set page post headline and caption
  var title = $("title").text();

  if (title.length > 0) {
    $(".post-headline a.editable").text(title.substring(0, 25));
    $(".post-headline a.editable").attr('href', document.URL);
    $(".post-caption a.editable").text(window.location.hostname);
  }
  // Set page post text
  var text = $("p").text();
  if (text.length > 0) {
    $(".post-text").text(text.substring(0, 90));
  }
  // Set page post image
  if (images.length > 0) {
    $("img.post-image").attr('src', images[image_index]['src']);
  }
  // Set link url
  $("input#link-url").val(document.URL);
  // Register buttons for changing image
  $(".btn-left").click(function(){
    if (image_index > 0) {
      $("img.post-image").attr('src', images[--image_index]['src']);
    }
  });
  $(".btn-right").click(function(){
    if (image_index <= images.length) {
      $('img.post-image').attr('src', images[++image_index]['src']);
    }
  });
  // Make elements editable with X-editable
  $(".editable").editable({
    'highlight': false,
    'unsavedclass': null,
  });
  // Enable typeahead for connecting a Facebook page
  $("#facebook-page").typeahead({
    name: 'facebook-pages',
    prefetch: '/facebook/pages.json',
    valueKey: 'name',
    template: [
      '<div class="page-typeahead">',
      '<img class="page-picture" src="{{picture.data.url}}" />',
      '<div class="page-info">',
      '<p class="page-name">{{name}}</p>',
      '<p class="page-category">{{category}}</p>',
      '<p class="page-likes">{{likes}} likes</p>',
      '</div>',
      '</div>',
    ].join(''),
    engine: Hogan,
  }).on('typeahead:selected', function(e, v) {
    // Update Page name and picture on select
    console.log(v.id);
    $("input#page-id").val(v.id);
    $("h5.page-name").text(v.name);
    $("img.page-picture").attr('src', v.picture.data.url);
  });
});
