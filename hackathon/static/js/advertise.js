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
    $("input#post-headline").val(title.substring(0, 25));
    $(".post-headline a.editable").attr('href', document.URL);
    $(".post-caption a.editable").text(window.location.hostname);
    $("input#post-caption").val(window.location.hostname);
  }
  $(".post-headline").editable({
    type: 'text',
    success: function(response, newValue) {
      $("input#post-headline").val(newValue);
    }
  });
  $(".post-caption").editable({
    type: 'text',
    success: function(response, newValue) {
      $("input#post-caption").val(newValue);
    }
  });
  $(".post-description").editable({
    type: 'text',
    success: function(response, newValue) {
      $("input#post-description").val(newValue);
    }
  });
  // Set page post text
  var text = $("p").text();

  if (text.length > 0) {
    $("p.post-text").text(text.substring(0, 90));
    $("input#post-text").val(text.substring(0, 90));
  }
  $(".post-text").editable({
    type: 'textarea',
    success: function(response, newValue) {
      $("input#post-text").val(newValue);
    }
  });
  // Set page post image
  if (images.length > 0) {
    $("img.post-image").attr('src', images[image_index]['src']);
    $("input#post-image-url").val(images[image_index]['src']);
  }
  // Set link url
  $("input#link-url").val(document.URL);
  // Register buttons for changing image
  $(".btn-left").click(function(){
    if (image_index > 0) {
      $("img.post-image").attr('src', images[--image_index]['src']);
      $("input#post-image-url").val(images[image_index]['src']);
    }
  });
  $(".btn-right").click(function(){
    if (image_index < images.length - 1) {
      $('img.post-image').attr('src', images[++image_index]['src']);
      $("input#post-image-url").val(images[image_index]['src']);
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
