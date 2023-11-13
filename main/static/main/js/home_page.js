$("#languages").on('change', function () {
    this.form.submit();
})

var myCarouselTop = $('#carouselTopBanner');
var intervalTop = Number(myCarouselTop.attr('value'));
if (intervalTop) {
    var carouselTop = new bootstrap.Carousel(myCarouselTop, {
        interval: intervalTop
    })
}


var myCarousel = $('#carouselNewsPromotions');
var interval = Number(myCarousel.attr('value'));
if (interval) {
    var carousel = new bootstrap.Carousel(myCarousel, {
        interval: interval
    })
}