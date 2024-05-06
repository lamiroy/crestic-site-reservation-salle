document.addEventListener('DOMContentLoaded', function() {
    let calendarEl = document.getElementById('calendar');
    let calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        nowIndicator: true,
        locale: 'fr',
        hiddenDays: [0],
        weekNumbers: true,
        weekText: 'Semaine',
        allDaySlot: false,
        eventClick: function(info) {
            let start = moment(info.event.start).format("HH:mm");
            let end = moment(info.event.end).format("HH:mm");
            let description = info.event.extendedProps.description || "Aucune description";
            let eventDescription = document.getElementById('eventDescription');
            eventDescription.innerHTML = "<p>" + info.event.title + "</p>";
            eventDescription.innerHTML += "<p>" + start + ' - ' + end + "</p>";
            eventDescription.innerHTML += "<p>Motif : " + info.event.extendedProps.motif + "</p>";
            eventDescription.innerHTML += "<p>Nombre de personnes : " + info.event.extendedProps.eventNbPers + "</p>";
            eventDescription.innerHTML += "<p>Laboratoire : " + info.event.extendedProps.labo + "</p>";
            eventDescription.innerHTML += "<p>Status : " + description + "</p>";
            eventModal.style.display = 'block';
        },
        businessHours: [
            {
                daysOfWeek: [1, 2, 3, 4, 5], // Monday - Friday
                startTime: '08:00', // 8am
                endTime: '18:00' // 6pm
            },
            {
                daysOfWeek: [6], // Saturday
                startTime: '08:00', // 8am
                endTime: '12:30', // 12:30pm
            }
        ],
        slotMinTime: "08:00:00", // Heure d'ouverture
        slotMaxTime: "18:00:00", // Heure de fermeture
        slotDuration: "00:30:00",
        height: "auto",
        selectable: true,
        buttonText: {
            today: 'Aujourd\'hui',
            timeGridWeek: 'Semaine',
            timeGridDay: 'Jour'
        },
        headerToolbar: {
            left: 'prev today',
            center: 'title',
            right: 'timeGridWeek,timeGridDay next'
        },
        eventSources: [
  {
    url: 'calendar/holiday.ics',
    format: 'ics',
    success: function() {
            console.log('ICS holiday loaded!');
        },
        failure: function() {
            console.error('Failed to load ICS holiday.');
        },
  },
  {
    url: 'calendar/bookedrooms.ics',
    format: 'ics',
    success: function() {
                console.log('ICS booked loaded!');
            },
            failure: function() {
                console.error('Failed to load ICS booked.');
            }
  },
  // Ajoutez d'autres sources d'événements ici
],

        select: function(info) {
            modal.style.display = 'block';
            document.getElementById('id_date').value = moment(info.start).format("MM/DD/YYYY");
            document.getElementById('id_startTime').value = moment(info.start).format("HH:mm");
            document.getElementById('id_endTime').value = moment(info.end).format("HH:mm");
        },
        selectAllow: function(selectInfo) {
            if (selectInfo.start.getDay() === 6) { // Saturday
                let startTime = new Date(selectInfo.start.getFullYear(), selectInfo.start.getMonth(), selectInfo.start.getDate(), 8, 0);
                let endTime = new Date(selectInfo.start.getFullYear(), selectInfo.start.getMonth(), selectInfo.start.getDate(), 12, 30);
                return selectInfo.start >= startTime && selectInfo.end <= endTime;
            }
            return true;
        }
    });

    calendar.render();

    let modal = document.getElementById('modal');
    let eventModal = document.getElementById('eventModal');
    let btnCloseModal = document.getElementById('btnCloseModal');
    let btnCloseEventModal = document.getElementById('btnCloseEventModal');
    let eventForm = document.getElementById('eventForm');

    btnCloseModal.addEventListener('click', function() {
        modal.style.display = 'none';
        eventForm.reset();
    });

    btnCloseEventModal.addEventListener('click', function() {
        eventModal.style.display = 'none';
    });
    // à revoir, permet d'ajouter dans la ressource calendar l'event (en cache)
    // eventForm.addEventListener('submit', function(event) {
    //     event.preventDefault();
    //
    //     let title = document.getElementById('id_room_category').value;
    //     let date = document.getElementById('id_date').value;
    //     let startTime = document.getElementById('id_startTime').value;
    //     let endTime = document.getElementById('id_endTime').value;
    //     let motif = document.getElementById('id_motif').value;
    //     let eventNbPers = document.getElementById('id_peopleAmount').value;
    //     let labo = document.getElementById('id_groups').value;
    //
    //     if (title.trim() !== '' && date.trim() !== '' && startTime.trim() !== '' && endTime.trim() !== '') {
    //         let event = {
    //             title: title,
    //             start: date + 'T' + startTime,
    //             end: date + 'T' + endTime,
    //             motif: motif,
    //             eventNbPers: eventNbPers,
    //             labo: labo,
    //             description: "En attente"
    //         };
    //         calendar.addEvent(event);
    //         modal.style.display = 'none';
    //         eventForm.reset();
    //     } else {
    //         alert("Veuillez remplir tous les champs.");
    //     }
    // });
});
