(() => {
  'use strict';
  const menuButton = document.querySelector('[data-menu-button]');
  const menu = document.querySelector('[data-menu]');
  const scrim = document.querySelector('[data-menu-scrim]');
  let previousFocus = null;
  function setMenu(open) {
    if (!menu || !menuButton || !scrim) return;
    if (open) previousFocus = document.activeElement;
    menu.classList.toggle('open', open);
    scrim.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-hidden', String(!open));
    menu.inert = !open;
    if (open) menu.querySelector('a')?.focus();
    else previousFocus?.focus?.();
  }
  if (menu) menu.inert = true;
  menuButton?.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
  scrim?.addEventListener('click', () => setMenu(false));
  menu?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));

  const dialog = document.querySelector('[data-video-modal]');
  const video = dialog?.querySelector('video');
  const title = dialog?.querySelector('[data-video-title]');
  const close = dialog?.querySelector('[data-video-close]');
  let returnFocus = null;
  function stopVideo() {
    if (!dialog || !video) return;
    video.pause(); video.removeAttribute('src'); video.load();
    dialog.classList.remove('open'); dialog.setAttribute('aria-hidden','true');
    document.body.classList.remove('menu-open');
    returnFocus?.focus?.();
  }
  document.querySelectorAll('[data-video-url]').forEach(button => button.addEventListener('click', () => {
    if (!dialog || !video) return;
    returnFocus = document.activeElement;
    title.textContent = button.dataset.videoTitle || '';
    video.poster = button.dataset.poster || '';
    video.src = button.dataset.videoUrl;
    dialog.classList.add('open'); dialog.setAttribute('aria-hidden','false');
    document.body.classList.add('menu-open');
    close?.focus();
  }));
  close?.addEventListener('click', stopVideo);
  dialog?.addEventListener('click', e => { if (e.target === dialog) stopVideo(); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      if (dialog?.classList.contains('open')) stopVideo();
      else if (menu?.classList.contains('open')) setMenu(false);
    }
    if (e.key === 'Tab' && dialog?.classList.contains('open')) {
      const focusable = dialog.querySelectorAll('button, video[controls]');
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  const observer = 'IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches
    ? new IntersectionObserver((entries) => {
        entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('in'); observer.unobserve(entry.target); } });
      }, {threshold: 0.08}) : null;
  document.querySelectorAll('.reveal').forEach(el => observer ? observer.observe(el) : el.classList.add('in'));
})();
