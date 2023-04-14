/* switch For user menu buttons */
const titlePage = document.querySelector(".title-page");
let linkUserMenuPage = "";

switch (true) {
    case pathname.startsWith("/my-account/orders/"):
        linkUserMenuPage = document.getElementById("user-orders");
        linkUserMenuPage.classList.add("active-user-menu");
        titlePage.innerHTML = linkUserMenuPage.innerHTML;
        break;
    case pathname === "/my-account/profile/":
        linkUserMenuPage = document.getElementById("user-profile");
        linkUserMenuPage.classList.add("active-user-menu");
        titlePage.innerHTML = linkUserMenuPage.innerHTML;
        break;
    case pathname === "/my-account/address/":
        linkUserMenuPage = document.getElementById("user-address");
        linkUserMenuPage.classList.add("active-user-menu");
        titlePage.innerHTML = linkUserMenuPage.innerHTML;
        break;
    case pathname === "/my-account/points/":
        linkUserMenuPage = document.getElementById("user-points");
        linkUserMenuPage.classList.add("active-user-menu");
        titlePage.innerHTML = linkUserMenuPage.innerHTML;
        break;
};
