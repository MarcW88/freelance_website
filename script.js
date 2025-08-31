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

// FAQ accordion
const accordionItems = document.querySelectorAll('.accordion-item');
accordionItems.forEach(item => {
  const title = item.querySelector('.accordion-title');
  const content = item.querySelector('.accordion-content');

  title.addEventListener('click', () => {
    const isExpanded = title.getAttribute('aria-expanded') === 'true';

    accordionItems.forEach(i => {
      const t = i.querySelector('.accordion-title');
      const c = i.querySelector('.accordion-content');
      t.setAttribute('aria-expanded', 'false');
      c.setAttribute('aria-hidden', 'true');
      i.classList.remove('active');
    });

    if (!isExpanded) {
      title.setAttribute('aria-expanded', 'true');
      content.setAttribute('aria-hidden', 'false');
      item.classList.add('active');
    }
  });
});
