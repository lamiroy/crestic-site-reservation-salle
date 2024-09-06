document.addEventListener('DOMContentLoaded', function() {
    // Obtention de l'élément HTML représentant le calendrier
    let calendarEl = document.getElementById('calendar');
    let sitePrefix = '/reservations'

    // Création d'une instance du calendrier FullCalendar
    let calendar = new FullCalendar.Calendar(calendarEl, {
        // Configuration initiale de la vue du calendrier
        initialView: 'timeGridWeek', // Vue initiale : grille horaire pour une semaine
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
            let eventTitle = document.getElementById('eventTitle');
            let eventDescription = document.getElementById('eventDescription'); // Élément HTML où afficher les détails de l'événement
            const detailsButton = document.querySelector('button.d-none.modalDetails');
            detailsButton.click();
            // Convertir la chaîne JSON corrigée en objet JavaScript
            let eventData = JSON.parse(info.event.title);
            let eventDetailsButtons = document.querySelector("div.eventDetailsButtons");
            if (eventData.holiday === "false") {
                let statut;
                if (eventData.status === "pending") {
                    statut = "En attente";
                } else if (eventData.status === "canceled") {
                    statut = "Annulé";
                } else if (eventData.status === "validated") {
                    statut = "Validé";
                }
                // Construction du contenu HTML avec les détails de l'événement
                eventTitle.innerHTML = `
                    ${start} - ${end}&ensp;❘&ensp;
                    <span class="modal-detail-title">${eventData.nom}</span>
                    <div class="flex-space-modal"></div>
                    <span class="badge text-bg-danger modal-detail-badge">${eventData.nombre_personnes}/${eventData.max_capacity} pers.</span>
                `; // Titre de l'événement
                eventDescription.innerHTML = `<p class="modal-description">${eventData.motif}</p>`; // Motif de réservation
                eventDescription.innerHTML += `
                    <ul class="list-group modal-list">
                        <li class="list-group-item d-flex justify-content-between align-items-start">
                            <div class="ms-2 me-auto">
                                <div class="fw-bold">Laboratoire</div>
                                ${eventData.labo}
                            </div>
                        </li>
                        <li class="list-group-item d-flex justify-content-between align-items-start">
                            <div class="ms-2 me-auto">
                                <div class="fw-bold">Statut</div>
                                ${statut}
                            </div>
                        </li>
                    </ul>
                `; // Laboratoire et statut
                // Ajout du contenu des ancres
                if (eventData.holiday === "false") {
                    eventDetailsButtons.innerHTML = `
                        <a id="ancreEdit" class="btn btn-primary button-style" href="``${sitePrefix}/roombooking/${eventData.id}/edit/">Modifier</a>
                        <a id="ancreDelete" class="btn btn-danger card-link button-style button-red" href="``${sitePrefix}/roombooking/${eventData.id}/delete/">Annuler</a>
                    `;
                }
            } else {
                eventTitle.innerText = "Jour férié";
                eventDetailsButtons.innerHTML = null;
                eventDescription.innerHTML = `<p class="modal-description">${eventData.nom}</p>`;
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
                endTime: '12:30' // Heure de fermeture (12:30)
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
            left: 'prev today rooms,equipments', // Boutons de navigation à gauche
            center: 'title', // Titre du calendrier au centre
            right: 'timeGridWeek,timeGridDay next' // Boutons de navigation à droite
        },
        customButtons: {
            rooms: {
                text: 'Salles'
            },
            equipments: {
                text: 'Équipements',
                click: function() {
                    window.location.href = `${sitePrefix}/equipments/calendar`;
		    // window.location.href = "{% url 'home_equipment' %}";
                }
            }
        },
        viewDidMount: function() {
            // Désactiver le bouton "Salles"
            document.querySelector('.fc-rooms-button').setAttribute('disabled', 'true');
        },
        views: {
            timeGridWeek: {
                buttonText: 'Semaine',
                didMount: function(view) {
                    document.querySelector('.fc-timeGridWeek-button').classList.add('disable');
                    document.querySelector('.fc-timeGridDay-button').classList.remove('disable');
                }
            },
            timeGridDay: {
                buttonText: 'Jour',
                didMount: function(view) {
                    document.querySelector('.fc-timeGridDay-button').classList.add('disable');
                    document.querySelector('.fc-timeGridWeek-button').classList.remove('disable');
                }
            }
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
            const addButton = document.querySelector('button.d-none.modalAdd');
            addButton.click();
            // Remplir les champs de la fenêtre modale avec les informations de la sélection
            document.getElementById('id_date').value = moment(info.start).format("DD/MM/YYYY"); // Date
            document.getElementById('id_startTime').value = moment(info.start).format("HH:mm"); // Heure de début
            document.getElementById('id_endTime').value = moment(info.end).format("HH:mm"); // Heure de fin
        },
        // Fonction de validation pour permettre la sélection de créneaux horaires spécifiques
        selectAllow: function(selectInfo) {
            if (selectInfo.start.getDay() === 6) { // Si le jour sélectionné est un samedi
                // Défini les heures d'ouverture et de fermeture pour le samedi
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
            if (eventData.holiday === "false") {
                if (eventData.status === 'pending') {
                    switch (eventData.labo) {
                        case 'CReSTIC':
                            classNames.push('event-pending-crestic');
                            break;
                        case 'Lab-i*':
                            classNames.push('event-pending-labi');
                            break;
                        case 'LICIIS':
                            classNames.push('event-pending-liciis');
                            break;
                        case 'Autre':
                            classNames.push('event-pending-autre');
                            break;
                    }
                } else if (eventData.status === 'validated') {
                    switch (eventData.labo) {
                        case 'CReSTIC':
                            classNames.push('event-validated-crestic');
                            break;
                        case 'Lab-i*':
                            classNames.push('event-validated-labi');
                            break;
                        case 'LICIIS':
                            classNames.push('event-validated-liciis');
                            break;
                        case 'Autre':
                            classNames.push('event-validated-autre');
                            break;
                    }
                }
            } else {
                classNames.push('event-holiday');
            }
            // Ajouter les classes au DOM de l'événement
            info.el.classList.add(...classNames);
        },
        eventContent: function(arg) {
            let start = moment(arg.event.start).format("HH:mm"); // Heure de début formatée
            let end = moment(arg.event.end).format("HH:mm"); // Heure de fin formatée
            let eventDetails = document.createElement('span');
            let eventData = JSON.parse(arg.event.title);
            if (eventData.holiday === "false") {
                eventDetails.innerHTML = `<p class="event-details">${start} - ${end}&ensp;❘&ensp;${eventData.nom}</p>`;
                eventDetails.innerHTML += `<p class="event-labo">${eventData.labo}</p>`;
                eventDetails.innerHTML += `<p class="event-motif">${eventData.motif}</p>`;
            } else {
                eventDetails.innerHTML = `<p class="event-details">${eventData.nom}</p>`;
            }
            let arrayOfDomNodes = [ eventDetails ];
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

    // Vérifie s'il y a une erreur dans le formulaire
    const formError = document.getElementById('error-form');
    if (formError) {
        const addButton = document.querySelector('button.d-none.modalAdd');
        addButton.click();
    }

    // Ajout des écouteurs d'événements pour désactiver les boutons de navigation
    let btnWeek = document.querySelector('.fc-timeGridWeek-button');
    let btnDay = document.querySelector('.fc-timeGridDay-button');

    // Désactiver le bouton "Semaine" de base
    btnWeek.disabled = true;

    btnWeek.addEventListener('click', function() {
        btnWeek.disabled = true;  // Désactiver le bouton "Semaine"
        btnDay.disabled = false;  // Activer le bouton "Jour"
    });

    btnDay.addEventListener('click', function() {
        btnDay.disabled = true;   // Désactiver le bouton "Jour"
        btnWeek.disabled = false; // Activer le bouton "Semaine"
    });
});
