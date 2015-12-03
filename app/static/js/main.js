/**
 * Copyright (C) 2015 Pimpositor
 * License: http://www.gnu.org/licenses/gpl.html GPL version 2 or higher
 *
 * Some open source application is free software: you can redistribute
 * it and/or modify it under the terms of the GNU General Public
 * License as published by the Free Software Foundation, either
 * version 3 of the License, or (at your option) any later version.
 *
 * Some open source application is distributed in the hope that it will
 * be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
 * of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * <http://www.gnu.org/licenses/>.
 *
 * @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>
 */

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