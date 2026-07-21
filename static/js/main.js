/* ============================================================
   main.js — tiny, dependency-free interactions.
   Two jobs:
     1. Reveal sections as they scroll into view.
     2. Animate skill progress bars to their data-level %.
   Both use IntersectionObserver — the modern, cheap way to ask
   the browser "tell me when this element becomes visible".
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
  // ---- 1. Scroll-reveal ----
  // Every element with class .reveal starts hidden (see CSS).
  // When ~15% of it enters the viewport we add .visible and stop watching.
  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target); // animate once, then forget
        }
      });
    },
    { threshold: 0.15 }
  );
  document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

  // ---- 2. Skill bars ----
  // Each .skill has data-level="NN". When the bar scrolls into view we set
  // the fill width, and CSS transitions it smoothly from 0 to NN%.
  const skillObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const level = entry.target.dataset.level || "0";
          const fill = entry.target.querySelector(".skill-fill");
          if (fill) fill.style.width = level + "%";
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.4 }
  );
  document.querySelectorAll(".skill").forEach((el) => skillObserver.observe(el));
});
