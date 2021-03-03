"use strict";

console.log('in javascript');

// Set the default date as today
document.querySelector("#completion-input").valueAsDate = new Date();

// Try again using delivery time example from notes -- SUCCESS!
$('#date-completed').on('submit', (evt) => {
    evt.preventDefault();
    // Get user input from a form
    const formData = { 
        completion: $('#completion-input').val(),
        pattern_id: $('#patt-id').val()
    };
    
    // console.log(formData);

    // Send formData to the server (becomes a query string)
    $.get('/completion_date.json', formData, (res) => {
      // Display response from the server
      // console.log(res);
      $('#completion-date').text(`${res.completion}`);

    });
  });


  $('#delete-pattern').on('click', (evt) => {
    evt.preventDefault();
    // Get pattern_id to be deleted
    const formData = { 
        pattern_id: $('#patt-id').val()
    };
    console.log(formData);
    // Send formData to the server (becomes a query string)
    $.get('/deletion', formData, (res) => {
      console.log("delete-pattern");
      $('#printed-pattern').text(`${res.pattern_id}`);

    });
  });


