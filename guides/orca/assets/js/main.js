// ORCA guide — mobile sidebar toggle and active-link highlighting.
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.querySelector('.mobile-nav-toggle');
    var sidebar = document.querySelector('.sidebar');

    if (toggle && sidebar) {
      toggle.addEventListener('click', function () {
        sidebar.classList.toggle('open');
      });

      // Close sidebar when a nav link is tapped on small screens.
      sidebar.addEventListener('click', function (event) {
        var link = event.target.closest('.nav-list a');
        if (link && window.matchMedia('(max-width: 900px)').matches) {
          sidebar.classList.remove('open');
        }
      });
    }

    // Mark the current page in the ORCA sidebar.
    var currentFile = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    var links = document.querySelectorAll('.sidebar .nav-list a');
    links.forEach(function (link) {
      var href = (link.getAttribute('href') || '').toLowerCase();
      if (href === currentFile) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
      }
    });

    // Copy-to-clipboard buttons on code blocks.
    var isKo = (document.documentElement.lang || '').toLowerCase().indexOf('ko') === 0;
    var labelCopy = isKo ? '복사' : 'Copy';
    var labelCopied = isKo ? '복사됨' : 'Copied';

    function fallbackCopy(text, onDone) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'absolute';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(ta);
      onDone();
    }

    document.querySelectorAll('.content pre > code').forEach(function (code) {
      var pre = code.parentNode;
      if (pre.querySelector('.copy-btn')) return;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'copy-btn';
      btn.textContent = labelCopy;
      btn.setAttribute('aria-label', isKo ? '코드 복사' : 'Copy code to clipboard');
      btn.addEventListener('click', function () {
        var text = code.textContent;
        var flash = function () {
          btn.textContent = labelCopied;
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = labelCopy;
            btn.classList.remove('copied');
          }, 1500);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(flash, function () { fallbackCopy(text, flash); });
        } else {
          fallbackCopy(text, flash);
        }
      });
      pre.appendChild(btn);
    });
  });
})();
