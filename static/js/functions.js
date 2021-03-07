
var novel_id;
var context;
var target_sentence
var target_word;
var hasContext;
var choices = [];
var num_prompt;

var use_checklist;
var buffer4checklist;
var buffer4textInput;

window.onload = function(){
  use_checklist = true;
  fetchARecord();
  num_prompt = document.getElementById("num_prompt");

};

// fetch a RANDOM row that DID NOT OCCUR
// TODO: delete the index parameter after enabling randomly selecting in the backend
function fetchARecord() {
  choices = [];
  buffer4textInput="";
  buffer4checklist=0;

  if (!(use_checklist)) {
    document.getElementById('answer').value = '';
  }

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

          choices.push('猜不到')
          choices.push(data.choice1)
          choices.push(data.choice2)
          choices.push(data.choice3)
          choices.push(data.choice4)
          choices.push(data.choice5)
          choices.push(data.choice6)

          // for(var i=1; i<choices.length; i++) {
          //   if (choices[i].length == 0) {
          //     document.getElementById("choice" + i).disabled = false
          //   }
          // }
          if (hasContext) {
            document.getElementById('context').innerHTML = context+ '________';
            //document.getElementById('target-sentence').innerHTML = target_sentence

            if(use_checklist)
            {
              document.getElementById("num_prompt").innerHTML= "";
              document.getElementById("choice0").checked=true;

              for(var i=1; i<choices.length; i++){
                if(choices[i].length == 0){
                  document.getElementById("choice"+i).disabled=true;
                } else {
                  document.getElementById("choice"+i).disabled=false;
                }
                document.getElementById('label_c'+i).innerHTML = choices[i];
              }
            }
            else{
              document.getElementById("num_prompt").innerHTML = "字数：" + target_word.length;
            }

          } else {
            document.getElementById('context').innerHTML = target_sentence+ '________';
            // document.getElementById('context-wrapper').innerHTML = "";
            // document.getElementById('target-sentence').innerHTML = target_sentence + '________';
            document.getElementById("num_prompt").innerHTML = "字数：" + target_word.length;
          }
        }

      });

};

function getSelected() {
  var checklist = document.getElementsByName("choices")
  for (i=0; i < checklist.length; i++){
    if (checklist[i].checked){
      return i;
    }
  }
}

function submit() {
  var guess = null
  if (use_checklist) {
    guess = choices[getSelected()]
  } else {
    guess = document.getElementById('answer').value.trim();
  }

  //alert(guess)
  var guessed = guess.localeCompare(target_word)==0;
  var data = {'novel_id':novel_id, 'hasContext':hasContext, 'guess':guess,'isRight':guessed,'t_word':target_word};

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

function changeView() {
  use_checklist = !(use_checklist);

  if (use_checklist) {
    buffer4textInput = document.getElementById("answer").value;

    document.getElementById('form').innerHTML =
    "<input type=\"radio\" id=\"choice0\" name=\"choices\" value=\"0\"><label for=\"choice0\", id=\"label_c0\" >猜不到</label><br><input type=\"radio\" id=\"choice1\" name=\"choices\" value=\"1\"><label for=\"choice1\", id=\"label_c1\"></label><br><input type=\"radio\" id=\"choice2\" name=\"choices\" value=\"2\"><label for=\"choice2\", id=\"label_c2\"></label><br><input type=\"radio\" id=\"choice3\" name=\"choices\" value=\"3\"><label for=\"choice3\", id=\"label_c3\"></label><br><input type=\"radio\" id=\"choice4\" name=\"choices\" value=\"4\"><label for=\"choice4\", id=\"label_c4\"></label><br><input type=\"radio\" id=\"choice5\" name=\"choices\" value=\"5\"><label for=\"choice5\", id=\"label_c5\"></label><br><input type=\"radio\" id=\"choice6\" name=\"choices\" value=\"6\"><label for=\"choice6\", id=\"label_c6\"></label><br>";

    for(var i=1; i<choices.length; i++){
      document.getElementById('label_c'+i).innerHTML = choices[i];
    }

    checkedBtn = document.getElementById("choice"+buffer4checklist);
    checkedBtn.checked = true;
    document.getElementById("num_prompt").innerHTML= "";


  } else {
    buffer4checklist = getSelected();

    document.getElementById('form').innerHTML = "<input type=\"text\" name=\"answer\" id=\"answer\" required=\"required\" placeholder=\"请键入\">";
    document.getElementById('answer').value = buffer4textInput;
    document.getElementById("num_prompt").innerHTML = "字数：" + target_word.length;

    // call the submit function when user hits the enter button
    var input = document.getElementById("answer");
    input.addEventListener("keydown", function(event) {
      if (event.keyCode === 13) {
        // prevent the default form action
        event.preventDefault();
        document.getElementById("submit").click();
      }
    });
  }


}
