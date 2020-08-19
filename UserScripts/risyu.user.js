// ==UserScript==
// @name         Risyu to .ics
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  saidai riyuuu page to icalender format file
// @author       kimotu
// @match        https://risyu.saitama-u.ac.jp/portal/StudentApp/Regist/RegistList.aspx
// @grant        none
// @updateURL    https://github.com/kimotu4632uz/Fragment/raw/master/UserScripts/risyu.user.js
// @downloadURL  https://github.com/kimotu4632uz/Fragment/raw/master/UserScripts/risyu.user.js

// @require https://unpkg.com/dayjs@1.8.21/dayjs.min.js
// ==/UserScript==

(() => {
    'use strict';

    const timetable = {
        "1": "0900",
        "2": "1030",
        "3": "1330",
        "4": "1500",
        "5": "1630"
    };
    const classtime = 80;

    let start = window.prompt("enter first class day");
    let end = window.prompt("enter last class day");

    const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    var subjects = [];

    for (var i = 1; i <= 7; i++) {
        for (let day of days) {
            let e = document.getElementById(`ctl00_phContents_rrMain_ttTable_lct${day}${i}_ctl00_lblSbjName`);

            if (e.children.length > 0) {
                subjects.push({ "name": e.firstElementChild.innerHTML.split('<br>')[0], "day": days.indexOf(day) + 1, "time": i });
            }
        }
    }

    var cals = [];

    let first = dayjs(start.slice(0,3) + "-" + start.slice(4,5) + "-" + start.slice(6,7) + 'T00:00:00.000Z');
    let last = dayjs(end.slice(0,3) + "-" + end.slice(4,5) + "-" + end.slice(6,7) + 'T00:00:00.000Z');

    for (var i = 1; i <= 7.; i++) {
        let start_diff = i - first.day();
        if (start_diff < 0) { day_diff += 7; }

        let cls_first_date = first.add(start_diff, 'date');

        let end_diff = i - last.day();
        if (end_diff > 0) { end_diff -= 7; }

        let cls_last_date = end.add(end_diff, 'date');

        for (let s of subjects.filter(e => e.day == i)) {
            let cls_first = cls_first_date.add(timetable[s.time].slice(0,1), 'hour').add(timetable[s["time"]].slice(2,3), 'minutes');
            let cls_end = cls_first.add(classtime, 'minutes');

            cals.push(`BEGIN:VEVENT\nDTSTART;TZID=Asia/Tokyo:${cls_first.toISOString().slice(0,-1)}\nDTEND;TZID=Asia/Tokyo;${cls_end.toISOString().slice(0,-1)}`)
        }
    }

})();
