/* switch For menu buttons */
// We use regular expressions to compare the pathnames
const start = /^\/$/;
const store = /^\/store\/$/;
const contact = /^\/contact\/$/;
const myAccount = /^(\/my-account\/)([\s\S]*\/)$/;
const pointsRules = /^\/points-rules\/$/;

let pathname = window.location.pathname;
let linkMenuPage = "";
switch (true) {
    case start.test(pathname):
        linkMenuPage = document.getElementById("start")
        linkMenuPage.classList.add("active");
        break;
    case store.test(pathname):
        linkMenuPage = document.getElementById("store")
        linkMenuPage.classList.add("active");
        break;
    case contact.test(pathname):
        linkMenuPage = document.getElementById("contact")
        linkMenuPage.classList.add("active");
        break;
    case myAccount.test(pathname):
        linkMenuPage = document.getElementById("my-account")
        linkMenuPage.classList.add("active");
        break;
    case pointsRules.test(pathname):
        linkMenuPage = document.getElementById("points-rules")
        linkMenuPage.classList.add("active");
        break;
};
