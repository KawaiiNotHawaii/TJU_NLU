
var novel_id;
// TODO: user user_id or not? add user_id logic if use it
var user_id=1;
var context;
var target_sentence
var target_word;
var hasContext;

window.onload = function(){
  fetchARecord();

  // call the submit function when user hits the enter button
  var input = document.getElementById("answer");
  input.addEventListener("keydown", function(event) {
    if (event.keyCode === 13) {
      // prevent the default form action
      event.preventDefault();
      document.getElementById("submit").click();
    }
  });
};

// fetch a RANDOM row that DID NOT OCCUR
// TODO: delete the index parameter after enabling randomly selecting in the backend
function fetchARecord() {
  document.getElementById('answer').value = '';

  fetch("/fetch",{
    method:'GET'})
      .then((response) => {
        return response.json();
      }).then((data) => {
        novel_id = data.id;
        context = data.context;
        target_sentence = data.targetSentence;
        target_word = data.targetWord;
        hasContext = data.hasContext;

        document.getElementById('context').innerHTML = context;
        document.getElementById('target-sentence').innerHTML = target_sentence + '________';
      });

};

function submit() {
  var guess = document.getElementById('answer').value.trim();
  var guessed = guess.localeCompare(target_word)==0;

  var data = {'novel_id':novel_id, 'user_id':user_id, 'hasContext':hasContext, 'guess':guess, 'isRight':guessed};

  fetch("/post", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)})
      .then((response) => {
        return response.json();
      }).then((data) => {
        // TODO: DELETE; only for debug
        // alert(data.message);
        fetchARecord();
      });

  // fetch(`/post/${guessed}`,{
  //   method:'POST'})
  //     .then((response) => {
  //       return response.json();
  //     }).then((data) => {
  //       // TODO: DELETE; only for debug
  //       alert(data.message);
  //     });


}
