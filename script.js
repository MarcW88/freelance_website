// Mobile navigation toggle
const navToggle = document.querySelector('.nav-toggle');
const navList = document.querySelector('.nav ul');

navToggle.addEventListener('click', () => {
  navList.classList.toggle('active');
});

// Contact form handler
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Message envoyé !');
    contactForm.reset();
  });
}
