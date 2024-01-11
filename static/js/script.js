document.addEventListener('DOMContentLoaded', function() {
    // Get all the anchor tags inside the accordion
    var accordionLinks = document.querySelectorAll('.accordion a');
  
    // Add a click event listener to each anchor tag
    accordionLinks.forEach(function(link) {
      link.addEventListener('click', function(event) {
        // Prevent the default action of the link
        event.preventDefault();
        // Open the link's URL in the current tab
        window.location.href = link.getAttribute('href');
      });
    });
  });