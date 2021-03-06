define('cli', [], function() {
    'use strict';

    var $progress = $('#progress');

    return {
        hasTouch: ('ontouchstart' in window) ||
                   window.DocumentTouch &&
                   document instanceof DocumentTouch,
        bodyData: $('body').data(),
        showProgress: function(msg) {
            if ($progress.length) {
                msg = msg || this.bodyData.loadingMsg;
                $progress.find('.txt').text(msg);
                $progress.show();
            }
        },
        hideProgress: function() {
            if ($progress.length) {
                $progress.hide();
            }
        },
        focusOnPin: function(config) {
            config = config || {};
            var $form = config.$form || $('#pin');
            var $toHide = config.$toHide || null;
            var $toFadeIn = config.$toFadeIn || null;
            var $pinBox = $form.find('.pinbox');
            var $input = $form.find('input[name="pin"]');
            if ($toHide && $toHide.length) {
                $toHide.hide();
            }
            this.hideProgress();
            if ($toFadeIn && $toFadeIn.length) {
                $toFadeIn.fadeIn();
            }
            if (!$pinBox.hasClass('error')) {
                console.log('[cli] Focusing pin');
                $input.focus();
            }
        }
    };
});
