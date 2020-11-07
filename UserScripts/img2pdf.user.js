// ==UserScript==
// @name         img2pdf
// @namespace    http://tampermonkey.net/
// @version      1.2.0
// @description  save jpeg and png in the site to the pdf
// @author       kimotu
// @include      https://*
// @grant        none
// @updateURL    https://github.com/kimotu4632uz/Fragment/raw/master/UserScripts/img2pdf.user.js
// @downloadURL  https://github.com/kimotu4632uz/Fragment/raw/master/UserScripts/img2pdf.user.js

// @require https://code.jquery.com/jquery-3.5.1.min.js
// @require https://github.com/foliojs/pdfkit/releases/download/v0.11.0/pdfkit.standalone.js
// @require https://github.com/devongovett/blob-stream/releases/download/v0.1.3/blob-stream.js

// ==/UserScript==

function setLoadAllCallback(elems, callback) {
    var count = 0;
    for (let elem of elems) {
        elem.onload = () => {
            count++;
            if (count == elems.length) {
                callback(elems);
            }
        };
    }
}

(() => {
    'use strict';

    var imgs = [];
    var urls = [];

    $('a[href]').filter((i,e) => {
        let ext = e['href'].split('.').pop();
        return ext == "jpeg" || ext == "jpg" || ext == "png";
    }).each((i,e) => {
        if (!urls.includes(e['href'])) {
            urls.push(e['href']);
        }
    });

    $('img[src]').filter((i,e) => {
        let ext = e['src'].split('.').pop();
        return ext == "jpeg" || ext == "jpg" || ext == "png";
    }).each((i,e) => {
        if (!urls.includes(e['src'])) {
            urls.push(e['src']);
        }
    });

    var pdf = new PDFDocument({autoFirstPage:false});
    const stream = pdf.pipe(blobStream());

    var canvas = document.createElement("canvas");
    var ctx = canvas.getContext("2d");

    let fst = true;

    for (let url of urls) {
        var img = new Image();
        imgs.push(img);
    }

    setLoadAllCallback(imgs, (elems) => {
        for (let img of elems) {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);

            let ext = img.src.split('.').pop();
            var dataurl = "";

            if (ext == "jpg" || ext == "jpeg") {
                dataurl = canvas.toDataURL('image/jpeg');
            } else {
                dataurl = canvas.toDataURL();
            }


            if (img.height > 700) {
                pdf.addPage({size: [img.width, img.height]});

                if (fst) {
                    pdf.image(dataurl, 0, 0).link(0, 0, img.width, img.height, window.location.href);
                    fst = false;
                } else {
                    pdf.image(dataurl, 0, 0);
                }
            }
        }

        pdf.end();

        stream.on('finish', () =>
            window.open(stream.toBlobURL('application/pdf'))
        );
    });

    for (var i=0;i<urls.length; i++) {
        imgs[i].src = urls[i];
    }

})();

