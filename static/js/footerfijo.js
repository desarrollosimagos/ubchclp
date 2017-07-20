/*
fuente: 
http://www.drupalcoder.com/blog/cross-browser-sticky-footer-with-fluid-height-using-jquery
*/
// sticky footer plugin
(function($){
  var footer;
 
  $.fn.extend({
    stickyFooter: function(options) {
      footer = this;
       
      positionFooter();
 
      $(window)
        .scroll(positionFooter)
        .resize(positionFooter);
 
      function positionFooter() {
        var docHeight = $(document.body).height() - $("#sticky-footer-push").height();
        if(docHeight < $(window).height()){
          var diff = $(window).height() - docHeight;
          if (!$("#sticky-footer-push").length > 0) {
            $(footer).before('<div id="sticky-footer-push"></div>');
          }
          $("#sticky-footer-push").height(diff);
        }
      }
    }
  });
})(jQuery);

$(document).ready(function() {
  positionFooter();
   
  $(window)
    .scroll(positionFooter)
    .resize(positionFooter);
   
  function positionFooter() {
    var docHeight = $(document.body).height() - $("#sticky-footer-push").height();
    if(docHeight < $(window).height()){
      var diff = $(window).height() - docHeight;
      if (!$("#sticky-footer-push").length > 0) {
        $("#footer").before('<div id="sticky-footer-push"></div>');
      }
      $("#sticky-footer-push").height(diff);
    }
  }
});

$("#footer").stickyFooter();