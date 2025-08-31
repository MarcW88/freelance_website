// Mobile navigation toggle
const navToggle = document.querySelector('.nav-toggle');
const navList = document.querySelector('.nav ul');

navToggle.addEventListener('click', () => {
  navList.classList.toggle('active');
});

// Contact form handler
const contactForm = document.querySelector('#contact-form');
if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(contactForm);
    try {
      const response = await fetch(contactForm.action || '/api/contact', {
        method: contactForm.method || 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Erreur réseau');
      }

      alert('Message envoyé !');
      contactForm.reset();
    } catch (err) {
      console.error(err);
      alert("Une erreur est survenue lors de l'envoi du message.");
    }
  });
}
