document.addEventListener('DOMContentLoaded', function() {
    const body = document.querySelector("body");
    const menuButton = document.querySelector(".menu-button");
    const postButton = document.querySelector(".post-button");
    const postButtonText = document.querySelector(".post-button-text");
    const sideNavText = document.querySelectorAll(".side-nav-text");
    const sideNavButtons = document.querySelectorAll(".side-nav-button");

    // Expands and shrinks the side nav bar
    var sideNavState = false;
    menuButton.addEventListener('click', function() {
        if (sideNavState == true) {
            sideNavState = false;
            postButton.style.width = '40px';
            postButtonText.style.display = 'none';
            for (let i = 0; i < sideNavButtons.length; i++) {
                sideNavButtons[i].style.width = '40px';
            }
            for (let i = 0; i < sideNavText.length; i++) {
                sideNavText[i].style.display = 'none';
            }
            body.style.gridTemplateColumns = '60px auto';
        }
        else if (sideNavState == false) {
            sideNavState = true;
            postButton.style.width = '140px';
            postButtonText.style.display = 'inline';
            for (let i = 0; i < sideNavButtons.length; i++) {
                sideNavButtons[i].style.width = '140px';
            }
            for (let i = 0; i < sideNavText.length; i++) {
                sideNavText[i].style.display = 'inline';
            }
            body.style.gridTemplateColumns = '160px auto';
        }
    });


});