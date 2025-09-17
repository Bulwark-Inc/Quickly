document.addEventListener("DOMContentLoaded", () => {
  const darkModeClass = 'dark';
  const html = document.documentElement;

  // Initialize from localStorage
  if (localStorage.getItem('theme') === 'dark') {
    html.classList.add(darkModeClass);
  }

  const refreshIcons = () => {
    if (window.lucide) lucide.createIcons();
  };

  // Toggle on click
  document.querySelectorAll('[data-toggle-dark]').forEach((btn) => {
    btn.addEventListener('click', () => {
      html.classList.toggle(darkModeClass);
      localStorage.setItem('theme', html.classList.contains(darkModeClass) ? 'dark' : 'light');
    });
  });

  refreshIcons();
});
