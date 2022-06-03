
//Sidebar open-close
let arrow = document.querySelectorAll(".arrow");
for (var i = 0; i < arrow.length; i++) {
    arrow[i].addEventListener("click", (e) => {
        let arrowParent = e.target.parentElement.parentElement;//selecting main parent of arrow
        arrowParent.classList.toggle("showMenu");
    });
}
let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".material-icons.bars");
console.log(sidebarBtn);
sidebarBtn.addEventListener("click", () => {
    sidebar.classList.toggle("close");
});



//User dropdown menu
const img = document.querySelector(".img")
const dropDown = document.querySelector(".drop-menu")

const popUp = () => {
    dropDown.classList.toggle("on-of");
};

img.addEventListener("click", popUp);



//Toggle button inside User List Table
//let toggle_button = document.querySelector(".toggle");
//let toggle_text = document.querySelector(".toggle-text");
//function AnimatedToggle() {
   //toggle_button.classList.toggle("active");

    //if(toggle_button.classList.contains("active")) {
    //    toggle_text.innerHTML = "Active";
    //}
    //else {
    //    toggle_text.innerHTML = "Inactive";
    //}
//}