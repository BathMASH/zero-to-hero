const observer = new MutationObserver((mutations) => {
  mutations.forEach(mutation => {
    mutation.addedNodes.forEach(node => {
      if (node.nodeName === 'IFRAME' && node.src && node.src.includes('numbas')) {
        const src = node.getAttribute('src');
        node.removeAttribute('src');
        lazyLoad(node, src);
      }
    });
  });
});

observer.observe(document.documentElement, { childList: true, subtree: true });

function lazyLoad(iframe, src) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        iframe.src = src;
        io.unobserve(iframe);
      }
    });
  }, { rootMargin: '200px' });

  io.observe(iframe);
}
