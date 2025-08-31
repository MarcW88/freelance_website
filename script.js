// Mobile navigation toggle
const navToggle = document.querySelector('.nav-toggle');
const navList = document.querySelector('.nav ul');

navToggle.addEventListener('click', () => {
  navList.classList.toggle('active');
});

// Simple newsletter form handler (demo)
const form = document.querySelector('.newsletter-form');
form.addEventListener('submit', (e) => {
  e.preventDefault();
  const email = form.querySelector('input').value;
  alert(`Thanks for subscribing, ${email}!`);
  form.reset();
});
