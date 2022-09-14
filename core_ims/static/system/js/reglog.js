const inputs = document.querySelectorAll(".input-field");
const toggle_btn = document.querySelectorAll(".toggle");
const main = document.querySelector("main");
const bullets = document.querySelectorAll(".bullets span");
const images = document.querySelectorAll(".image");


//   js code to slide up input placeholders (labels) when input field active
/*inputs.forEach(inp => {
    inp.addEventListener("focus", () => {
        inp.classList.add("active");
    })
    inp.addEventListener("blur", () => {
        if (inp.value != "") return;
        inp.classList.remove("active");
    });
});*/


//   js code to switch between login and sign-up forms
//toggle_btn.forEach(btn => {
//    btn.addEventListener("click", () => {
//        main.classList.toggle("sign-up-mode");
 //   });
//});


//   js code for slider inside carousel div
function moveSlider() {
    let index = this.dataset.value;

    let currentImage = document.querySelector(`.img-${index}`);
    images.forEach(img => img.classList.remove("show"));
    currentImage.classList.add("show");

    const textSlider = document.querySelector(".text-group");
    textSlider.style.transform = `translateY(${-(index - 1) * 2.2}rem)`;

    bullets.forEach(bull => bull.classList.remove("active"));
    this.classList.add("active");
}

bullets.forEach(bullet => {
    bullet.addEventListener("click", moveSlider);
});


// Query all input fields
// var form_fields = document.getElementsByTagName('input')
// form_fields[1].placeholder='Username';
// form_fields[2].placeholder='E-mail address';
// form_fields[3].placeholder='Password';
// form_fields[4].placeholder='Password confirmation';

// for (var field in form_fields) {
//     form_fields[field].className += ' form-control '
// }