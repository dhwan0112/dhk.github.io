(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.querySelector('.mobile-nav-toggle');
    var sidebar = document.querySelector('.sidebar');
    if (toggle && sidebar) {
      toggle.addEventListener('click', function () {
        sidebar.classList.toggle('open');
      });
      sidebar.addEventListener('click', function (event) {
        if (event.target.closest('.nav-list a') && window.matchMedia('(max-width: 900px)').matches) {
          sidebar.classList.remove('open');
        }
      });
    }

    var content = document.querySelector('.content');
    if (!content) return;
    var headings = content.querySelectorAll('h2[id]');
    if (headings.length < 3) return;
    var box = document.createElement('div');
    box.className = 'toc';
    var title = document.createElement('div');
    title.className = 'toc-title';
    title.textContent = '이 페이지에서 다룹니다';
    var list = document.createElement('ul');
    headings.forEach(function (h) {
      var item = document.createElement('li');
      var link = document.createElement('a');
      link.href = '#' + h.id;
      link.textContent = h.textContent;
      item.appendChild(link);
      list.appendChild(item);
    });
    box.appendChild(title);
    box.appendChild(list);
    content.insertBefore(box, content.firstChild);
  });
})();
