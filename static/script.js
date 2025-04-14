document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle-button');
    
    // Set default event type to 'week' if no button is active
    const activeButton = document.querySelector('.toggle-button.active');
    if (!activeButton) {
        const weekButton = document.querySelector('#week_events');
        if (weekButton) {
            weekButton.classList.add('active');
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = weekButton.name;
            hiddenInput.value = weekButton.value;
            weekButton.parentNode.appendChild(hiddenInput);
        }
    }
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            toggleButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            // Update the hidden input value
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = this.name;
            hiddenInput.value = this.value;
            
            // Replace existing hidden input if it exists
            const existingInput = document.querySelector(`input[type="hidden"][name="${this.name}"]`);
            if (existingInput) {
                existingInput.remove();
            }
            this.parentNode.appendChild(hiddenInput);
        });
    });
});
