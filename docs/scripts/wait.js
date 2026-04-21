document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('iframe[src*="numbas"]').forEach(iframe => {
    const src = iframe.getAttribute('src');
    iframe.removeAttribute('src');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
        if (entry.isIntersecting) {
            iframe.src = src;
            observer.unobserve(iframe);
        }
        });
    }, { rootMargin: '200px' });

    observer.observe(iframe);
    });
});