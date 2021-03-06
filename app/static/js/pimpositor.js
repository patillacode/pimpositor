/**
 * Copyright (C) 2015 Pimpositor
 * based on code by Piers Olenski copyright (C) 2015 get-rekt-facial-recognition
 * License: http://www.gnu.org/licenses/gpl.html GPL version 2 or higher
 * Extension to https://github.com/superfunkminister/get-rekt-facial-recognition/
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


$(document).ready(function() {
    $('#picture').faceDetection({
        complete: function (faces) {
            for (var i = 0; i < faces.length; i++) {
                $('<div>', {
                    'class':'face',
                    'css': {
                        'position': 'absolute',
                        'left':     faces[i].x * faces[i].scaleX + 'px',
                        'top':      faces[i].y * faces[i].scaleY + 'px',
                        'width':    faces[i].width  * faces[i].scaleX + 'px',
                        'height':   faces[i].height * faces[i].scaleY + 'px'
                    }
                })
                .insertAfter(this);
            }
        },
        error:function (code, message) {
            console.log('Error in face Detection: ' + message);
        }
    });

    const IMAGES = {
        "top-left": [
            "windows95.png",
            "doritos.gif",
            "mountain-dew.png",
            "rekt.png"
        ],
        "top-right": [
            "pingu.png",
            "illuminati.png",
            "mlg.jpg",
            "doge.png"
        ],
        "bottom-left": [
            "thomas.png",
            "snoop.gif",
            "frog.gif",
            "gun.png"
        ]
    };

    var getRandomImage = function getRandomImage(selector) {
        var imageOptions = IMAGES[selector];
        var image = imageOptions[Math.floor(Math.random() * imageOptions.length)];
        return image;
    };

    var placeImages = function placeImages() {
        Object.keys(IMAGES).forEach(function(selector){
            $("<img>", {
                "class": selector,
                "src": "/static/img/" + getRandomImage(selector)
            }).insertAfter("#picture");
        });
    };

    placeImages();

    // Converts canvas to an image
    function convertCanvasToImage(canvas) {
        var image = new Image();

        // TODO: resize the canvas so the pimped image to be created
        // with its original size
        // context = canvas.getContext('2d');
        // canvas.width = original_width;
        // canvas.height = original_height;

        // context.drawImage(image, 0, 0, canvas.width, canvas.height);

        image.src = canvas.toDataURL("image/png");
        return image;
    }

    html2canvas(document.body).then(function(canvas) {
        // document.body.appendChild(canvas);
        $("#original-img").hide();
        $("#pimped-img").append(convertCanvasToImage(canvas));
    });

});