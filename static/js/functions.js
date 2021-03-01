
var novel_id;
var context;
var target_sentence
var target_word;
var hasContext;

var num_prompt;

window.onload = function(){
  fetchARecord();
  num_prompt = document.getElementById("num_prompt");
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

        if (hasContext) {
          document.getElementById('context').innerHTML = context;
          document.getElementById('target-sentence').innerHTML = target_sentence + '________';
          num_prompt.innerHTML = "字数：" + target_word.length;
        } else {
          document.getElementById('context-wrapper').innerHTML = "";
          document.getElementById('target-sentence').innerHTML = target_sentence + '________';
          num_prompt.innerHTML = "字数：" + target_word.length;
        }

      });

};

function submit() {
  var guess = document.getElementById('answer').value.trim();
  var guessed = guess.localeCompare(target_word)==0;

  var data = {'novel_id':novel_id, 'hasContext':hasContext, 'guess':guess, 'isRight':guessed};

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

}
