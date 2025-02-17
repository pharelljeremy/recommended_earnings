document.addEventListener('DOMContentLoaded', function () {
    // Add confirmation dialog for delete buttons
    const deleteButtons = document.querySelectorAll('a[href*="/delete/"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            const confirmDelete = confirm('Are you sure you want to delete this recommendation?');
            if (!confirmDelete) {
                event.preventDefault(); // Stop the link from navigating
            }
        });
    });
});