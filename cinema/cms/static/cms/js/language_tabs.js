function russian(event) {
    const index = event.target.value;
    $("#ru-" + index).removeAttr().css('background-color', '#ddd');
    $('#uk-' + index).css('background-color', 'white');
    $('#title-' + index).text('Название кинотеатра');
    $("#id_" + index + "-title").attr('placeholder', 'Название кинотеатра');
    $('#address-' + index).text('Адресc');
    $("#id_" + index + "-address").attr('placeholder', 'Адресc');
    $('#coordinates-' + index).text('Координаты для карты');
    $("#id_" + index + "-coordinates").attr('placeholder', 'Координаты для карты');
}

function ukraine(event) {
    const index = event.target.value;
    $('#ru-' + index).css('background-color', 'white');
    $('#uk-' + index).css('background-color', '#ddd');
    $('#title-' + index).text('Назва кінотеатру');
    $("#id_" + index + "-title").attr('placeholder', 'Назва кінотеатру');
    $('#address-' + index).text('Адреса');
    $("#id_" + index + "-address").attr('placeholder', 'Адреса');
    $('#coordinates-' + index).text('Координати для карти');
    $("#id_" + index + "-coordinates").attr('placeholder', 'Координати для карти');

}




