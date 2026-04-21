document.addEventListener('DOMContentLoaded', () => {
  // Block focus theft for 1 second after page load
  const blockUntil = Date.now() + 1000;

  window.addEventListener('blur', (e) => {
    if (Date.now() < blockUntil) {
      window.focus();
    }
  }, true);
});