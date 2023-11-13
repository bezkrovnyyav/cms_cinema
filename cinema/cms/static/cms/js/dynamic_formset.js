function validations_image(event, obj) {
    const index = obj.id;
    const file = event.target.files[0];
    var img = new Image();
    img.src = window.URL.createObjectURL(file);
    $("." + index).attr("src", window.URL.createObjectURL(file));

    // check width and height
    img.onload = function () {
        if (this.width != 1000 && this.height != 190) {
            $("#errors-" + index).css('display', 'block').attr("value", 'enabled');
            clean_errors();
            return false;

        } else {
            $("#errors-" + index).css('display', 'none').attr("value", 'disabled');
            clean_errors();

        }
    }
}

// check value in errors gallary
function clean_errors() {
    var element = $("[value=enabled]");
    if (element.length) {
        $("#sub").attr("disabled", "disabled");
        $("#sub2").attr("disabled", "disabled");
        $("#sub3").attr("disabled", "disabled");

    } else {
        $("#sub").removeAttr("disabled");
        $("#sub2").removeAttr("disabled");
        $("#sub3").removeAttr("disabled");


    }
}


$("#add-image").on('click', function () {
    const form_idx = $('#id_form-TOTAL_FORMS').val();
    $("#formset").append($('.empty_form').html().replace(/__prefix__/g, form_idx))
    $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})


function delete_image(event) {
    const index = event.target.id;
    document.getElementById('id_' + index + '-image').value = '';
    $("#" + index).css('display', 'none');
    $('.can-delete-list').append('<input type="hidden" value="on" name="' + index + '-DELETE" id="id_' + index + '-DELETE">');

    // validations_image if delete_image
    $("#errors-" + index).attr("value", 'disabled');
    clean_errors();
}

