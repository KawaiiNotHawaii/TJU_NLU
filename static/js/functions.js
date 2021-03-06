
var novel_id;
var context;
var target_sentence
var target_word;
var hasContext;
var choices = [];
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
        if(data.isFinished){
          document.getElementById('main').innerHTML = "所有数据均已标记完成！"
        } else {
          novel_id = data.id;
          context = data.context;
          target_sentence = data.targetSentence;
          target_word = data.targetWord;
          hasContext = data.hasContext;

          choice1 = data.choice1
          choice2 = data.choice2
          choice3 = data.choice3
          choice4 = data.choice4
          choice5 = data.choice5
          choice6 = data.choice6
          choices.push('猜不到')
          choices.push(choice1)
          choices.push(choice2)
          choices.push(choice3)
          choices.push(choice4)
          choices.push(choice5)
          choices.push(choice6)

          document.getElementById("choice1").disabled=false
          document.getElementById("choice2").disabled=false
          document.getElementById("choice3").disabled=false
          document.getElementById("choice4").disabled=false
          document.getElementById("choice5").disabled=false
          document.getElementById("choice6").disabled=false
          if (hasContext) {
            document.getElementById('context').innerHTML = context+ '________';
            //document.getElementById('target-sentence').innerHTML = target_sentence
            document.getElementById("choice0").checked=true
            if (choice1 == ''){
                document.getElementById("choice1").disabled=true
            }
            document.getElementById('label_c1').innerHTML = choice1;

            if (choice2.length == 0){
                document.getElementById("choice2").disabled=true
            }
            document.getElementById('label_c2').innerHTML = choice2;
            if (choice3.length == 0){
                document.getElementById("choice3").disabled=true
            }
            document.getElementById('label_c3').innerHTML = choice3;
            if (choice4.length == 0){
                document.getElementById("choice4").disabled=true
            }
            document.getElementById('label_c4').innerHTML = choice4;

            if (choice5.length == 0){
                document.getElementById("choice5").disabled=true
            }
            document.getElementById('label_c5').innerHTML = choice5;

            if (choice6.length == 0){
                document.getElementById("choice6").disabled=true
            }
            document.getElementById('label_c6').innerHTML = choice6;

            num_prompt.innerHTML = "字数：" + target_word.length;
          } else {
            document.getElementById('context-wrapper').innerHTML = "";
            document.getElementById('target-sentence').innerHTML = target_sentence + '________';
            num_prompt.innerHTML = "字数：" + target_word.length;
          }
        }

      });

};

function submit() {
  //var guess = document.getElementById('answer').value.trim();
  var radio = document.getElementsByName("choices")
  var guess = null
  for (i=0; i < radio.length; i++){
    if (radio[i].checked){
      guess = choices[i]
      break
    }
  }
  choices = []
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
