// ==UserScript==
// @name         img2pdf
// @namespace    http://tampermonkey.net/
// @version      1.0.8
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

    var urldic = {};

    for (let url of urls) {
        let parts = new URL(url);
        urldic[parts.pathname.split('/').pop()] = url;
    }

    var groups = [];
    var grouped = [];

    for (let url in urldic) {
        if (grouped.includes(url)) {
            continue;
        }

        let temp = new RegExp('^' + url.replace(/\d+/g, '\\d+') + '$', 'u');
        var comp = [];

        for (let comped in urldic) {
            if (temp.test(comped)) {
                comp.push(urldic[comped]);
                grouped.push(comped);
            }
        }

        groups.push(comp);
    }

    groups.sort((a,b) => 
        b.length - a.length
    );

    var urls = groups[0].sort((a,b) => 
        a.match(/\d+/g).join('') - b.match(/\d+/g).join('')
    );
    console.log(groups);
    console.log(urls);

    var pdf = new PDFDocument({autoFirstPage:false});
    const stream = pdf.pipe(blobStream());

    var canvas = document.createElement("canvas");
    var ctx = canvas.getContext("2d");
    var img = new Image();

    let fst = true;

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

        if (fst) {
            pdf.image(dataurl, 0, 0).link(0, 0, img.width, img.height, window.location.href);
            fst = false;
        } else {
            pdf.image(dataurl, 0, 0);
        }
    }

    pdf.end();

    stream.on('finish', () =>
        window.open(stream.toBlobURL('application/pdf'))
    );

})();
