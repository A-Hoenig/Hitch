// add specific event listener to submit buttons inside accordions
document.addEventListener('DOMContentLoaded', function() {
  // Get all the ids containing Btn tags inside the accordion
  var accordionLinks = document.querySelectorAll('.accordion-body [id*="Btn"]');

  // Add a click event listener to each button with ID containing 'Btn'
  accordionLinks.forEach(function(link) {
    link.removeEventListener('click', preventDefaultAction); // Remove the preventDefault event listener
    link.addEventListener('click', function(event) {
    });
  });

  // function to prevent the default action
  function preventDefaultAction(event) {
    event.preventDefault();
  }
});

document.addEventListener('DOMContentLoaded', function() {
  var accordions = document.querySelectorAll('.accordion');
  accordions.forEach(function(accordion) {
      new bootstrap.Collapse(accordion, {
          toggle: false // If you don't want to automatically close others when one is opened
      });
  });
});
