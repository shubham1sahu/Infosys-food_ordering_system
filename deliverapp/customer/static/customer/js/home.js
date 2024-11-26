document.addEventListener('DOMContentLoaded', function() {
    // Example: Add click handlers for quick view buttons
    const quickViewButtons = document.querySelectorAll('.quick-view .view-btn');
    quickViewButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            // Add your quick view logic here
            console.log('Quick view clicked');
        });
    });
});






