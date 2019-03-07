$('.multi-menu .title').click(
    function () {
        $(this).next().toggleClass('hide');
        $(this).parent().siblings().find('.body').addClass('hide')
    }
);