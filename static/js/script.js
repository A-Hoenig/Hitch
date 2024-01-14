document.addEventListener('DOMContentLoaded', function() {
    // Get all the anchor tags inside the accordion
    var accordionLinks = document.querySelectorAll('.accordion a');
  
    // Add a click event listener to each anchor tag
    accordionLinks.forEach(function(link) {
      link.addEventListener('click', function(event) {
        // Prevent the default action of the link - no accordion
        event.preventDefault();
        // Open the link's URL in the current tab
        window.location.href = link.getAttribute('href');
      });
    });
  });

const exampleModal = document.getElementById('exampleModal')
if (exampleModal) {
  exampleModal.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const recipient = button.getAttribute('data-bs-whatever')
    // If necessary, you could initiate an Ajax request here
    // and then do the updating in a callback.

    // Update the modal's content.
    const modalTitle = exampleModal.querySelector('.modal-title')
    const modalBodyInput = exampleModal.querySelector('.modal-body input')

    modalTitle.textContent = `New message to ${recipient}`
    modalBodyInput.value = recipient
  })
}

