function ukraine() {

    $('#ru').css('background-color', 'white')
    $('#uk').css('background-color', '#ddd')
    $('#title').text('Назва');
    $('#description').text('Опис')
    $('#id_title').attr('placeholder', 'Назва');
    $('#id_description').attr('placeholder', 'Опис')
}

function russian() {
    $('#ru').css('background-color', '#ddd')
    $('#uk').css('background-color', 'white')
    $('#title').text('Название');
    $('#description').text('Описание')
    $('#id_title').attr('placeholder', 'Название');
    $('#id_description').attr('placeholder', 'Описание')
}