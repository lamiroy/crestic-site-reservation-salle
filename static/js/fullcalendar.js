document.addEventListener('DOMContentLoaded', function() {
    // Obtention de l'élément HTML représentant le calendrier
    let calendarEl = document.getElementById('calendar');

    // Création d'une instance du calendrier FullCalendar
    let calendar = new FullCalendar.Calendar(calendarEl, {
        // Configuration initiale de la vue du calendrier
        initialView: 'timeGridWeek', // Vue initiale: grille horaire pour une semaine
        nowIndicator: true, // Affichage d'un indicateur pour l'heure actuelle
        locale: 'fr', // Langue locale du calendrier
        hiddenDays: [0], // Masquer les dimanches
        weekNumbers: true, // Afficher les numéros de semaine
        weekText: 'Semaine', // Texte affiché pour la semaine
        allDaySlot: false, // Masquer la section de toute la journée
        // Fonction exécutée lors du clic sur un événement du calendrier
        eventClick: function(info) {
            let start = moment(info.event.start).format("HH:mm"); // Heure de début formatée
            let end = moment(info.event.end).format("HH:mm"); // Heure de fin formatée
            let description = info.event.extendedProps.description || "Aucune description"; // Description de l'événement
            let eventDescription = document.getElementById('eventDescription'); // Élément HTML où afficher les détails de l'événement
            const detailsButton = document.querySelector('button.d-none.modalDetails');
            detailsButton.click();
            // Convertir la chaîne JSON corrigée en objet JavaScript
            let eventData = JSON.parse(info.event.title);
            if (eventData.holiday == "false") {
                // Construction du contenu HTML avec les détails de l'événement
                eventDescription.innerHTML = "<p>" + eventData.nom + "</p>"; // Titre de l'événement
                eventDescription.innerHTML += "<p>" + start + ' - ' + end + "</p>"; // Plage horaire de l'événement
                eventDescription.innerHTML += "<p>Motif : " + eventData.motif + "</p>"; // Motif de réservation
                eventDescription.innerHTML += "<p>Nombre de personnes : " + eventData.nombre_personnes + "</p>"; // Nombre de personnes
                eventDescription.innerHTML += "<p>Laboratoire : " + eventData.labo + "</p>"; // Laboratoire
                eventDescription.innerHTML += "<p>Nom de la salle : " + eventData.nom + "</p>"; // Nom de la salle
                eventDescription.innerHTML += "<p>Status : " + eventData.status + "</p>"; // Status de la réservation
            } else {
                eventDescription.innerHTML = "<p>" + eventData.nom + "</p>";
            }

        },
        businessHours: [
            {
                daysOfWeek: [1, 2, 3, 4, 5], // Jours ouvrables (lundi à vendredi)
                startTime: '08:00', // Heure d'ouverture (08:00)
                endTime: '18:00' // Heure de fermeture (18:00)
            },
            {
                daysOfWeek: [6], // Samedi
                startTime: '08:00', // Heure d'ouverture (08:00)
                endTime: '12:30', // Heure de fermeture (12:30)
            }
        ],
        slotMinTime: "08:00:00", // Heure de début minimum pour les créneaux horaires
        slotMaxTime: "18:00:00", // Heure de fin maximum pour les créneaux horaires
        slotDuration: "00:30:00", // Durée par défaut des créneaux horaires
        height: "auto", // Hauteur automatique du calendrier en fonction du contenu
        selectable: true, // Activation de la sélection de créneaux horaires
        // Textes des boutons de navigation du calendrier
        buttonText: {
            today: 'Aujourd\'hui',
            timeGridWeek: 'Semaine',
            timeGridDay: 'Jour'
        },
        headerToolbar: {
            left: 'prev today', // Boutons de navigation à gauche
            center: 'title', // Titre du calendrier au centre
            right: 'timeGridWeek,timeGridDay next' // Boutons de navigation à droite
        },
        // Sources des événements pour le calendrier
        eventSources: [
            {
                url: 'calendar/holiday.ics', // URL du fichier iCalendar pour les jours fériés
                format: 'ics', // Format du fichier iCalendar
                success: function() {
                    console.log('ICS holiday loaded!'); // Message de réussite du chargement des jours fériés
                },
                failure: function() {
                    console.error('Failed to load ICS holiday.'); // Message d'erreur en cas d'échec du chargement des jours fériés
                }
            },
            {
                url: 'calendar/bookedrooms.ics', // URL du fichier iCalendar pour les réservations
                format: 'ics', // Format du fichier iCalendar
                success: function() {
                    console.log('ICS booked loaded!'); // Message de réussite du chargement des réservations
                },
                failure: function() {
                    console.error('Failed to load ICS booked.'); // Message d'erreur en cas d'échec du chargement des réservations
                }
            }
        ],
        // Fonction exécutée lors de la sélection d'un créneau horaire
        select: function(info) {
            const addButton = document.querySelector('button.d-none');
            addButton.click();
            // Remplir les champs de la fenêtre modale avec les informations de la sélection
            document.getElementById('id_date').value = moment(info.start).format("MM/DD/YYYY"); // Date
            document.getElementById('id_startTime').value = moment(info.start).format("HH:mm"); // Heure de début
            document.getElementById('id_endTime').value = moment(info.end).format("HH:mm"); // Heure de fin
        },
        // Fonction de validation pour permettre la sélection de créneaux horaires spécifiques
        selectAllow: function(selectInfo) {
            if (selectInfo.start.getDay() === 6) { // Si le jour sélectionné est un samedi
                // Définir les heures d'ouverture et de fermeture pour le samedi
                let startTime = new Date(selectInfo.start.getFullYear(), selectInfo.start.getMonth(), selectInfo.start.getDate(), 8, 0);
                let endTime = new Date(selectInfo.start.getFullYear(), selectInfo.start.getMonth(), selectInfo.start.getDate(), 12, 30);
                // Vérifier si la sélection est comprise entre les heures d'ouverture et de fermeture
                return selectInfo.start >= startTime && selectInfo.end <= endTime;
            }
            return true; // Autoriser la sélection pour les autres jours
        },
        eventDidMount: function(info) {
            let classNames = [];
            let eventData = JSON.parse(info.event.title);
            if (eventData.holiday == "false") {
                if (eventData.status !== 'pending') {
                    // Ajouter des classes en fonction du laboratoire
                    switch (eventData.labo) {
                        case 'CReSTIC':
                            classNames.push('event-crestic');
                            break;
                        case 'Labi*':
                            classNames.push('event-labi');
                            break;
                        case 'Liciis':
                            classNames.push('event-liciis');
                            break;
                        default:
                            classNames.push('event-default');
                    }
                } else {
                    classNames.push('event-pending');
                }
                // Ajouter les classes au DOM de l'événement
                info.el.classList.add(...classNames);
            }
        },
        eventContent: function(arg) {
            let start = moment(arg.event.start).format("HH:mm"); // Heure de début formatée
            let end = moment(arg.event.end).format("HH:mm"); // Heure de fin formatée
            let italicEl = document.createElement('span');
            let eventData = JSON.parse(arg.event.title);
            if (eventData.holiday == "false") {
                italicEl.innerHTML = '<b>' + start + ' - ' + end + '</b> &ensp;';
                italicEl.innerHTML += '<i>' + eventData.nom + '</i> &ensp;'
                italicEl.innerHTML += '<i>' + eventData.labo + '</i>'
            } else {
                italicEl.innerHTML += '<i>' + eventData.nom + '</i>'
            }
            let arrayOfDomNodes = [ italicEl ];
            return { domNodes: arrayOfDomNodes };
    }

    });

    calendar.render(); // Afficher le calendrier

    // Gestion de la fermeture de la fenêtre modale de création de réservation
    let btnCloseAdd = document.getElementById('btnCloseAdd');
    let eventForm = document.getElementById('eventForm');
    btnCloseAdd.addEventListener('click', function() {
        eventForm.reset(); // Réinitialiser le formulaire de réservation
    });
});
