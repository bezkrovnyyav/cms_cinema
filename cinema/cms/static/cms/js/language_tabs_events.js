function ukraine() {

    $('#ru').css('background-color', 'white')
    $('#uk').css('background-color', '#ddd')
    $('#title_promotions').text('Назва Акції');
    $('#title_news').text('Назва Новини');
    $('#date').text('Дата публікації');
    $('#description').text('Опис');
    $('#id_title').attr('placeholder', 'Назва');
    $('#id_description').attr('placeholder', 'Опис')
}

function russian() {
    $('#ru').css('background-color', '#ddd')
    $('#uk').css('background-color', 'white')
    $('#title_promotions').text('Название Акции');
    $('#title_news').text('Название Новости');
    $('#date').text('Дата публикации');
    $('#description').text('Описание')
    $('#id_title').attr('placeholder', 'Название');
    $('#id_description').attr('placeholder', 'Описание')
}