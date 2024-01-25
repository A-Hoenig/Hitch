
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

document.addEventListener('DOMContentLoaded', function() {
  var accordions = document.querySelectorAll('.accordion');
  accordions.forEach(function(accordion) {
      new bootstrap.Collapse(accordion, {
          toggle: false
      });
  });
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
    var deleteBtn = document.getElementById('deleteBtn-' + elementId);
    if (deleteBtn.classList.contains('d-none')) {
        deleteBtn.classList.remove('d-none');
    } else {
        deleteBtn.classList.add('d-none');
    }
    deleteBtn.offsetWidth; // Trigger DOM rebuild
}

// Auto-dismiss alert after 5 seconds (5000 milliseconds)
$(document).ready(function () {
    window.setTimeout(function () {
        $(".alert").alert('close');
    }, 5000);
});


// show or hide weekday based on Recurring value in trip form.
document.addEventListener("DOMContentLoaded", function () {
  var dropdown = document.getElementById("id_recurring");
  var elementToToggle = document.getElementById("weekday-checkboxes");

  function updateVisibility() {
      var selectedValue = dropdown.value;
      elementToToggle.classList.toggle("d-none", selectedValue === "False");
  }
  // Set initial state based on the current value of the dropdown
  updateVisibility();

  // now add event
  dropdown.addEventListener("change", updateVisibility);
});


// show or hide return time in trip form based on trip direction.
document.addEventListener('DOMContentLoaded', function () {
  var directionSelect = document.querySelector('#id_direction select');
  var returnTimeDiv = document.getElementById('id_return_time');

  function updateReturnTimeVisibility() {
      if (directionSelect.value === 'True') {
          returnTimeDiv.classList.remove('d-none');
      } else {
          returnTimeDiv.classList.add('d-none');
      }
  }

  // Initial check when the page loads
  updateReturnTimeVisibility();

  // Event listener for changes in the dropdown
  directionSelect.addEventListener('change', updateReturnTimeVisibility);
});



// tool tips (popper))
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

// const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
// const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))


