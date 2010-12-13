$(function () {

  var
    WAIT_SECONDS = 7,
    SLIDE_SECONDS = 1
  ;

  (function () {
    // Create a watermark in the search box.
    $('#search_q').watermark('Search');
  })();

  (function () {
    // Jump to comment if one was just posted.
    var commentRegexp = /\?c=(\d+)$/,
        commentId;
    if (commentRegexp.test(document.location.href)) {
        commentId = commentRegexp.exec(document.location.href)[1];
        document.location = document.location.href + '#c' + commentId;
    }
  })();

  (function () {
    // Hide message box(es) after seven seconds of waiting.
    setTimeout(function() {
        $('#site-messages').slideUp(SLIDE_SECONDS * 1000);
    }, WAIT_SECONDS * 1000);
  })();

  (function () {
    var snippetId = function (id) {
      var r = /wakacms-links-([\w\_-]+)/;
      return 'wakacms-snippet-' + r.exec(id)[1];
    };
    // Highlight wakacms content snippets whenever hoving over wakacms link.
    $('.wakacms-links')
      .mouseenter(function () {
        var highlightId = snippetId(this.id);
        $('#' + highlightId).addClass('wakacms-highlighted');
      })
      .mouseleave(function () {
        var highlightId = snippetId(this.id);
        $('#' + highlightId).removeClass('wakacms-highlighted');
      })
    ;
  })();

});
