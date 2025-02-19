document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle-button');
    
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
