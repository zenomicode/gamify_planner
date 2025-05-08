async function loadComponent(path, target) {
  try {
    let response = await fetch(path);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    let html = await response.text();
    
    // Добавляем проверку активной страницы
    const currentPage = window.location.pathname.split('/').pop() || 'profile.html';
    html = html.replace(/href="([^"]+)"/g, (match, href) => {
      const page = href.split('/').pop();
      return currentPage === page ? `${match} class="active"` : match;
    });
    
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    target.appendChild(doc.body.firstChild);
  } catch (err) {
    console.error(`Error loading ${path}:`, err);
  }
}

async function initPage() {
  const headerWrapper = document.getElementById('header-wrapper');
  
  if (!headerWrapper) {
    console.error('Header wrapper not found!');
    return;
  }

  // Загружаем компоненты последовательно
  await loadComponent('includes/header.html', headerWrapper);
  await loadComponent('includes/desktop-menu.html', document.body);
  await loadComponent('includes/mobile-menu.html', document.body);
  
  // Подключаем скрипты
  const script = document.createElement('script');
  script.src = 'js/menu.js';
  document.body.appendChild(script);
}

// Запускаем после полной загрузки DOM
if (document.readyState === 'complete') {
  initPage();
} else {
  document.addEventListener('DOMContentLoaded', initPage);
}