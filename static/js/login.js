function login() {
  var user_id = document.getElementById('user_id').value;
  var pwd = document.getElementById('pwd').value;

  var data = {'user_id':user_id, 'pwd':pwd};

  fetch("/validate", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)})
      .then((response) => {
        return response.json();
      }).then((data) => {
        
      });

}
