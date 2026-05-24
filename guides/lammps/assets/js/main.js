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
  });
})();
