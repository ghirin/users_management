(function() {
    document.addEventListener('DOMContentLoaded', function() {
        // Найти все фильтры-<details> в админке
        var filterDetails = document.querySelectorAll('.filter-section details');
        filterDetails.forEach(function(details, idx) {
            if (idx > 0 && details.hasAttribute('open')) {
                details.removeAttribute('open');
            }
        });
    });
})();