
// add specific event listener to submit buttons inside accordions
document.addEventListener('DOMContentLoaded', function() {
  // Get all the ids containing Btn tags inside the accordion
  var accordionLinks = document.querySelectorAll('.accordion-body [id*="Btn"]');

  // Add a click event listener to each button with ID containing 'Btn'
  accordionLinks.forEach(function(link) {
    link.removeEventListener('click', preventDefaultAction);
    link.addEventListener('click', function(event) {
    });
  });

  // function to prevent the default action
  function preventDefaultAction(event) {
    event.preventDefault();
  }
});


// update ride or hitch region filter when user selects one from dropdown
document.addEventListener('DOMContentLoaded', function () {
  var form = document.getElementById('filterForm');
  
  // check a form is present first
  if (form) {
    var regionDropdown = form.querySelector('#id_selected_region');

    // Check for regionDropdown first
    if (regionDropdown) {
      regionDropdown.addEventListener('change', function () {
        form.submit();
      });
    }
  }
});

// reveal confirm delete buttons
function revealDelete(elementId) {
  console.log("Called revealDelete with ID:", elementId); // Debugging  
  var deleteBtn = document.getElementById('deleteBtn-' + elementId);
    if (deleteBtn.classList.contains('d-none')) {
        deleteBtn.classList.remove('d-none');
    } else {
        deleteBtn.classList.add('d-none');
    }
}

// Auto-dismiss alert after 5 seconds (5000 milliseconds)
$(document).ready(function () {
    window.setTimeout(function () {
        $(".alert").alert('close');
    }, 5000);
});


// tool tips (popper))
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

// const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
// const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))


