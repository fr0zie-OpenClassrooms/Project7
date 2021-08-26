$(document).ready(function () {
    $('#form').on('submit', function (event) {
        event.stopImmediatePropagation();
        event.preventDefault();
        $.ajax({
            data: {
                question: $('#question').val(),
            },
            type: 'GET',
            url: '/result'
        }).done(create_message);
    });
});

function create_message(result) {
    section = $("#result").children().clone();
    $('.alert', section).addClass(result.status);
    $('.address', section).text(result.address);
    $('.extract', section).text(result.extract);
    $('.question', section).text(result.question);
    section.appendTo("#answer");
}