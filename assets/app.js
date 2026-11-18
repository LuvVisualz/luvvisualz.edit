(() => {
  'use strict';
  const header = document.querySelector('.site-header');
  const menuButton = document.querySelector('[data-menu-button]');
  const menu = document.querySelector('[data-menu]');
  const scrim = document.querySelector('[data-menu-scrim]');
  let previousFocus = null;
  let lastScrollY = Math.max(0, window.scrollY);
  let scrollTravel = 0;
  let scrollDirection = 0;
  let wantsHeader = true;
  let headerFrame = 0;
  function updateHeader() {
    if (!header) return;
    const y = Math.max(0, window.scrollY);
    const delta = y - lastScrollY;
    const direction = Math.sign(delta);
    const menuOpen = menu?.classList.contains('open');
    const focusInHeader = !!header.querySelector(':focus-visible');
    const atTop = y <= 8;
    if (atTop || menuOpen || focusInHeader) {
      wantsHeader = true;
      scrollTravel = 0;
    } else if (direction) {
      if (direction !== scrollDirection) scrollTravel = 0;
      scrollTravel += Math.abs(delta);
      if (scrollTravel >= 18) {
        wantsHeader = direction < 0;
        scrollTravel = 0;
      }
    }
    if (direction) scrollDirection = direction;
    lastScrollY = y;
    const height = header.getBoundingClientRect().height;
    const controlsAtTop = !atTop && !menuOpen && [...document.querySelectorAll('.video-controls')]
      .some(controls => {
        const rect = controls.getBoundingClientRect();
        return rect.top < height && rect.bottom > 0;
      });
    header.classList.toggle('header-scrolled', !atTop);
    header.classList.toggle('header-away', !atTop && !menuOpen && !focusInHeader && (!wantsHeader || controlsAtTop));
    header.classList.toggle('menu-visible', !!menuOpen);
  }
  window.addEventListener('scroll', () => {
    if (headerFrame) return;
    headerFrame = requestAnimationFrame(() => { headerFrame = 0; updateHeader(); });
  }, {passive: true});
  window.addEventListener('resize', updateHeader);
  header?.addEventListener('focusin', updateHeader);
  header?.addEventListener('focusout', () => requestAnimationFrame(updateHeader));
  updateHeader();
  function setMenu(open) {
    if (!menu || !menuButton || !scrim) return;
    if (open) previousFocus = document.activeElement;
    menu.classList.toggle('open', open);
    scrim.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-hidden', String(!open));
    menu.inert = !open;
    updateHeader();
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
    const coverPlay = player.querySelector('[data-cover-play]');
    const seek = player.querySelector('[data-seek]');
    const time = player.querySelector('[data-time]');
    const mute = player.querySelector('[data-mute]');
    const volume = player.querySelector('[data-volume]');
    const volumeControl = player.querySelector('.volume-control');
    const fullscreen = player.querySelector('[data-fullscreen]');
    const speed = player.querySelector('[data-speed]');
    const quality = player.querySelector('[data-quality]');
    const frame = player.querySelector('.work-frame');
    if (!media || !play || !coverPlay || !seek || !time || !mute || !fullscreen || !speed || !frame) return;

    const spanish = document.documentElement.lang === 'es';
    const label = (es, en) => spanish ? es : en;
    const stamp = seconds => `${Math.floor(seconds / 60)}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
    frame.style.setProperty('--video-poster', `url("${media.poster}")`);
    media.controls = false;
    let lastVolume = media.volume || 1;
    let switching = null;
    let qualityChange = 0;
    const rates = [1, 1.5, 2];
    let speedIndex = 0;
    const speedText = rate => rate === 1.5 && spanish ? '1,5×' : `${rate}×`;
    function updateSpeed() {
      const rate = rates[speedIndex];
      const next = rates[(speedIndex + 1) % rates.length];
      media.playbackRate = rate;
      speed.textContent = speedText(rate);
      speed.setAttribute('aria-label', label(
        `Velocidad de reproducción: ${speedText(rate)}. Activar ${speedText(next)}`,
        `Playback speed: ${speedText(rate)}. Switch to ${speedText(next)}`));
    }

    // iOS does not allow page controls to change media.volume. In that case only mute remains.
    let volumeWritable = false;
    try {
      const original = media.volume;
      media.volume = 0.46;
      volumeWritable = Math.abs(media.volume - 0.46) < 0.01;
      media.volume = original;
    } catch (_) { /* Native volume control only. */ }
    const volumeUsable = volumeWritable && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    if (!volumeUsable) volumeControl?.classList.add('no-slider');
    let volumePinned = false;
    let volumeDragging = false;
    let volumeCloseTimer = null;
    function placeVolume() {
      if (!volumeUsable || !volumeControl) return;
      const controls = player.querySelector('.video-controls').getBoundingClientRect();
      const bounds = player.getBoundingClientRect();
      const trigger = volumeControl.getBoundingClientRect();
      const above = trigger.left - bounds.left < 108;
      volumeControl.classList.toggle('volume-above', above);
      if (above) {
        const popupLeft = Math.max(bounds.left + 4, Math.min(trigger.left, bounds.right - 108));
        volumeControl.style.setProperty('--volume-shift', `${Math.round(popupLeft - trigger.left)}px`);
        volumeControl.style.setProperty('--volume-clearance', `${Math.ceil(trigger.bottom - controls.top + 4)}px`);
      }
    }
    function openVolume() {
      if (!volumeUsable) return;
      clearTimeout(volumeCloseTimer);
      placeVolume();
      volumeControl.classList.add('is-open');
    }
    function closeVolume() {
      clearTimeout(volumeCloseTimer);
      volumeControl?.classList.remove('is-open');
    }
    function scheduleVolumeClose() {
      clearTimeout(volumeCloseTimer);
      volumeCloseTimer = setTimeout(() => {
        if (!volumePinned && !volumeDragging && !volumeControl.matches(':hover') &&
            !volumeControl.querySelector(':focus-visible')) closeVolume();
      }, 300);
    }
    if (volumeUsable) {
      volumeControl.addEventListener('pointerenter', openVolume);
      volumeControl.addEventListener('pointerleave', scheduleVolumeClose);
      volumeControl.addEventListener('focusin', openVolume);
      volumeControl.addEventListener('focusout', scheduleVolumeClose);
      volumeControl.addEventListener('keydown', event => {
        if (event.key === 'Escape') {
          event.stopPropagation();
          volumePinned = false;
          mute.focus();
          closeVolume();
        }
      });
      volume?.addEventListener('pointerdown', () => {
        volumeDragging = true;
        openVolume();
      });
      const stopVolumeDrag = () => {
        if (!volumeDragging) return;
        volumeDragging = false;
        scheduleVolumeClose();
      };
      document.addEventListener('pointerup', stopVolumeDrag);
      document.addEventListener('pointercancel', stopVolumeDrag);
      document.addEventListener('pointerdown', event => {
        if (!volumeControl.contains(event.target)) {
          volumePinned = false;
          if (!volumeDragging) closeVolume();
        }
      });
      window.addEventListener('resize', placeVolume);
      document.addEventListener('fullscreenchange', placeVolume);
    }

    const errorNotice = document.createElement('p');
    errorNotice.className = 'video-error';
    errorNotice.setAttribute('role', 'status');
    errorNotice.hidden = true;
    frame.append(errorNotice);

    function updatePlay() {
      const playing = !media.paused && !media.ended;
      play.classList.toggle('playing', playing);
      play.setAttribute('aria-pressed', String(playing));
      play.setAttribute('aria-label', playing
        ? label('Pausar video', 'Pause video')
        : player.classList.contains('has-error')
          ? label('Reintentar video', 'Retry video')
          : media.ended ? label('Volver a reproducir video', 'Replay video')
          : label('Reproducir video', 'Play video'));
      coverPlay.setAttribute('aria-label', player.classList.contains('has-error')
        ? label('Reintentar video', 'Retry video') : label('Reproducir video', 'Play video'));
    }
    function syncVolume() {
      const silent = media.muted || media.volume === 0;
      mute.dataset.volumeState = silent ? 'muted' : media.volume <= 0.5 ? 'low' : 'high';
      mute.setAttribute('aria-pressed', String(silent));
      mute.setAttribute('aria-label', silent ? label('Activar sonido', 'Unmute video') : label('Silenciar video', 'Mute video'));
      if (!silent) lastVolume = media.volume;
      if (volume) volume.value = String(Math.round(media.volume * 100));
    }
    function clearError() {
      player.classList.remove('has-error');
      errorNotice.hidden = true;
      media.controls = false;
      updatePlay();
    }
    function showError() {
      switching = null;
      if (quality) quality.disabled = false;
      player.classList.remove('is-loading', 'is-playing');
      player.classList.add('has-error', 'show-poster');
      errorNotice.textContent = label('No se pudo cargar el video. Toca reproducir para reintentar.',
        'Could not load this video. Tap play to try again.');
      errorNotice.hidden = false;
      time.textContent = '—';
      media.controls = false;
      updatePlay();
    }
    function requestPlay() {
      if (player.classList.contains('has-error')) {
        clearError();
        media.load();
      }
      document.querySelectorAll('[data-player] video').forEach(other => {
        if (other !== media) other.pause();
      });
      media.play().catch(error => {
        if (error?.name !== 'AbortError' && error?.name !== 'NotAllowedError') showError();
      });
    }
    const togglePlay = () => media.paused || media.ended ? requestPlay() : media.pause();
    play.addEventListener('click', togglePlay);
    coverPlay.addEventListener('click', togglePlay);
    media.addEventListener('click', () => { if (!media.controls) togglePlay(); });
    media.addEventListener('play', updatePlay);
    media.addEventListener('playing', () => {
      clearError();
      player.classList.remove('is-loading', 'show-poster');
      player.classList.add('is-playing');
      updatePlay();
    });
    media.addEventListener('pause', () => {
      player.classList.remove('is-playing');
      updatePlay();
    });
    media.addEventListener('ended', () => {
      player.classList.remove('is-playing');
      player.classList.add('show-poster');
      updatePlay();
    });
    media.addEventListener('timeupdate', () => {
      time.textContent = stamp(media.currentTime);
      if (Number.isFinite(media.duration) && media.duration > 0) {
        seek.value = String(Math.round(media.currentTime / media.duration * 1000));
      }
    });
    seek.addEventListener('input', () => {
      if (Number.isFinite(media.duration) && media.duration > 0) {
        media.currentTime = media.duration * Number(seek.value) / 1000;
      }
    });
    speed.addEventListener('click', () => { speedIndex = (speedIndex + 1) % rates.length; updateSpeed(); });
    media.addEventListener('loadedmetadata', updateSpeed);
    updateSpeed();

    function finishSwitch() {
      if (!switching || !switching.seekComplete || media.seeking || media.readyState < 2) return;
      const resume = switching.resume;
      switching = null;
      quality.disabled = false;
      player.classList.remove('is-loading');
      if (resume) requestPlay();
      else player.classList.remove('show-poster');
    }
    quality?.addEventListener('change', () => {
      const source = quality.selectedOptions[0]?.dataset.src;
      if (!source || media.getAttribute('src') === source) return;
      const change = ++qualityChange;
      const position = Number.isFinite(media.currentTime) ? media.currentTime : 0;
      switching = {resume: !media.paused && !media.ended, change, seekComplete: position === 0};
      media.pause();
      player.classList.add('is-loading', 'show-poster');
      quality.disabled = true;
      media.src = source;
      media.load();
      media.addEventListener('loadedmetadata', () => {
        if (!switching || switching.change !== change) return;
        media.playbackRate = rates[speedIndex];
        if (position && Number.isFinite(media.duration)) {
          try { media.currentTime = Math.min(position, Math.max(0, media.duration - 0.1)); }
          catch (_) { switching.seekComplete = true; }
        }
        finishSwitch();
      }, {once: true});
    });
    media.addEventListener('canplay', finishSwitch);
    media.addEventListener('seeked', () => {
      if (switching) switching.seekComplete = true;
      finishSwitch();
    });

    mute.addEventListener('click', () => {
      if (volumeUsable) { volumePinned = !volumePinned; openVolume(); }
      if (media.muted || media.volume === 0) {
        if (media.volume === 0 && volumeWritable) media.volume = lastVolume || 1;
        media.muted = false;
      } else {
        lastVolume = media.volume;
        media.muted = true;
      }
      syncVolume();
    });
    volume?.addEventListener('input', () => {
      if (!volumeWritable) return;
      media.volume = Number(volume.value) / 100;
      media.muted = media.volume === 0;
      syncVolume();
    });
    media.addEventListener('volumechange', syncVolume);
    syncVolume();

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
      } else nativeFullscreen();
    });
    document.addEventListener('fullscreenchange', () => {
      const active = document.fullscreenElement === player;
      fullscreen.setAttribute('aria-pressed', String(active));
      fullscreen.setAttribute('aria-label', active
        ? label('Salir de pantalla completa', 'Exit full screen')
        : label('Pantalla completa', 'Full screen'));
    });
    media.addEventListener('webkitendfullscreen', () => { media.controls = false; });
    media.addEventListener('error', () => {
      if (media.error?.code !== MediaError.MEDIA_ERR_ABORTED) showError();
    });
    updatePlay();
  });

  const observer = 'IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches
    ? new IntersectionObserver((entries) => {
        entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('in'); observer.unobserve(entry.target); } });
      }, {threshold: 0.08}) : null;
  document.querySelectorAll('.reveal').forEach(el => observer ? observer.observe(el) : el.classList.add('in'));
})();
