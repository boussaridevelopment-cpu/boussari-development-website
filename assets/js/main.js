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

  /* ---------- mobile nav ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.style.overflow = open ? "hidden" : "";
      document.body.classList.toggle("menu-open", open);
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("open");
        toggle.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
        document.body.classList.remove("menu-open");
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) toggle.click();
    });
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

  /* ---------- projects gallery filter ---------- */
  var filterBtns = document.querySelectorAll(".filters button");
  var gItems = document.querySelectorAll(".g-item");
  if (filterBtns.length && gItems.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        filterBtns.forEach(function (b) {
          b.classList.remove("on");
          b.setAttribute("aria-pressed", "false");
        });
        btn.classList.add("on");
        btn.setAttribute("aria-pressed", "true");
        var f = btn.getAttribute("data-filter");
        gItems.forEach(function (it) {
          var show = f === "all" || it.getAttribute("data-cat") === f;
          it.classList.toggle("hide", !show);
        });
      });
    });
  }

  /* ---------- forms (local demo handler) ---------- */
  var forms = document.querySelectorAll("form[data-demo-form]");
  forms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      /* honeypot spam check */
      var hp = form.querySelector(".hp-field input");
      if (hp && hp.value !== "") return;
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var ok = form.parentElement.querySelector(".form-success") ||
               form.querySelector(".form-success");
      if (!ok) {
        ok = document.createElement("div");
        ok.className = "form-success";
        ok.innerHTML =
          '<div class="ok-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg></div>' +
          "<h3>Thank you — your request has been recorded.</h3>" +
          "<p>Boussari Development will contact you using your preferred method, typically within one business day. For urgent commercial service, call <a href=\"tel:+14169300400\" class=\"gold\">416-930-0400</a> (24/7).</p>";
        form.parentElement.appendChild(ok);
      }
      form.style.display = "none";
      ok.classList.add("show");
      ok.setAttribute("tabindex", "-1");
      ok.focus();
    });
  });

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
