// switch For menu buttons
let linkMenuPage = "";
switch (window.location.pathname) {
    case "/":
        linkMenuPage = document.getElementById("start")
        linkMenuPage.classList.add("active");
        break;
    case "/contact/":
        linkMenuPage = document.getElementById("contact")
        linkMenuPage.classList.add("active");
        break;
    case "/user-dashboard/":
        linkMenuPage = document.getElementById("my-account")
        linkMenuPage.classList.add("active");
        break;
    case "/points-rules/":
        linkMenuPage = document.getElementById("points-rules")
        linkMenuPage.classList.add("active");
        break;
};
