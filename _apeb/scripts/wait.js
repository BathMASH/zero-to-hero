// Lazy-load heavy external iframes (Numbas, Desmos, Vimeo) until they are
// near the viewport. This prevents two problems:
//
// 1. Severe scroll jumps on page load in Firefox when Numbas content
//    autofocuses an input element inside a cross-origin iframe. Firefox
//    scrolls the parent page to bring the focused element into view.
//
// 2. Unnecessary network requests and rendering work for embeds that are
//    far below the fold and may never be viewed.
//
// The original version of this script caused scroll jumps by restoring
// iframe.src on scroll via IntersectionObserver (rootMargin: 200px).
// The new version defers loading with a negative rootMargin so the iframe
// only starts loading when the user is already scrolling toward it.

(function() {
  'use strict';

  const LAZY_DOMAINS = [
    'numbas.mathcentre.ac.uk',
    'desmos.com',
    'vimeo.com',
    'player.vimeo.com'
  ];

  function shouldLazyLoad(src) {
    return LAZY_DOMAINS.some(function(domain) {
      return src.indexOf(domain) !== -1;
    });
  }

  // Restore src only when the iframe is within 200px of entering the
  // viewport from below. This gives the embed time to load while the user
  // is scrolling toward it, without loading so early that the user might
  // scroll past before it finishes.
  var io = new IntersectionObserver(function(entries) {
    for (var i = 0; i < entries.length; i++) {
      var entry = entries[i];
      if (entry.isIntersecting) {
        var iframe = entry.target;
        var src = iframe.getAttribute('data-src');
        if (src) {
          iframe.removeAttribute('data-src');
          iframe.setAttribute('src', src);
        }
        io.unobserve(iframe);
      }
    }
  }, {
    rootMargin: '0px 0px -200px 0px',
    threshold: 0
  });

  function processIframe(iframe) {
    if (iframe.hasAttribute('data-wait-processed')) return;
    iframe.setAttribute('data-wait-processed', 'true');

    var src = iframe.getAttribute('src');
    if (src && shouldLazyLoad(src)) {
      iframe.setAttribute('data-src', src);
      iframe.removeAttribute('src');
      io.observe(iframe);
    }
  }

  // Catch iframes as the browser parses the document.
  var mo = new MutationObserver(function(mutations) {
    for (var i = 0; i < mutations.length; i++) {
      var added = mutations[i].addedNodes;
      for (var j = 0; j < added.length; j++) {
        var node = added[j];
        if (node.tagName === 'IFRAME') {
          processIframe(node);
        } else if (node.querySelectorAll) {
          var iframes = node.querySelectorAll('iframe');
          for (var k = 0; k < iframes.length; k++) {
            processIframe(iframes[k]);
          }
        }
      }
    }
  });

  mo.observe(document.documentElement, { childList: true, subtree: true });

  // Safety net: process any iframes already in the DOM (e.g. if this
  // script was injected after parsing finished).
  var existing = document.querySelectorAll('iframe');
  for (var i = 0; i < existing.length; i++) {
    processIframe(existing[i]);
  }
})();
