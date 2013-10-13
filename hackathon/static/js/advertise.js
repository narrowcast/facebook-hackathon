$(document).ready(function() {
  var images = $('img');
  var image_index = 0;

  // Turn to inline mode
  // $.fn.editable.defaults.mode = 'inline';
  // Make elements editable with X-editable
  $('.editable').editable();

  function changeThumbnail(index) {
    $('img.ad_thumbnail').attr('src', images[index]['src']);
  }
  // set headline & site domain
  var title = $('title').text();
  console.log(title);
  if (title.length > 0) {
    $('.headline').text(title.substring(0, 25));
    $('.headline').attr('href', document.URL);
    $('.caption').text(window.location.hostname);
  }
  // set ad text
  var text = $('p').text();
  console.log(text);
  if (text.length > 0) {
    $('.text').text(text.substring(0, 90));
  }
  // set ad preview thumbnail
  if (images.length > 0) {
    changeThumbnail(image_index);    
  }
  // Buttons for changing image
  $('.btn-left').click(function(){
    if (image_index > 0) {
      changeThumbnail(--image_index);
    }
  });
  $('.btn-right').click(function(){
    if (image_index <= images.length) {
      changeThumbnail(++image_index);
    }
  });  
});
