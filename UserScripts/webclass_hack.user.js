// ==UserScript==
// @name         Webclass hack
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  add video speed slider and video src url
// @author       kimotu
// @include      https://webclass.gks.saitama-u.ac.jp/webclass/*
// @grant        none
// @updateURL    https://github.com/kimotu4632uz/Fragment/raw/master/UserScripts/webclass_hack.user.js
// @downloadURL  https://github.com/kimotu4632uz/Fragment/raw/master/UserScripts/webclass_hack.user.js
// ==/UserScript==

(() => {
    'use strict';

    if (self.location.pathname == '/webclass/txtbk_show_text.php' && document.getElementById('video') != null) {
        var speed = document.createElement('input')
        var speed_display = document.createElement('div')
        var url_display = document.createElement('div')

        speed.type = 'range'
        speed.name = 'speed'
        speed.min = 1
        speed.max = 3
        speed.step = 0.1
        speed.value = 1

        var video = document.getElementById('video')
        speed.addEventListener('input', e => video.playbackRate = e.target.value)
        speed.addEventListener('input', e => speed_display.innerText = 'x' + e.target.value)
        speed_display.innerText = 'x1'

        if (hls != null) {
            url_display.innerText = /^.*\//.exec(hls.url)[0]
        }

        document.getElementsByClassName('contentfile')[0].appendChild(speed)
        document.getElementsByClassName('contentfile')[0].appendChild(speed_display)
        document.getElementsByClassName('contentfile')[0].appendChild(url_display)
    }
})();

