
var novel_id;
var context;
var target_sentence
var target_word;
var extra;
var hasContext;
var choices = [];
var num_prompt;

var use_checklist;
var buffer4checklist;
var buffer4textInput;

window.onload = function(){
  fetchARecord();
  num_prompt = document.getElementById("num_prompt");

};

// fetch a RANDOM row that DID NOT OCCUR
// TODO: delete the index parameter after enabling randomly selecting in the backend
function fetchARecord() {
  choices = [];
  buffer4textInput="";
  buffer4checklist=0;

  fetch("/fetch",{
    method:'GET'})
      .then((response) => {
        return response.json();
      }).then((data) => {
        if(data.isFinished){
          document.getElementById('main').innerHTML = "所有数据均已标记完成！"
        } else {
          novel_id = data.id;
          context = data.context;
          target_sentence = data.targetSentence;
          target_word = data.targetWord;
          hasContext = data.hasContext;
          extra = data.extra;
          document.getElementById('answer').value = "";


          // for(var i=1; i<choices.length; i++) {
          //   if (choices[i].length == 0) {
          //     document.getElementById("choice" + i).disabled = false
          //   }
          // }
          if (hasContext) {
            document.getElementById('context').innerHTML = context+ '________' + extra;
            //document.getElementById('target-sentence').innerHTML = target_sentence
            document.getElementById("num_prompt").innerHTML = "字数：" + target_word.length;
          } else {
            document.getElementById('context').innerHTML = target_sentence+ '________';
            // document.getElementById('context-wrapper').innerHTML = "";
            // document.getElementById('target-sentence').innerHTML = target_sentence + '________';
            document.getElementById("num_prompt").innerHTML = "字数：" + target_word.length;
          }
        }

      });

};


function submit() {

  guess = document.getElementById('answer').value.trim();

  //alert(guess)
  if(guess == ""){
    guess = "nlu猜不出"
  }
  var guessed = guess.localeCompare(target_word) == 0;
  var data = {
    'novel_id': novel_id,
    'hasContext': hasContext,
    'guess': guess,
    'isRight': guessed,
    't_word': target_word
  };


  fetch("/post", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
      .then((response) => {
        return response.json();
      }).then((data) => {
    // TODO: DELETE; only for debug
    // alert(data.message);
    fetchARecord();
  });

}

