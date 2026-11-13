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
  document.querySelectorAll('[data-player]').forEach(player => {
    const media = player.querySelector('video');
    const play = player.querySelector('[data-play]');
    const seek = player.querySelector('[data-seek]');
    const time = player.querySelector('[data-time]');
    const mute = player.querySelector('[data-mute]');
    const fullscreen = player.querySelector('[data-fullscreen]');
    const coverPlay = player.querySelector('[data-cover-play]');
    const quality = player.querySelector('[data-quality]');
    const speed = player.querySelector('[data-speed]');
    if (!media || !play || !seek || !time || !mute || !fullscreen || !speed) return;
    if (quality) {
      quality.hidden = true;
      player.classList.remove('has-quality');
      Promise.all([...quality.options].map(option => option.dataset.src
        ? fetch(option.dataset.src, {method: 'HEAD'}).then(response => response.ok).catch(() => false)
        : Promise.resolve(false))).then(available => {
          if (available.every(Boolean)) {
            quality.hidden = false;
            player.classList.add('has-quality');
          }
        });
    }
    const errorNotice = document.createElement('p');
    errorNotice.className = 'video-error';
    errorNotice.setAttribute('role', 'status');
    errorNotice.hidden = true;
    player.querySelector('.work-frame').append(errorNotice);
    media.controls = false;
    const spanish = document.documentElement.lang === 'es';
    const clearError = () => {
      player.classList.remove('has-error');
      errorNotice.hidden = true;
      media.controls = false;
    };
    const showError = () => {
      player.classList.add('has-error');
      player.classList.remove('has-started');
      errorNotice.textContent = spanish
        ? 'No se pudo cargar el video. Toca reproducir para reintentar.'
        : 'Could not load this video. Tap play to try again.';
      errorNotice.hidden = false;
      time.textContent = '—';
      media.controls = false;
      if (quality) quality.disabled = false;
      play.textContent = '▶';
      play.setAttribute('aria-label', spanish ? 'Reintentar video' : 'Retry video');
      play.setAttribute('aria-pressed', 'false');
      if (coverPlay) coverPlay.setAttribute('aria-label', spanish ? 'Reintentar video' : 'Retry video');
    };
    speed.addEventListener('change', () => {
      media.playbackRate = Number(speed.value);
    });
    media.addEventListener('loadedmetadata', () => {
      media.playbackRate = Number(speed.value);
      if (quality) quality.disabled = false;
    });
    const stamp = seconds => `${Math.floor(seconds / 60)}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
    const requestPlay = () => {
      if (player.classList.contains('has-error')) {
        const position = Number.isFinite(media.currentTime) ? media.currentTime : 0;
        clearError();
        media.load();
        if (position) media.addEventListener('loadedmetadata', () => {
          try { media.currentTime = Math.min(position, Math.max(0, media.duration - 0.1)); }
          catch (_) { /* The browser may defer seeking. */ }
        }, {once: true});
      }
      document.querySelectorAll('[data-player] video').forEach(other => { if (other !== media) other.pause(); });
      media.play().catch(error => {
        if (error?.name !== 'AbortError') showError();
      });
    };
    const togglePlay = () => media.paused || media.ended ? requestPlay() : media.pause();
    play.addEventListener('click', togglePlay);
    coverPlay?.addEventListener('click', togglePlay);
    media.addEventListener('click', () => { if (!media.controls) togglePlay(); });
    media.addEventListener('play', () => {
      play.textContent = 'Ⅱ';
      play.setAttribute('aria-label', spanish ? 'Pausar video' : 'Pause video');
      play.setAttribute('aria-pressed', 'true');
    });
    media.addEventListener('canplay', clearError);
    media.addEventListener('playing', () => {
      clearError();
      player.classList.add('has-started');
    });
    media.addEventListener('pause', () => {
      play.textContent = '▶';
      play.setAttribute('aria-label', player.classList.contains('has-error')
        ? (spanish ? 'Reintentar video' : 'Retry video')
        : (spanish ? 'Reproducir video' : 'Play video'));
      play.setAttribute('aria-pressed', 'false');
    });
    media.addEventListener('ended', () => {
      player.classList.remove('has-started');
      play.textContent = '▶';
      play.setAttribute('aria-label', spanish ? 'Volver a reproducir video' : 'Replay video');
      play.setAttribute('aria-pressed', 'false');
    });
    media.addEventListener('timeupdate', () => {
      time.textContent = stamp(media.currentTime);
      if (Number.isFinite(media.duration) && media.duration > 0) seek.value = String(Math.round(media.currentTime / media.duration * 1000));
    });
    // Only players with two verified sources expose this control.
    let qualityChange = 0;
    quality?.addEventListener('change', () => {
      const source = quality.selectedOptions[0]?.dataset.src;
      if (!source || media.getAttribute('src') === source) return;
      const change = ++qualityChange;
      const position = Number.isFinite(media.currentTime) ? media.currentTime : 0;
      const resume = !media.paused;
      const rate = Number(speed.value);
      media.pause();
      clearError();
      player.classList.remove('has-started');
      quality.disabled = true;
      media.src = source;
      media.load();
      media.playbackRate = rate;
      media.addEventListener('loadedmetadata', () => {
        if (change !== qualityChange) return;
        quality.disabled = false;
        media.playbackRate = rate;
        if (position && Number.isFinite(media.duration)) {
          try { media.currentTime = Math.min(position, Math.max(0, media.duration - 0.1)); }
          catch (_) { /* Some mobile browsers defer seeking. */ }
        }
        if (resume) requestPlay();
      }, {once:true});
    });
    seek.addEventListener('input', () => {
      if (Number.isFinite(media.duration) && media.duration > 0) media.currentTime = media.duration * Number(seek.value) / 1000;
    });
    mute.addEventListener('click', () => {
      media.muted = !media.muted;
    });
    media.addEventListener('volumechange', () => {
      mute.textContent = media.muted ? '×' : '◖';
      mute.setAttribute('aria-label', spanish ? (media.muted ? 'Activar sonido' : 'Silenciar video') : (media.muted ? 'Unmute video' : 'Mute video'));
    });
    const nativeFullscreen = () => {
      if (!media.webkitEnterFullscreen) return;
      media.controls = true;
      try { media.webkitEnterFullscreen(); } catch (_) { media.controls = false; }
    };
    fullscreen.addEventListener('click', () => {
      if (document.fullscreenElement) document.exitFullscreen();
      else if (player.requestFullscreen) {
        try { Promise.resolve(player.requestFullscreen()).catch(nativeFullscreen); }
        catch (_) { nativeFullscreen(); }
      }
      else nativeFullscreen();
    });
    media.addEventListener('webkitendfullscreen', () => { media.controls = false; });
    media.addEventListener('error', () => {
      if (media.error?.code !== MediaError.MEDIA_ERR_ABORTED) showError();
    });
  });

  const observer = 'IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches
    ? new IntersectionObserver((entries) => {
        entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('in'); observer.unobserve(entry.target); } });
      }, {threshold: 0.08}) : null;
  document.querySelectorAll('.reveal').forEach(el => observer ? observer.observe(el) : el.classList.add('in'));
})();
