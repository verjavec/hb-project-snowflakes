"use strict";
// TODO Figure out what I need to change for this to work.  
// Might change submit to a button instead to use the sample code I brought over.

console.log('ajax works!')

function displayChoices(evt) {
  evt.preventDefault(); 

    // What sends that data to that route?
    //      This does - @app.route('/api/choices/<int:pattern_id>')
  let num_rounds = $('#num_rounds').val();  
  let url = '/users_choice?num_rounds=' + num_rounds;
  console.log(num_rounds);
        
    // Want to display what was just selected. 
  $.get(url, (res) => {
      console.log(res);
    $('#num_rounds').text(res['num_rounds']);
    // $('#num_branches').text(res['num_branches']);
    // $('#num_points').text(res['num_points']);
    
  });    
//  This part is an example that I was going to try to imitate. 
// May change submit to a button.
//  $('button').on('click', (evt) => {
//     const clickedBtn = evt.target;
//     disableLetterButton(clickedBtn);

//     const letter = clickedBtn.innerHTML;
}
// function displayChoices(evt)  {
//     evt.preventDefault();

//     console.log('Made it to ajax.js');

//     $.get($('#num_rounds'), (res) => {
//         console log('Made it to get');
//         console log(res);
//         $('#dis_num_rounds').text(res['num_rounds']);
//         // $('#dis_num_branches').text(res['num_branches']);
//         // $('#dis_num_points').text(res['num_points']);
// });


$('#get-choices').on('submit', displayChoices)
