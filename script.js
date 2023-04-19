//honestly got no idea what this line does. it just stops an error that occurs within 
//the file stopping it from loading 
window.onload=function(){
//allows the button on the webpage to communicate with the jscript 
const btn = document.querySelector(".btn-toggle");
//allows the ID of light theme to link with the script 
const theme = document.querySelector("#theme-link");
//listens for when the button is pressed. If light theme and button 
//is pressed go dark if dark and button is pressed go light. 
btn.addEventListener("click", function() {
 if (theme.getAttribute("href") == "light-theme.css") {

    theme.href = "dark-theme.css";
  } else {

    theme.href = "light-theme.css";
  }
});
}
