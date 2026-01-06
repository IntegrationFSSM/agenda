// Sidebar Toggle
document.addEventListener('DOMContentLoaded', function () {
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');

    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', function () {
            sidebar.classList.toggle('active');
            content.classList.toggle('active');
        });
    }

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirmation for delete actions
    const deleteButtons = document.querySelectorAll('[href*="delete"]');
    deleteButtons.forEach(function (button) {
        if (!button.closest('form')) {
            button.addEventListener('click', function (e) {
                if (!confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
                    e.preventDefault();
                }
            });
        }
    });

    // Real-time search (debounced)
    const searchInputs = document.querySelectorAll('input[name="search"]');
    searchInputs.forEach(function (input) {
        let timeout = null;
        input.addEventListener('input', function () {
            clearTimeout(timeout);
            timeout = setTimeout(function () {
                // Auto-submit form after 500ms of no typing
                const form = input.closest('form');
                if (form && input.value.length > 2) {
                    // Optionally auto-submit
                    // form.submit();
                }
            }, 500);
        });
    });
});
