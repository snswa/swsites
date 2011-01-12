(function ($) {
    var DEBUG = false;
    if (!DEBUG && $.browser.msie) {
        // Just skip IE for now.  :-/
        return;
    }
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
        updateItems,
        itemTypeLinksActive = true;

    // Detach forms and attach to item types as original.
    $('.topic .item-type').each(function() {
        var $itemType = $(this),
            $form = $itemType.find('.form');
        $form.detach();
        $itemType.data('originalform', $form.html());
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
        if (!itemTypeLinksActive) {
            return false;
        }

        var $itemType = $(event.target).parents('.item-type'),
            $form = $itemType.find('.form');

        // Hide all other item types.
        $('.topic .item-type').each(function () {
            var $candidate = $(this);
            if (this != $itemType[0]) {
                $candidate.slideUp('fast', function () {
                    // Remove any form copies that may exist, for good measure.
                    $candidate.find('.form').remove();
                });
            }
        });

        // Now clone and show the form for this item type.
        $form = $('<div class="form">' + $itemType.data('originalform') + '</div>');
        $form.hide().appendTo($itemType).slideDown('fast');
        $form.find(':input:first[type!="hidden"]').focus();
        itemTypeLinksActive = false;

        return false;
    });

    // When cancel clicked, slide up this form, and make all other content types visible.
    $('.topic .item-type .form a.cancel').live('click', function (event) {
        var $itemType = $(event.target).parents('.item-type'),
            $form = $itemType.find('.form');
        $form.slideUp('fast', function () { $form.remove(); });
        $('.topic .item-type').each(function () {
            var $candidate = $(this);
            if (this != $itemType[0]) {
                $candidate.slideDown('fast');
            }
        });
        itemTypeLinksActive = true;
        return false;
    });

    $('.topic .item-type form').live('submit', function (event) {
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
                var $formDiv,
                    $formItemType,
                    $formParent;
                if (data == '1') {
                    // Successful submit.  Destroy the form, and show other item types.
                    $formDiv = $form.parent('.form');
                    $formDiv.slideUp('slow', function () { $formDiv.remove(); });
                    $formItemType = $form.parent('.item-type');
                    $('.topic .item-type').each(function () {
                        var $candidate = $(this);
                        if (this != $formItemType[0]) {
                            $candidate.slideDown('fast');
                        }
                    });
                    itemTypeLinksActive = true;
                    updateItems();
                } else {
                    // Unsuccessful; replace the form with the snippet received from the server.
                    $formParent = $form.parent();
                    $form.remove();
                    $formParent.append(data);
                    $formParent.find('form :input:first[type!="hidden"]').focus();
                }
            },
            error: function (req, status) {
                trace('Error when submitting, status is ' + status);
            }
        });
        return false;
    });
})(jQuery);
