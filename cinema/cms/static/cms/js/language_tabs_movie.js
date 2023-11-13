function russian() {
    $("#ru").removeAttr().css('background-color', '#ddd');
    $('#uk').css('background-color', 'white');
    $('#title').text('Название фильма');
    $("#id_title").attr('placeholder', 'Название фильма');
    $('#description').text('Описание');
    $("#id_description").attr('placeholder', 'Описание');

}

function ukraine() {
    $('#ru').css('background-color', 'white');
    $('#uk').css('background-color', '#ddd');
    $('#title').text('Назва фильму');
    $("#id_title").attr('placeholder', 'Назва фильму');
    $('#description').text('Опис');
    $("#id_description").attr('placeholder', 'Опис');


}
