$(function () {

  var stripPrefix = function(str, prefix) {
    if (str.indexOf(prefix) === 0) {
      return str.substr(prefix.length);
    } else {
      return str;
    }
  }

  var submitVote = function(event, direction, prefix) {
    var $form,
        $otherform,
        $img,
        $otherimg,
        $score,
        objectId,
        otherDirection,
        voteInfo,
        voteAction,
        newVoteAction,
        newImageVotedState;

    if (direction == 'up') {
      otherDirection = 'down';
    } else if (direction == 'down') {
      otherDirection = 'up';
    }

    $form = $(event.target);
    objectId = stripPrefix($form.attr('id'), prefix);
    $.post($form.attr('action'), function (data) {
      voteInfo = $.parseJSON(data);
      if (voteInfo.success === true) {
        voteAction = /(up|down|clear)\/$/.exec($form.attr('action'))[1];
        $score = $('#votescore-' + objectId);
        $img = $('#vote' + direction + 'arrow-' + objectId);
        $otherimg = $('#vote' + otherDirection + 'arrow-' + objectId);
        $otherform = $('#vote' + otherDirection + '-' + objectId);
        if (direction == 'up') {
          if (voteAction == 'clear') {
            newVoteAction = '/up/';
            newImageVotedState = false;
          } else {
            newVoteAction = '/clear/';
            newImageVotedState = true;
          }
        } else if (direction == 'down') {
          if (voteAction == 'clear') {
            newVoteAction = '/down/';
            newImageVotedState = false;
          } else {
            newVoteAction = '/clear/';
            newImageVotedState = true;
          }
        }
        // Clear or set voting image.
        if (newImageVotedState) {
          $img.attr('src', $img.attr('src').replace(/_plain.png$/, '_voted.png'));
          if (voteAction !== 'clear') {
            $otherimg.attr('src', $otherimg.attr('src').replace(/_voted.png$/, '_plain.png'));
          } else {
            $otherimg.attr('src', $otherimg.attr('src').replace(/_voted.png$/, '_plain.png'));
          }
        } else {
          $img.attr('src', $img.attr('src').replace(/_voted.png$/, '_plain.png'));
          if (voteAction !== 'clear') {
            $otherimg.attr('src', $otherimg.attr('src').replace(/_plain.png$/, '_voted.png'));
          } else {
            $otherimg.attr('src', $otherimg.attr('src').replace(/_voted.png$/, '_plain.png'));
          }
        }
        // Set new form action.
        $form.attr('action', $form.attr('action').replace(/\/(up|down|clear)\/$/, newVoteAction));
        $otherform.attr('action', $otherform.attr('action').replace(/\/(up|down|clear)\/$/, '/' + otherDirection + '/'));
        // Set new score.
        $score.text(voteInfo.score.score.toString());
      }
    });
    return false;
  }

  $('[id|=voteup]').submit(function (event) {
    return submitVote(event, 'up', 'voteup-');
  });

  $('[id|=votedown]').submit(function (event) {
    return submitVote(event, 'down', 'votedown-');
  });

});
