var html = document.querySelector("#upload_frame");
var body = document.querySelector("#body1");
var container = document.querySelector("#upload_container");

container.addEventListener('resize', async (el, ev) => {
    if (body.offsetWidth != html.offsetWidth) {                    
        document.querySelector("body").offsetWidth = document.querySelector("html").offsetWidth;
        document.querySelector("#upload_container").offsetWidth = document.querySelector("body").offsetWidth;
        console.log("Html " + html);
        console.log("body " + body);
        console.log("container " + container);
    }
    else{
        console.log("Something went wrong");
    }
    });


var form_border = document.querySelector("#form_border")
var col = document.querySelector("#form_border").style.backgroundColor;

form_border.addEventListener('mouseover', async (el, ev) => {
    
    form_border.style.backgroundColor = "#00ffff33 ";
    });
    
form_border.addEventListener('mouseout', async (el, ev) => {
    document.querySelector("#form_border").style.backgroundColor = col;
    });

