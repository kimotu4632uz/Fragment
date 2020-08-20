// ==UserScript==
// @name         Risyu to .ics
// @namespace    http://tampermonkey.net/
// @version      1.0.0
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
        '1': '09:00',
        '2': '10:30',
        '3': '13:30',
        '4': '15:00',
        '5': '16:30'
    };
    const classtime = 80;

    const start = window.prompt('enter first class day');
    const qend = window.prompt('enter 1st quarter end day');
    const qstart = window.prompt('enter 2nd quarter start day');
    const end = window.prompt('enter last class day');

    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    let subjects = [];

    for (let day of days.slice(1)) {
        for (var i = 1; i <= 7; i++) {
            for (let sbj of document.getElementById(`ctl00_phContents_rrMain_ttTable_td${day}${i}`).children) {
                if (sbj.tagName === 'DIV') {
                    const ct = sbj.id.split('_')[5];

                    const sbjname = document.getElementById(`ctl00_phContents_rrMain_ttTable_lct${day}${i}_${ct}_lblSbjName`);
                    const teacher = document.getElementById(`ctl00_phContents_rrMain_ttTable_lct${day}${i}_${ct}_lblStaffName`);
                    const      id = document.getElementById(`ctl00_phContents_rrMain_ttTable_lct${day}${i}_${ct}_lblLctCd`).innerText;

                    if (sbjname.children.length > 0) {
                        const sbjinfo = sbjname.firstElementChild.innerText.split(/\n/);

                        let quarter = 0;

                        if (sbjinfo.length > 1) {
                            const result = /第([1-4])ターム/.exec(sbjinfo[1].replace(/[０-９]/g, s => String.fromCharCode(s.charCodeAt(0) - 65248)));

                            if (result != null) {
                                if (result[1] == '1' || result[1] == '3') { quarter = 1 }
                                else { quarter = 2 }
                            }
                        }

                        const prev = subjects.findIndex(e => e.id === id && e.day === days.indexOf(day) && e.time[e.time.length - 1] === (i - 1));
                        if (prev != -1) {
                            subjects[prev].time.push(i);
                        } else {
                            subjects.push({ 'name': sbjinfo[0], 'teacher': teacher.innerText, 'day': days.indexOf(day), 'time': [i], 'quarter': quarter, 'id': id });
                        }
                    }
                }
            }
        }
    }

    const first = dayjs(`${start.slice(0,4)}-${start.slice(4,6)}-${start.slice(6,8)}T00:00:00.000+09:00`);
    const qlast = dayjs(`${qend.slice(0,4)}-${qend.slice(4,6)}-${qend.slice(6,8)}T00:00:00.000+09:00`);
    const qfirst = dayjs(`${qstart.slice(0,4)}-${qstart.slice(4,6)}-${qstart.slice(6,8)}T00:00:00.000+09:00`);
    const last = dayjs(`${end.slice(0,4)}-${end.slice(4,6)}-${end.slice(6,8)}T00:00:00.000+09:00`);

    let cals = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//org//me//JP'];

    for (var i = 1; i < 7; i++) {
        let start_diff = i - first.day();
        if (start_diff < 0) { start_diff += 7; }

        let qstart_diff = i - qfirst.day();
        if (qstart_diff < 0) { qstart_diff += 7; }

        for (let s of subjects.filter(e => e.day == i)) {
            const cls_first_date =
                s.quarter == 2 ? qfirst.add(qstart_diff, 'day')
                               : first.add(start_diff, 'day');

            const count =
                s.quarter == 1 ? Math.floor(qlast.diff(cls_first_date, 'day') / 7)
                               : Math.floor(last.diff(cls_first_date, 'day') / 7);

            const cls_first = cls_first_date.add(timetable[s.time[0]].split(':')[0], 'hour').add(timetable[s.time[0]].split(':')[1], 'minutes');

            const cls_last_time = timetable[s.time[s.time.length - 1]];
            const cls_last = cls_first_date.add(cls_last_time.split(':')[0], 'hour').add(Number(cls_last_time.split(':')[1]) + classtime, 'minutes');

            cals.push(`
                BEGIN:VEVENT
                DTSTART;TZID=Asia/Tokyo:${cls_first.format('YYYYMMDDTHHmmss')}
                DTEND;TZID=Asia/Tokyo:${cls_last.format('YYYYMMDDTHHmmss')}
                RRULE:FREQ=WEEKLY;COUNT=${count + 1};BYDAY=${days[s.day].slice(0,2).toUpperCase()}
                SUMMARY:${s.name}
                DESCRIPTION:${s.teacher}, ${s.id}
                END:VEVENT
            `.replace(/^\s+/gm, ''));
        }
    }

    cals.push('END:VCALENDAR');

    const a = document.createElement('a');
    const blob = new Blob([cals.join('\n')], {type: 'text/plain'});
    const url = URL.createObjectURL(blob);
    a.style = 'display:none';
    a.href = url;
    a.download = 'risyu.ics';
    a.click();
    URL.revokeObjectURL(url);
})();
