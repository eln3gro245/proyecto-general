// js/main.js
document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const page = link.getAttribute('data-page');
        if (currentPath.includes(page)) {
            link.classList.add('active');
        }
    });
});