// ==UserScript==
// @name         img2pdf
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  save jpeg and png in the site to the pdf
// @author       kimotu
// @include      https://*
// @grant        none

// @require https://code.jquery.com/jquery-3.5.1.min.js
// @require https://github.com/foliojs/pdfkit/releases/download/v0.11.0/pdfkit.standalone.js
// @require https://github.com/devongovett/blob-stream/releases/download/v0.1.3/blob-stream.js

// ==/UserScript==


(() => {
    'use strict';

    var imgs = [];
    var urls = [];

    $('a[href]').filter((i,e) => {
        let ext = e['href'].split('.').pop();
        return ext == "jpeg" || ext == "jpg" || ext == "png";
    }).each((i,e) =>
        urls.push(e['href'])
    );

    $('img[src]').filter((i,e) => {
        let ext = e['src'].split('.').pop();
        return ext == "jpeg" || ext == "jpg" || ext == "png";
    }).each((i,e) =>
        urls.push(e['src'])
    );

    var pdf = new PDFDocument({autoFirstPage:false});
    const stream = pdf.pipe(blobStream());

    var canvas = document.createElement("canvas");
    var ctx = canvas.getContext("2d");
    var img = new Image();

    for (let url of urls) {
        img.src = url;
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);

        let ext = url.split('.').pop();
        var dataurl = "";

        if (ext == "jpg" || ext == "jpeg") {
            dataurl = canvas.toDataURL('image/jpeg');
        } else {
            dataurl = canvas.toDataURL();
        }

        pdf.addPage({size: [img.width, img.height]});
        pdf.image(dataurl, 0, 0);
    }

    pdf.end();

    stream.on('finish', () =>
        window.open(stream.toBlobURL('application/pdf'))
    );

})();