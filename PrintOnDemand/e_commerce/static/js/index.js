// Menu Toggle for Mobile View
const menuIcon = document.querySelector('.menu img');
const navbarContainer = document.querySelector('.container1');

menuIcon.addEventListener('click', () => {
    navbarContainer.classList.toggle('active');
});

// Search Bar Focus and Blur Effect
const searchInput = document.querySelector('.search input');
const searchIcon = document.querySelector('.search img');

searchInput.addEventListener('focus', () => {
    searchIcon.style.display = 'none';
});

searchInput.addEventListener('blur', () => {
    if (searchInput.value === '') {
        searchIcon.style.display = 'block';
    }
});

// Scrollable Gallery for Images (box6, box7, box8, box9)
const scrollableContainer = document.querySelector('.scrollable-container');

// Smooth scroll functionality for the image gallery
scrollableContainer.addEventListener('wheel', (e) => {
    if (e.deltaY > 0) {
        scrollableContainer.scrollLeft += 100;
    } else {
        scrollableContainer.scrollLeft -= 100;
    }
});

// Fixed Navbar on Scroll
const navbar = document.querySelector('.navbar');
const mainContainer = document.querySelector('.main');

window.addEventListener('scroll', () => {
    if (window.scrollY > 0) {
        navbar.classList.add('fixed-navbar');
    } else {
        navbar.classList.remove('fixed-navbar');
    }
});

// Toggle active class for navbar items when clicked (optional)
const navItems = document.querySelectorAll('.leftcontainer div');

navItems.forEach(item => {
    item.addEventListener('click', () => {
        navItems.forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');
    });
});

// Make images clickable to open in a modal or link to another page
const imageBoxes = document.querySelectorAll('.box2 img, .box3 img, .box4 img, .box5 img, .box6 img, .box7 img, .box8 img, .box9 img');

imageBoxes.forEach((image) => {
    image.addEventListener('click', (event) => {
        const imageUrl = event.target.src; // Get the image URL
        openImageInModal(imageUrl); // Open the image in a modal
    });
});

// Function to open image in a modal
function openImageInModal(imageUrl) {
    const modal = document.createElement('div');
    modal.classList.add('image-modal');
    
    const modalContent = document.createElement('div');
    modalContent.classList.add('modal-content');
    
    const img = document.createElement('img');
    img.src = imageUrl;
    
    modalContent.appendChild(img);
    modal.appendChild(modalContent);
    
    // Close modal when clicked outside
    modal.addEventListener('click', () => {
        modal.remove();
    });
    
    document.body.appendChild(modal);
}
