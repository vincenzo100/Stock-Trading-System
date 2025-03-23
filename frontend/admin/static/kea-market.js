/* var button = document.getElementById("demo");

var toggle = true;

button.addEventListener("click", handleButtonClick);

function handleButtonClick() {
    if (toggle) {
        button.style.backgroundColor = "#772e25"
        button.style.color = "#edddd4"
        button.style.fontWeight = 700;
        console.log("true")
    }
    else {
        button.style.backgroundColor = "#edddd4"
        button.style.color = "gray"
        button.style.fontWeight = 200;
        console.log("true")
    }

    toggle = !toggle;
} */

//I had to change it because I didn't know you were trying to document.get more than one button
//so you have to select all of them by class and run a for each function in order to make sure all
//of them get the same logic to them.

//this function above works great for one button. If you're doing multiple, then you will have
//to write 7 of the same function

//ORRRR you can just use a forEach function to loop through the same logic again and again and again and x7


//for each button, add an eventlistener to listen for "click"
document.querySelectorAll(".default").forEach(button => {
                                    //once a click is heard, run some sort of lamdba function,
                                    //  a nameless function that can do something pretty quick
    button.addEventListener("click", function(event) {
        // make sure the page doesn't refresh like what the hell is up with that bruh ts pmo
        event.preventDefault(); 
        //this function will give the button another class of selected
        this.classList.toggle("selected");
    });

    //there is another selector for selected in the market-style.css page
    //Once the button is pressed again, it will toggle the selected class off. 
    // So it won't be assigned to the button tag anymore making the code work
});
