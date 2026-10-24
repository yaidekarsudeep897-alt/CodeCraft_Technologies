document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav-links");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      toggle.setAttribute("aria-label", open ? "Open navigation" : "Close navigation");
      nav.classList.toggle("is-open", !open);
      document.body.classList.toggle("menu-open", !open);
    });
    nav.querySelectorAll("a").forEach(link => link.addEventListener("click", () => {
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open navigation");
      nav.classList.remove("is-open");
      document.body.classList.remove("menu-open");
    }));
  }
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  // Preselect service when arriving from a service card.
  const params = new URLSearchParams(window.location.search);
  const service = params.get("service");
  const select = document.querySelector('select[name="service"]');
  if (service && select) {
    const option = Array.from(select.options).find(o => o.text.toLowerCase() === service.toLowerCase() || o.value.toLowerCase() === service.toLowerCase());
    if (option) select.value = option.value;
  }
});
