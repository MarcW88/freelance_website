// Mobile navigation toggle
const navToggle = document.querySelector('.nav-toggle');
const navList = document.querySelector('.nav ul');

navToggle.addEventListener('click', () => {
  navList.classList.toggle('active');
});

// Contact form handler
const contactForm = document.querySelector('#contact-form');
const formStatus = document.querySelector('.form-status');
if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    formStatus.textContent = '';
    formStatus.classList.remove('success', 'error');

    const formData = new FormData(contactForm);
    try {
      const response = await fetch(contactForm.action || '/api/contact', {
        method: contactForm.method || 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Erreur réseau');
      }

      formStatus.textContent = 'Message envoyé !';
      formStatus.classList.add('success');
      contactForm.reset();
    } catch (err) {
      console.error(err);
      formStatus.textContent = "Une erreur est survenue lors de l'envoi du message.";
      formStatus.classList.add('error');
    }
  });
}

