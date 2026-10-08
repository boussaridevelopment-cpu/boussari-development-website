/* ============================================================
   BOUSSARI DEVELOPMENT — interactions
   ============================================================ */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- header stuck state ---------- */
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-stuck", window.scrollY > 24);
    parallax();
  }

  /* ---------- scroll reveal ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add("in");
            io.unobserve(en.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- subtle parallax ---------- */
  var px = document.querySelectorAll("[data-parallax]");
  var ticking = false;
  function parallax() {
    if (reduceMotion || !px.length || window.innerWidth < 900) return;
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      var vh = window.innerHeight;
      px.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var speed = parseFloat(el.getAttribute("data-parallax")) || 0.06;
        var off = (r.top + r.height / 2 - vh / 2) * -speed;
        el.style.transform = "translate3d(0," + off.toFixed(1) + "px,0)";
      });
      ticking = false;
    });
  }

  /* ---------- animated stat counters ---------- */
  var stats = document.querySelectorAll(".stat .n[data-count]");
  if (stats.length && "IntersectionObserver" in window) {
    var sio = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          var el = en.target;
          sio.unobserve(el);
          var target = parseFloat(el.getAttribute("data-count"));
          if (reduceMotion) { el.textContent = target; return; }
          var t0 = null, dur = 1400;
          function tick(t) {
            if (!t0) t0 = t;
            var p = Math.min((t - t0) / dur, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            el.textContent = Math.round(target * eased);
            if (p < 1) window.requestAnimationFrame(tick);
          }
          window.requestAnimationFrame(tick);
        });
      },
      { threshold: 0.6 }
    );
    stats.forEach(function (el) { sio.observe(el); });
  }

  /* ---------- interactive value map (homepage) ---------- */
  var zoneEls = document.querySelectorAll("[data-zone]");
  if (zoneEls.length) {
    var keys = ["reno", "comm", "base", "invest"];
    var autoTimer = null;
    var setZone = function (k) {
      document.querySelectorAll("[data-zone]").forEach(function (el) {
        el.classList.toggle("on", el.getAttribute("data-zone") === k);
      });
      document.querySelectorAll("[data-panel]").forEach(function (el) {
        el.classList.toggle("on", el.getAttribute("data-panel") === k);
      });
    };
    var stopAuto = function () {
      if (autoTimer) { clearInterval(autoTimer); autoTimer = null; }
    };
    zoneEls.forEach(function (el) {
      el.addEventListener("click", function () { stopAuto(); setZone(el.getAttribute("data-zone")); });
      el.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); stopAuto(); setZone(el.getAttribute("data-zone")); }
      });
    });
    setZone("reno");
    if (!reduceMotion) {
      var zi = 0;
      autoTimer = setInterval(function () { zi = (zi + 1) % keys.length; setZone(keys[zi]); }, 5200);
    }
    /* mouse parallax on the illustrated scene */
    var art = document.querySelector(".xsec-art");
    var layers = art ? art.querySelectorAll("[data-depth]") : [];
    if (art && layers.length && !reduceMotion) {
      art.addEventListener("pointermove", function (e) {
        var r = art.getBoundingClientRect();
        var dx = (e.clientX - r.left - r.width / 2) / r.width;
        var dy = (e.clientY - r.top - r.height / 2) / r.height;
        layers.forEach(function (l) {
          var d = parseFloat(l.getAttribute("data-depth")) || 1;
          l.style.transform = "translate(" + (dx * d * 14).toFixed(1) + "px," + (dy * d * 9).toFixed(1) + "px)";
        });
      });
      art.addEventListener("pointerleave", function () {
        layers.forEach(function (l) { l.style.transform = "translate(0,0)"; });
      });
    }
  }

  /* ---------- hero isometric model ---------- */
  var isoFloors = document.querySelectorAll(".iso-floor");
  var tip = document.getElementById("ha-tip");
  if (isoFloors.length && tip) {
    var tips = {
      reno: "Home Renovation & Improvement — from a door and a floor to a whole-home renovation, with one coordinator from start to close.",
      comm: "Commercial Services — urgent repairs and on-site handyman support for commercial properties, 24/7.",
      base: "Basement Income — a legal second suite with the financing coordinated alongside the build, assessment to rent.",
      invest: "Real Estate & Investment — purchase price, renovation budget, gross rent, cash flow and cap rate looked at together."
    };
    var tipDefault = tip.textContent;
    var isoKeys = ["reno", "comm", "base", "invest"];
    var isoAuto = null;
    var setIso = function (k) {
      isoFloors.forEach(function (f) { f.classList.toggle("on", f.getAttribute("data-key") === k); });
      tip.textContent = tips[k] || tipDefault;
    };
    var stopIso = function () { if (isoAuto) { clearInterval(isoAuto); isoAuto = null; } };
    isoFloors.forEach(function (f) {
      var k = f.getAttribute("data-key");
      f.addEventListener("pointerenter", function () { stopIso(); setIso(k); });
      f.addEventListener("focus", function () { stopIso(); setIso(k); });
      f.addEventListener("pointerleave", function () { f.classList.remove("on"); tip.textContent = tipDefault; });
      f.addEventListener("blur", function () { f.classList.remove("on"); tip.textContent = tipDefault; });
    });
    if (!reduceMotion) {
      var ii = 0;
      isoAuto = setInterval(function () { ii = (ii + 1) % isoKeys.length; setIso(isoKeys[ii]); }, 4200);
    }
  }

  /* ---------- footer year ---------- */
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();

  /* ---------- mobile call bar spacer ---------- */
  if (window.matchMedia("(max-width: 900px)").matches) {
    document.body.classList.add("has-callbar");
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", parallax, { passive: true });
  onScroll();
})();

/* Shared navigation, photo viewer and explicit email handoff. */
(function () {
  'use strict';
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  const serviceDetails = document.querySelector('.nav-services details');
  function closeMenu(returnFocus) {
    if (!toggle || !nav) return;
    nav.classList.remove('open');
    toggle.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    document.body.style.overflow = '';
    document.body.classList.remove('menu-open');
    if (returnFocus) toggle.focus();
  }
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      if (nav.classList.contains('open')) return closeMenu(true);
      nav.classList.add('open');
      toggle.classList.add('is-open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Close menu');
      document.body.style.overflow = 'hidden';
      document.body.classList.add('menu-open');
      nav.querySelector('a').focus();
    });
    nav.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(false); });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        if (nav.classList.contains('open')) closeMenu(true);
        if (serviceDetails && serviceDetails.open) {
          serviceDetails.open = false;
          serviceDetails.querySelector('summary').focus();
        }
      }
      if (e.key !== 'Tab' || !nav.classList.contains('open')) return;
      const stops = [toggle, ...nav.querySelectorAll('a, summary')].filter(el => el.getClientRects().length);
      const first = stops[0], last = stops[stops.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    window.addEventListener('resize', () => { if (window.innerWidth > 900) closeMenu(false); });
  }
  document.addEventListener('click', e => {
    if (serviceDetails && !serviceDetails.contains(e.target)) serviceDetails.open = false;
  });
  if (serviceDetails) serviceDetails.addEventListener('focusout', () => {
    setTimeout(() => { if (!serviceDetails.contains(document.activeElement)) serviceDetails.open = false; }, 0);
  });

  const buttons = [...document.querySelectorAll('[data-filter]')];
  const items = [...document.querySelectorAll('.g-item[data-cat]')];
  const count = document.querySelector('#gallery-count');
  function filter(category, updateURL) {
    buttons.forEach(btn => {
      const selected = btn.dataset.filter === category;
      btn.classList.toggle('on', selected);
      btn.setAttribute('aria-pressed', String(selected));
    });
    items.forEach(item => { item.hidden = category !== 'all' && item.dataset.cat !== category; });
    const visible = items.filter(item => !item.hidden).length;
    if (count) count.textContent = `${visible} ${visible === 1 ? 'photo' : 'photos'}`;
    if (updateURL) {
      const url = new URL(window.location.href);
      if (category === 'all') url.searchParams.delete('category');
      else url.searchParams.set('category', category);
      history.replaceState(null, '', url);
    }
  }
  function restoreFilter() {
    const requested = new URLSearchParams(location.search).get('category');
    filter(buttons.some(b => b.dataset.filter === requested) ? requested : 'all', false);
  }
  if (buttons.length) {
    buttons.forEach(btn => btn.addEventListener('click', () => filter(btn.dataset.filter, true)));
    restoreFilter();
    window.addEventListener('popstate', restoreFilter);
  }

  const dialog = document.querySelector('.photo-dialog');
  if (dialog && typeof dialog.showModal === 'function') {
    const image = dialog.querySelector('.photo-full');
    const caption = dialog.querySelector('#photo-caption');
    const position = dialog.querySelector('.photo-position');
    const links = [...document.querySelectorAll('.photo-open')];
    let active = [], index = 0, opener = null;
    function show(step) {
      index = (step + active.length) % active.length;
      const link = active[index];
      image.src = link.href;
      image.alt = link.querySelector('img').alt;
      caption.textContent = link.dataset.caption;
      position.textContent = `${index + 1} / ${active.length}`;
    }
    links.forEach(link => link.addEventListener('click', e => {
      e.preventDefault();
      opener = link;
      const isComparison = !!link.closest('.comparison-grid');
      active = links.filter(a => !a.closest('[hidden]') && !!a.closest('.comparison-grid') === isComparison);
      show(active.indexOf(link));
      dialog.showModal();
      document.body.style.overflow = 'hidden';
      dialog.querySelector('.photo-close').focus();
    }));
    dialog.querySelector('.photo-close').addEventListener('click', () => dialog.close());
    dialog.querySelector('.photo-prev').addEventListener('click', () => show(index - 1));
    dialog.querySelector('.photo-next').addEventListener('click', () => show(index + 1));
    dialog.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') { e.preventDefault(); show(index + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(index - 1); }
    });
    dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => {
      document.body.style.overflow = '';
      image.removeAttribute('src');
      if (opener) opener.focus();
    });
  }

  document.querySelectorAll('form[data-email-form]').forEach((form, formIndex) => {
    let review;
    form.addEventListener('submit', e => {
      e.preventDefault();
      const honeypot = form.querySelector('.hp-field input');
      if (honeypot && honeypot.value) return;
      if (!form.checkValidity()) return form.reportValidity();
      const lines = ['Hello Boussari Development,', '', 'I would like to discuss a project.', ''];
      form.querySelectorAll('input, select, textarea').forEach(field => {
        if (!field.name || field.closest('.hp-field') || field.type === 'file' || !field.value) return;
        const label = field.labels && field.labels[0] ? field.labels[0].textContent.replace(/\s*\*\s*/g, '').trim() : field.name;
        lines.push(label + ': ' + field.value.trim());
      });
      const body = lines.join('\n');
      if (!review) {
        review = document.createElement('div');
        review.className = 'email-review';
        review.tabIndex = -1;
        const id = 'email-message-' + formIndex;
        review.innerHTML = '<h3>Review your request</h3><p>Your request has not been sent. Open the draft in your email app, attach any photos, then send it. If an email app does not open, copy the message and email <a href="mailto:info@boussaridevelopment.com">info@boussaridevelopment.com</a>.</p><label for="' + id + '">Your message</label><textarea id="' + id + '" readonly></textarea><div class="btn-row"><a class="btn btn-gold email-open">Open email draft</a><button type="button" class="btn btn-ghost email-copy">Copy message</button></div><p class="copy-status" role="status" aria-live="polite"></p>';
        form.after(review);
        review.querySelector('.email-copy').addEventListener('click', async () => {
          const text = review.querySelector('textarea');
          try {
            await navigator.clipboard.writeText(text.value);
            review.querySelector('.copy-status').textContent = 'Message copied. Paste it into your email.';
          } catch (_) {
            text.focus(); text.select();
            review.querySelector('.copy-status').textContent = 'Message selected. Use your device’s copy command.';
          }
        });
      }
      review.querySelector('textarea').value = body;
      review.querySelector('.copy-status').textContent = '';
      review.querySelector('.email-open').href = 'mailto:info@boussaridevelopment.com?subject=' + encodeURIComponent('Project inquiry — Boussari Development') + '&body=' + encodeURIComponent(body);
      review.focus();
    });
  });
})();

document.querySelectorAll("[data-email-submit]").forEach(button => { button.disabled = false; });
