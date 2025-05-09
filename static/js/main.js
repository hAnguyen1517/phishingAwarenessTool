// Form submission handling (for sign-up and sign-in)
const requiredClasses = ['logout-form', 'fake-site-form', 'quiz-form', 'report-form', 'password-form', 'profile-form', 'contact-form', 'profile-form']
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', (e) => {
        // Skip the logout form
        if (requiredClasses.some(cls => form.classList.contains(cls))) {
            return; // Allow the form to submit naturally
        }
        e.preventDefault();
        alert('Form submitted!');
        // Add API integration logic here
    });
});

// Sidebar navigation
document.querySelectorAll('.sidebar ul li a').forEach(link => {
    link.addEventListener('click', () => {
        document.querySelectorAll('.sidebar ul li a').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('active');
            mainContent.classList.remove('dimmed');
            overlay.style.display = 'none';
        }
    });
});

// Dropdown menu
document.querySelector('.user-info').addEventListener('click', (e) => {
    // Only prevent default if the click is not on the logout form, logout button, or profile link
    const isLogoutForm = e.target.closest('.logout-form') || e.target.classList.contains('dropdown-logout');
    const isProfileLink = e.target.tagName === 'A' && e.target.getAttribute('href') === '/dashboard/profile/';
    if (!isLogoutForm && !isProfileLink) {
        e.preventDefault();
        const dropdown = document.querySelector('.dropdown');
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    }
});

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    const dropdown = document.querySelector('.dropdown');
    if (!e.target.closest('.user-info')) {
        dropdown.style.display = 'none';
    }
});

// Hamburger and Close menu toggle
const hamburger = document.querySelector('.hamburger');
const closeBtn = document.querySelector('.close-btn');
const sidebar = document.querySelector('.sidebar');
const mainContent = document.querySelector('.main-content');
const overlay = document.createElement('div');
overlay.className = 'overlay';
document.body.appendChild(overlay);

hamburger.addEventListener('click', () => {
    sidebar.classList.add('active');
    mainContent.classList.add('dimmed');
    overlay.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    sidebar.classList.remove('active');
    mainContent.classList.remove('dimmed');
    overlay.style.display = 'none';
});

overlay.addEventListener('click', () => {
    sidebar.classList.remove('active');
    mainContent.classList.remove('dimmed');
    overlay.style.display = 'none';
});

// Close sidebar if clicking outside on small screens
document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768 && !e.target.closest('.sidebar') && !e.target.classList.contains('hamburger')) {
        sidebar.classList.remove('active');
        mainContent.classList.remove('dimmed');
        overlay.style.display = 'none';
    }
});