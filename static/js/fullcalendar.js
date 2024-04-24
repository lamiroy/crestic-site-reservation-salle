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
            document.getElementById('eventDescription').innerText = info.event.title;
            document.getElementById('eventDescription').innerText += '\n ' + start + ' - ' + end;
            document.getElementById('eventDescription').innerText += '\nStatus : ' + description;
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
            today: 'Aujourd\'hui'
        },
        headerToolbar: {
            left: 'prev today',
            center: 'title',
            right: 'next'
        },
        events: {
            url: '/calendrier.ics',
            format: 'ics',
            success: function() {
                console.log('ICS events loaded!');
            },
            failure: function() {
                console.error('Failed to load ICS events.');
            }
        },
        select: function(info) {

            // Open modal for adding new event
            modal.style.display = 'block';

            // Populate date and time inputs in the form
            document.getElementById('eventDate').value = moment(info.start).format("YYYY-MM-DD");
            document.getElementById('eventStartTime').value = moment(info.start).format("HH:mm");
            document.getElementById('eventEndTime').value = moment(info.end).format("HH:mm");
        }
    });
    calendar.render();
    let modal = document.getElementById('modal');
    let eventModal = document.getElementById('eventModal');
    let btnAddEvent = document.getElementById('btnAddEvent');
    let btnCloseModal = document.getElementById('btnCloseModal');
    let btnCloseEventModal = document.getElementById('btnCloseEventModal');
    let eventForm = document.getElementById('eventForm');

    btnAddEvent.addEventListener('click', function() {
        modal.style.display = 'block';
    });

    btnCloseModal.addEventListener('click', function() {
        modal.style.display = 'none';
        // Clear form fields when modal is closed
        eventForm.reset();
    });

    btnCloseEventModal.addEventListener('click', function() {
        eventModal.style.display = 'none';
    });

    eventForm.addEventListener('submit', function(event) {
        event.preventDefault();

        let title = document.getElementById('eventTitle').value;
        let date = document.getElementById('eventDate').value;
        let startTime = document.getElementById('eventStartTime').value;
        let endTime = document.getElementById('eventEndTime').value;


        if (title.trim() !== '' && date.trim() !== '' && startTime.trim() !== '' && endTime.trim() !== '') {
            let event = {
                title: title,
                start: date + 'T' + startTime,
                end: date + 'T' + endTime,
                description: "En attente"
            };
            calendar.addEvent(event);
            modal.style.display = 'none';
            // Clear form fields after successful submission
            eventForm.reset();
        } else {
            alert("Veuillez remplir tous les champs.");
        }
    });
});
