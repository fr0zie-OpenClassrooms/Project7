$(document).ready(function () {
    $('form').on('submit', function (event) {
        event.preventDefault();
        $.ajax({
            data: {
                question: $('#question').val(),
            },
            type: 'GET',
            url: '/data'
        }).done(function (data) {
            dialogue = $("<section></section>");
            dialogue.addClass("col-12 dialogue");
            dialogue.html(data);
            dialogue.appendTo("#answer");
        });
    });
});