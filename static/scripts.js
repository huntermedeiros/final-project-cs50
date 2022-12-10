document.addEventListener('DOMContentLoaded', function() {
    const body = document.querySelector("body");
    const menuButton = document.querySelector(".menu-button");
    const sideNavText = document.querySelectorAll(".side-nav-text");
    const sideNavButton = document.querySelectorAll(".side-nav-button")

    var sideNavState = true;
    menuButton.addEventListener('click', function() {
        if (sideNavState == true) {
            sideNavState = false;
            for (let i = 0; i < sideNavButton.length; i++) {
                sideNavButton[i].style.width = '40px';
            }
            for (let i = 0; i < sideNavText.length; i++) {
                sideNavText[i].style.display = 'none';
            }
            
            body.style.gridTemplateColumns = '60px auto';
        }
        else if (sideNavState == false) {
            sideNavState = true;
            for (let i = 0; i < sideNavButton.length; i++) {
                sideNavButton[i].style.width = '140px';
            }
            for (let i = 0; i < sideNavText.length; i++) {
                sideNavText[i].style.display = 'inline';
            }
            
            body.style.gridTemplateColumns = '160px auto';
        }
    });
});