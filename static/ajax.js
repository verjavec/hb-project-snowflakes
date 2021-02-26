"use strict";

console.log('in javascript');

// Set the default date as today
document.querySelector("#completion_input").valueAsDate = new Date();

// Try again using delivery time example from notes -- SUCCESS!
$('#date-completed').on('submit', (evt) => {
    evt.preventDefault();
    // Get user input from a form
    const formData = { 
        completion: $('#completion_input').val(),
        pattern_id: $('#patt-id').val()
    };
    
    console.log(formData);

    // Send formData to the server (becomes a query string)
    $.get('/completion_date.json', formData, (res) => {
      // Display response from the server
      console.log(res);
      $('#completion-date').text(`${res.completion}`);

    });
  });



// Attempt to just retrieve the variable with a click alone
// const dateInput = document.querySelector('#date-completed');

// dateInput.addEventListener('submit', (evt) => {
//   console.log(evt);

  
//   let formData = { 'completion': $('completion-input').val() };
//   console.log(formData)
//   $('#date').text(formData);

// });

// This function should retrieve the date from the date form and display it 
// It's currently giving an error: "GET http://localhost:8000/completion_date.json 500 (INTERNAL SERVER ERROR)"
// function updateCompletionDate(evt) {
//     evt.preventDefault();

//     let url = "/completion_date.json";
//     let formData = { 'completion': $('completion-input').val() };
//     console.log(formData)

//     console.log("made it to the function");

//     $.get(url, (response) => {
//         // console.log(response);
//         $('#date').text(response);
//     });

// }

// $('#date-completed').on('submit', updateCompletionDate)
