// ==UserScript==
// @name         Risyu to .ics
// @namespace    http://tampermonkey.net/
// @version      0.2
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
            for (let sbj of document.getElementById(`ctl00_phContents_rrMain_ttTable_td${day}${i}`).children) {
                if (sbj.tagName === 'DIV') {
                    let ct = sbj.id.split('_')[5];

                    let sbjname = sbj.getElementById(`ctl00_phContents_rrMain_ttTable_lct${day}${i}_${ct}_lblSbjName`);
                    let teacher = sbj.getElementById(`ctl00_phContents_rrMain_ttTable_lct${day}${i}_${ct}_lblStaffName`)

                    if (sbjname.children.length > 0) {
                        subjects.push({ "name": sbjname.firstElementChild.innerText.split(/\n/)[0], "teacher": teacher.innerText, "day": days.indexOf(day) + 1, "time": i });
                    }
                }
            }
        }
    }

    console.log(subjects);
    var cals = [];

    let first = dayjs(start.slice(0,3) + "-" + start.slice(4,5) + "-" + start.slice(6,7) + 'T00:00:00.000Z');
    let last = dayjs(end.slice(0,3) + "-" + end.slice(4,5) + "-" + end.slice(6,7) + 'T00:00:00.000Z');

    for (var i = 1; i <= 7.; i++) {
        let start_diff = i - first.day();
        if (start_diff < 0) { day_diff += 7; }

        let cls_first_date = first.add(start_diff, 'date');
        let count = Math.floor(last.diff(cls_first_date, 'day') / 7);

        for (let s of subjects.filter(e => e.day == i)) {
            let cls_first = cls_first_date.add(timetable[s.time].slice(0,1), 'hour').add(timetable[s["time"]].slice(2,3), 'minutes');
            let cls_last = cls_first.add(classtime, 'minutes');

            cals.push(`
                BEGIN:VEVENT
                DTSTART;TZID=Asia/Tokyo:${cls_first.toISOString().slice(0,-1)}
                DTEND;TZID=Asia/Tokyo;${cls_last.toISOString().slice(0,-1)}
                RRULE;FREQ=WEEKLY;COUNT=${count};BYDAY=${days[s.day - 1].slice(0,1).toUpperCase()}
                SUMMARY:${s.name}
                DESCRIPTION:${s.teacher}
                END:VEVENT
            `)
        }
    }

    console.log(cals);

})();
