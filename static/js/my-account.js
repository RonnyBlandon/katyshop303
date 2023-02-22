// Show and hide the mobile menu
const userMenuShow = document.querySelector(".nav-user-show");
const userMenuClose = document.querySelector(".nav-user-close");

userMenuShow.addEventListener("click", ()=> {
   const boxNavUser = document.querySelector(".box-nav-user");
   boxNavUser.style.right = "0";
});

userMenuClose.addEventListener("click", ()=> {
    const boxNavUser = document.querySelector(".box-nav-user");
    boxNavUser.style.right = "100%";
 });

/*
const re = /^+?/;
const text = "180045678980";

if (re.test(text)) {
   console.log("Es correcto");
}
else {
   console.log("Es incorrecto");
}
*/