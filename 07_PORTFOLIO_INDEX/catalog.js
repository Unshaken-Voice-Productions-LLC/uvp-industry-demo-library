'use strict';
const search = document.getElementById('search');
const industry = document.getElementById('industry');
const cards = Array.from(document.querySelectorAll('#catalog article'));
function updateCatalog() {
  const term = search.value.trim().toLocaleLowerCase();
  let count = 0;
  for (const card of cards) {
    const visible = (!industry.value || card.dataset.industry === industry.value) && card.dataset.search.includes(term);
    card.hidden = !visible;
    if (visible) count += 1;
  }
  document.getElementById('count').textContent = `${count} of ${cards.length} demos`;
  document.getElementById('empty').hidden = count !== 0;
}
search.addEventListener('input', updateCatalog);
industry.addEventListener('change', updateCatalog);
document.getElementById('reset').addEventListener('click', () => {
  search.value = '';
  industry.value = '';
  updateCatalog();
  search.focus();
});
updateCatalog();
