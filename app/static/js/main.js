
$(document).ready(function($) {
    $('#instructions').toggle();

    $(".pop").on("click", function() {
       $('#pop-img').attr('src', $(this).attr('src'));
       $('#modal').modal('show');
    });

    $('#instructions-button').on('click', function() {
        $('#instructions').toggle();
    });

    $('#file-upload').change(
        function(){
            if ($(this).val()) {
                // $('input:submit').attr('disabled',false);
                $('#pimp-button').removeAttr('disabled');
            }
        }
    );
});