console.log("app.js running")

const fillin_elems = document.querySelectorAll(".fillin");  

// resize blank based on the number of characters
// apply the onchange event handler to each fillin
// apply the onfocus event handler to each fillin
fillin_elems.forEach(item => {
  var wordlen = item.getAttribute("data").length;
  item.style.width = (wordlen+2) +"ch";

  if ( !feedback || feedback=="immediate"){
    item.addEventListener('change', function(){ checkAnswer(this); });
  }
  item.addEventListener('keydown', processFillin);
})

const feedbackbutton = document.getElementById("feedback");
if (feedbackbutton){
  feedbackbutton.addEventListener('click', pageFeedback);
}


fillin_elems[0].focus();


function checkAnswer(elem){
  // get the answer
  const attempt = elem.value.toLowerCase();
  const correctanswer = elem.getAttribute('data').toLowerCase()

  console.log("checkAnswer()");
  console.log("ending fillin");

  elem.classList.remove("fillin-started");  
  
  if (attempt===""){
    elem.classList.remove("wrong");
    elem.classList.remove("correct");
    return;
  }  

  if (attempt==correctanswer){
    elem.classList.remove("wrong");
    elem.classList.add("correct");
  } else {
    elem.classList.remove("correct");
    elem.classList.add("wrong");
  }

  return elem.classList.contains("correct")
}

// executed when the feedback button is pressed
function pageFeedback(){
  
  var score=0;
  var count=0;

  console.log("")
  console.log("in pageFeedback()")
  
  fillin_elems.forEach( item => {
    if (checkAnswer(item))  score++;
    console.log(count, score)
  })
  console.log("page score =", score)

  return score;
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


/*
Code for managing the input page
*/

// view the input
function preview(){
    var previewarea = document.getElementById("preview-area");
    var ptext = document.getElementById("problem-text");
    previewarea.innerHTML = ptext.value;

    var linearr = processFillinText(ptext.value);
    console.log(linearr);

    document.getElementById("json").textContent = JSON.stringify(linearr, undefined, 2);

    var json = JSON.parse(document.getElementById("json").textContent);

    console.log("json")
    console.log(json)
    
    
  }


// this function splits the input text into lines (using /n)
function processFillinText(text){
  var linearr = text.split("\n");
  var parr = [];

  // create a problem object for these entries
  linearr.forEach( line => {
    if (line){
      var pobj = processFillinLine(line);
      parr.push(pobj);
    }
  })

  return parr;
}

//
// process an input string - the assumption is that 
// the input has already been split into separate lines
//
function processFillinLine(s)
{
  var fillin = [];
  var type="text";
  var str=""; 
  for (let i=0; i<(s.length-1); i++){
    if (s[i]==="[" & s[i+1]==="["){
      // end the previous text and add
      if (str!==""){
        console.log("pushing text : " + str);
        fillin.push({ 
          type:"text",
          text:str
        });
      }
      // start of a fillin
      i=i+2;
      str=s[i];
      type="fillin";
    } else if (s[i]==="]" & s[i+1]==="]"){
      // end of fillin
      i=i+1;
      console.log("pushing blank : " + str);
      fillin.push({ 
        type:"fillin",
          text:str
        });

      type="text";
      str=""
    } else {
      // just text - add to the current string
      str+=s[i];
    }

  }
  if (type=="text"){
    str+=s[s.length-1];
    fillin.push({ 
          type:"text",
          text:str
        });
  }
  return fillin;
}

