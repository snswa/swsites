(function ($) {
    var DEBUG = false;
    function trace(s) {
        if (DEBUG) {
            try { console.log(s) } catch (e) { alert(s) }
        };
    };

    var minPoll = 10000,
        maxPoll = 60000,
        pollFactor = 1.25,
        currentPoll = 10000,
        currentTimeout,
        updateItems;

    // Detach forms and attach to item types as original.
    $('.topic .item-type').each(function() {
        var $itemtype = $(this),
            $form = $itemtype.find('.form');
        $form.detach();
        $itemtype.data('originalform', $form.html());
    });

    updateItems = function () {
        var date = (new Date()).getTime();
        // Find URL from current top-most item.
        var url = $('#items .item:first a.items-after').attr('href');
        if (typeof currentTimeout !== undefined) {
            clearTimeout(currentTimeout);
        }
        if (url) {
            url += (url.indexOf('?') != -1 ? '&' : '?') + date;
            trace('requesting url ' + url);
            $.ajax({
                type: 'GET',
                url: url,
                success: function (data) {
                    data = $.trim(data);
                    trace('data.length is ' + data.length);
                    if (data.length > 0) {
                        $('<div style="display:none">' + data + '</div>')
                            .prependTo('#items ul:first')
                            .slideDown('slow')
                        ;
                        currentPoll = minPoll;
                    } else {
                        currentPoll = Math.min(currentPoll * pollFactor, maxPoll);
                    }
                    currentTimeout = setTimeout(updateItems, currentPoll);
                },
                error: function (req, status) {
                    trace('updateItems error, status ' + status);
                }
            });
        }
    };

    setTimeout(updateItems, currentPoll);

    $('.topic .item-type .label a').live('click', function (event) {
        var $itemtype = $(event.target).parents('.item-type'),
            $form = $itemtype.find('.form');
        // Hide all other forms first as needed.
        $('.topic .item-type .form').each(function () {
            var $candidate = $(this);
            if ($candidate != $form && $candidate.find(':visible').length > 0) {
                $candidate.slideUp('fast', function () { $candidate.remove(); });
            }
        });
        // Now show or hide this one.
        if ($form.find(':visible').length > 0) {
            // hide and remove
            $form.slideUp('fast', function () { $form.remove(); });
        } else {
            // clone and show.  generate from html for proper event hookups.
            $form = $('<div class="form">' + $itemtype.data('originalform') + '</div>');
            $form.hide().appendTo($itemtype).slideDown('fast');
            $form.find(':input:first[type!="hidden"]').focus();
        }
        return false;
    });

    $('.topic .item-type .form').live('submit', function (event) {
        var $form = $(event.target);
        if (!$form.is('form')) {
            // on IE, it's not the form that's submitted, it's
            // the submit button itself.
            $form = $form.parents('form');
        }
        $.ajax({
            type: 'POST',
            url: $form.attr('action'),
            data: $form.serialize(),
            success: function (data) {
                var $formparent;
                if (data == '1') {
                    $form.slideUp('slow');
                    updateItems();
                } else {
                    $formparent = $form.parent();
                    $form.remove();
                    $formparent.append(data);
                    $formparent.find('form :input:first[type!="hidden"]').focus();
                }
            },
            error: function (req, status) {
                trace('Error when submitting, status is ' + status);
            }
        });
        return false;
    });
})(jQuery);
