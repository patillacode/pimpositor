// $(function () {
$(document).ready(function() {
    // $("#logger").append("Entered...<br/>");
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
            // $("#logger").append(message);
        }
    });

    alert("Did faceDetection");

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
        // $("#logger").append("getting random image<br/>");
        var imageOptions = IMAGES[selector];
        var image = imageOptions[Math.floor(Math.random() * imageOptions.length)];
        return image;
    };

    var placeImages = function placeImages() {
        // $("#logger").append("Inserting corner images...<br/>");
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
        // $("#logger").append("html canvas<br/>");
        // document.body.appendChild(canvas);
        $("#original-img").hide();
        $("#pimped-img").append(convertCanvasToImage(canvas));
    });

});