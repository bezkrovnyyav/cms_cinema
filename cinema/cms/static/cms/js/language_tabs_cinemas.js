function russian() {
    $("#ru").removeAttr().css('background-color', '#ddd');
    $('#uk').css('background-color', 'white');
    $('#title').text('Название кинотеатра');
    $("#id_title").attr('placeholder', 'Название кинотеатра');
    $('#description').text('Описание');
    $("#id_description").attr('placeholder', 'Описание');
    $('#conditions').text('Условия');
    $("#id_conditions").attr('placeholder', 'Условие');
}

function ukraine() {
    $('#ru').css('background-color', 'white');
    $('#uk').css('background-color', '#ddd');
    $('#title').text('Назва кінотеатру');
    $("#id_title").attr('placeholder', 'Назва кінотеатру');
    $('#description').text('Опис');
    $("#id_description").attr('placeholder', 'Опис');
    $('#conditions').text('Умови');
    $("#id_conditions").attr('placeholder', 'Умови');

}
