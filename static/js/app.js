console.log("app.js running")

const fillin_elems = document.querySelectorAll(".fillin");  

// resize blank based on the number of characters
// apply the onchange event handler to each fillin
// apply the onfocus event handler to each fillin
fillin_elems.forEach(item => {
  var wordlen = item.getAttribute("data").length;
  item.style.width = (wordlen+2) +"ch";
  item.addEventListener('change', checkAnswer);
  item.addEventListener('keydown', processFillin);
})

fillin_elems[0].focus();


// e is the element
function checkAnswer(){
  // get the answer
  const attempt = this.value.toLowerCase();
  const correctanswer = this.getAttribute('data').toLowerCase()

  console.log("checkAnswer()");
  console.log("ending fillin");

  this.classList.remove("fillin-started");  
  
  if (attempt===""){
    this.classList.remove("wrong");
    this.classList.remove("correct");
    return;
  }  

  if (attempt==correctanswer){
    this.classList.remove("wrong");
    this.classList.add("correct");
  } else {
    this.classList.remove("correct");
    this.classList.add("wrong");
  }

}

// when focus returns to the fillin
// set to blank and remove correct or wrong classes
function restartFillin(){
  this.value=""
  this.classList.remove("wrong");
  this.classList.remove("correct");
}

// when focus returns to the fillin
// set to blank and remove correct or wrong classes
function processFillin(e){
  let excludedKeys=["Tab", "Shift", "Alt", "Ctrl", "Space"];

  // make sure a tab key does not trigger a refress
  console.log("processFillin( " + e.key + " )")

  if(!excludedKeys.includes(e.key)){
    if (!this.classList.contains('fillin-started')){
      console.log("starting filling")
      this.value=""
      this.classList.remove("wrong");
      this.classList.remove("correct");  
      this.classList.add("fillin-started");  
    }
    else{
      console.log("\t...")
    }
  } else {
    console.log("key ignored")
  }
}

