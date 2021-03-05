"use strict";

// Set the default date as today
document.querySelector("#completion-input").valueAsDate = new Date();

// Get number of rounds, points and branches for the pattern_id
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

// Delete a pattern
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

// Upload a photo
var myWidget = cloudinary.createUploadWidget({
  cloudName: 'dbjwx7sg5', uploadPreset: 'rsk7e1ha'}, 
    (error, result) => { 
    if (!error && result && result.event === "success") { 
      // console.log('Done! Here is the image info: ', result.info); 
      const imageData = {
        image_url:result.info.url,
        image_public_id:result.info.public_id,
        image_format:result.info.format,
        pattern_id: $('#patt-id').val()
      }
      // console.log(imageData);
      $.get('/add_photo', imageData, (res) => {
        // console.log('add-photo');
        $('#photo').attr('src', `${res.image_url}`);
      });
    }
  }
)

document.getElementById("upload-photo").addEventListener("click", function(){
  myWidget.open();
}, false);

