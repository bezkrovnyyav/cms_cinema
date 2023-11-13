$("#add-contacts").on("click", function () {
    const form_idx = $('#id_form-TOTAL_FORMS').val();
    $("#formset").append($('.empty_form').html().replace(/__prefix__/g, form_idx))
    $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})

function load_logo(event, obj) {
    const index = obj.id;
    const file = event.target.files[0];
    $("." + index).attr("src", window.URL.createObjectURL(file));
}
