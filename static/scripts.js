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


    // Opens login/register screen
    const pageMask = document.querySelector('.page-mask');
    const signInScreen = document.querySelector('.sign-in-screen');
    const registerScreen = document.querySelector('.register-screen');
    const signInButton = document.querySelector("#sign-in");
    var currentPage = 0;

    signInButton.addEventListener('click', function(){
        pageMask.classList.toggle('inactive');
        signInScreen.classList.toggle('inactive');
        currentPage = 1;
    });
    
    const registerButton = document.querySelector("#register");
    registerButton.addEventListener('click', function(){
        pageMask.classList.toggle('inactive');
        registerScreen.classList.toggle('inactive');
        currentPage = 2;
    });

    // Closes login/register screen
    const closeButtons = document.querySelectorAll('.login-close');
    for (let i = 0; i < closeButtons.length; i++)    
        closeButtons[i].addEventListener('click', function() {
            pageMask.classList.toggle('inactive');
            if (currentPage == 1) {
                signInScreen.classList.toggle('inactive');
            }
            else if (currentPage == 2) {
                registerScreen.classList.toggle('inactive');
            }
            currentPage = 0;
    });

    // Switches the screen based on which screen user is on
    const registerButtonFooter = document.querySelector('.register-button');
    registerButtonFooter.addEventListener('click', function() {
        signInScreen.classList.toggle('inactive');
        registerScreen.classList.toggle('inactive');
        currentPage = 2;
    });

    const signInButtonFooter = document.querySelector('.signin-button');
    signInButtonFooter.addEventListener('click', function() {
        registerScreen.classList.toggle('inactive');
        signInScreen.classList.toggle('inactive');
        currentPage = 1;
    });

});