function banner_valid(event) {
    const file = event.target.files[0];
    var img = new Image();
    img.src = window.URL.createObjectURL(file);
    $("#background").attr("src", window.URL.createObjectURL(file));

    // check width and height
    img.onload = function () {
        if (this.width != 3000 && this.height != 2000) {
            $(".errorlist").css('display', 'block').attr("value", 'enabled');
            clean_errors();
            return false;

        } else {
            $(".errorlist").css('display', 'none').attr("value", 'disabled');
            clean_errors();
        }
    }
}


// banner_valid if delete_banner
function delete_banner() {
    $(".errorlist").css('display', 'none').attr("value", 'disabled');
    clean_errors();
}
