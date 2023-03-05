/* switch For user menu buttons */
let linkUserMenuPage = "";
switch (pathname) {
    case "/my-account/orders/":
        linkUserMenuPage = document.getElementById("user-orders");
        linkUserMenuPage.classList.add("active-user-menu");
        break;
    case "/my-account/profile/":
        linkUserMenuPage = document.getElementById("user-profile");
        linkUserMenuPage.classList.add("active-user-menu");
        break;
    case "/my-account/address/":
        linkUserMenuPage = document.getElementById("user-address");
        linkUserMenuPage.classList.add("active-user-menu");
        break;
    case "/my-account/points/":
        linkUserMenuPage = document.getElementById("user-points");
        linkUserMenuPage.classList.add("active-user-menu");
        break;
};