$(document).ready(function () {
    $('#form').on('submit', (function (event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        $.ajax({
            data: {
                question: $("#question").val()
            },
            type: 'GET',
            url: '/result',
            success: showResult
        });
    }));

    function showResult(result) {
        clone = $($('#result').html());
        $('.alert', clone).addClass(result.status);
        $('.address', clone).text(result.address);
        $('.extract', clone).text(result.extract);
        $('.question', clone).text(result.question);
        clone.appendTo("#answer");
    }
});
