function enable_submit(){
    $('#file-upload').change(
        function(){
            if ($(this).val()) {
                // $('input:submit').attr('disabled',false);
                $('#pimp-button').removeAttr('disabled');
            }
        }
    );
}


$(document).ready(
    enable_submit
);