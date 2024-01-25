
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


// show or hide weekdays based on Recurring value in trip form.
document.addEventListener("DOMContentLoaded", function () {
  var dropdown = document.getElementById("id_recurring");
  var elementToToggle = document.getElementById("weekday-checkboxes");
  function updateVisibility() {
      // Convert the selected value to a number
      var selectedValue = +dropdown.value;
      elementToToggle.classList.toggle("d-none", selectedValue === 0);
  }
  // Setstate based on the current value of the dropdown
  updateVisibility();

  // Add event listener for changes
  dropdown.addEventListener("change", updateVisibility);
});



// show or hide return time in trip form based on trip direction.
document.addEventListener('DOMContentLoaded', function () {
  var directionSelect = document.getElementById('id_direction').querySelector('select');
  var returnTimeDiv = document.getElementById('id_return_time');

  directionSelect.addEventListener('change', function() {
      returnTimeDiv.classList.toggle('d-none', +directionSelect.value !== 1);
  });

  // Trigger the function initially to set the correct state
  directionSelect.dispatchEvent(new Event('change'));
});


// tool tips (popper))
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

// const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
// const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))


