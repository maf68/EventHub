$(document).ready(function() {
    // Check if the user is logged in
    if (isLoggedIn()) {
      // Hide the login and signup buttons
      $('#login-btn').addClass('d-none');
      $('#signup-btn').addClass('d-none');
    } else {
      // Show the login and signup buttons
      $('#login-btn').removeClass('d-none').addClass('d-block');
      $('#signup-btn').removeClass('d-none').addClass('d-block');
    }
  });
  
  function isLoggedIn() {
    // Your code to check if the user is logged in goes here
    // Return true if the user is logged in, false otherwise
  }
  
  
  