// Configuration et initialisation de FullCalendar
document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        // Configuration de base
        locale: 'fr',
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        buttonText: {
            today: "Aujourd'hui",
            month: 'Mois',
            week: 'Semaine',
            day: 'Jour'
        },

        // Options d'affichage
        height: 'auto',
        navLinks: true,
        editable: false,
        selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        weekends: true,
        firstDay: 1, // Lundi

        // Charger les événements depuis l'API
        events: '/api/meetings/',

        // Sélection d'une plage de dates (créer une réunion)
        select: function (info) {
            // Rediriger vers le formulaire de création avec les dates pré-remplies
            var startDate = info.startStr;
            var endDate = info.endStr;
            window.location.href = `/meeting/create/?start=${startDate}&end=${endDate}`;
        },

        // Clic sur un événement (afficher les détails)
        eventClick: function (info) {
            info.jsEvent.preventDefault();

            var meetingId = info.event.id;
            var meeting = info.event;

            // Remplir le modal avec les informations de la réunion
            var modalBody = document.getElementById('meetingModalBody');
            var modalTitle = document.getElementById('meetingModalTitle');

            modalTitle.textContent = meeting.title;

            var participantsList = '';
            if (meeting.extendedProps.participants && meeting.extendedProps.participants.length > 0) {
                participantsList = '<ul class="list-group mb-3">';
                meeting.extendedProps.participants.forEach(function (participant) {
                    participantsList += `<li class="list-group-item">${participant}</li>`;
                });
                participantsList += '</ul>';
            } else {
                participantsList = '<p class="text-muted">Aucun participant</p>';
            }

            modalBody.innerHTML = `
                <div class="mb-3">
                    <h6 class="text-primary"><i class="fas fa-info-circle me-2"></i>Description</h6>
                    <p>${meeting.extendedProps.description || 'Aucune description'}</p>
                </div>
                <div class="row mb-3">
                    <div class="col-md-6">
                        <h6 class="text-primary"><i class="fas fa-clock me-2"></i>Date et heure</h6>
                        <p class="mb-1"><strong>Début:</strong> ${formatDateTime(meeting.start)}</p>
                        <p><strong>Fin:</strong> ${formatDateTime(meeting.end)}</p>
                    </div>
                    <div class="col-md-6">
                        <h6 class="text-primary"><i class="fas fa-map-marker-alt me-2"></i>Lieu</h6>
                        <p>${meeting.extendedProps.location || 'Non spécifié'}</p>
                    </div>
                </div>
                <div class="mb-3">
                    <h6 class="text-primary"><i class="fas fa-users me-2"></i>Participants</h6>
                    ${participantsList}
                </div>
            `;

            // Configurer les boutons d'action
            var editBtn = document.getElementById('editMeetingBtn');
            var deleteBtn = document.getElementById('deleteMeetingBtn');

            editBtn.href = `/meeting/${meetingId}/update/`;
            deleteBtn.onclick = function () {
                if (confirm('Êtes-vous sûr de vouloir supprimer cette réunion ?')) {
                    deleteMeeting(meetingId);
                }
            };

            // Afficher le modal
            var modal = new bootstrap.Modal(document.getElementById('meetingModal'));
            modal.show();
        },

        // Style des événements
        eventDidMount: function (info) {
            info.el.style.borderLeft = `4px solid ${info.event.backgroundColor}`;
        }
    });

    calendar.render();

    // Fonction pour formater la date et l'heure
    function formatDateTime(date) {
        if (!date) return 'Non spécifié';

        var options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };

        return new Date(date).toLocaleDateString('fr-FR', options);
    }

    // Fonction pour supprimer une réunion
    function deleteMeeting(meetingId) {
        fetch(`/meeting/${meetingId}/delete/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Fermer le modal
                    var modal = bootstrap.Modal.getInstance(document.getElementById('meetingModal'));
                    modal.hide();

                    // Recharger le calendrier
                    calendar.refetchEvents();

                    // Afficher un message de succès
                    showAlert('Réunion supprimée avec succès', 'success');
                } else {
                    showAlert('Erreur lors de la suppression', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Erreur lors de la suppression', 'danger');
            });
    }

    // Fonction pour obtenir le cookie CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Fonction pour afficher une alerte
    function showAlert(message, type) {
        var alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.setAttribute('role', 'alert');
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        var container = document.querySelector('.container-fluid');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);

            // Auto-dismiss après 5 secondes
            setTimeout(function () {
                alertDiv.classList.remove('show');
                setTimeout(function () {
                    alertDiv.remove();
                }, 150);
            }, 5000);
        }
    }
});
