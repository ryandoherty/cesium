function Warning() {
    Warning.prototype.addWarning = function(selector) {
        $(selector).click(function() {
            var resp = confirm("Are you sure you want to remove this page?");
            if (!resp)
                return false;
        });
    }
}
