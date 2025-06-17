// Toggle sidebar visibility on mobile
window.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');
  if (toggle && sidebar) {
    toggle.addEventListener('click', () => {
      sidebar.classList.toggle('hidden');
    });
  }
});
