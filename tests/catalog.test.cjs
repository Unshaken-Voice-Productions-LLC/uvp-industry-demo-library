const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function catalog() {
  const elements = {};
  for (const id of ['search', 'industry', 'reset', 'count', 'empty']) {
    elements[id] = {value: '', hidden: false, textContent: '', listeners: {}, focus() { this.focused = true; }, addEventListener(event, fn) { this.listeners[event] = fn; }};
  }
  const cards = [
    {dataset: {industry: 'Automotive', search: 'motor works diagnostics'}},
    {dataset: {industry: 'Education', search: 'kids discovery learning'}}
  ];
  const document = {getElementById: id => elements[id], querySelectorAll: () => cards};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../07_PORTFOLIO_INDEX/catalog.js'), 'utf8'), {document});
  return {elements, cards};
}
test('search filters actual cards and updates count', () => {
  const {elements, cards} = catalog();
  elements.search.value = '  DIAGNOSTICS ';
  elements.search.listeners.input();
  assert.equal(cards[0].hidden, false);
  assert.equal(cards[1].hidden, true);
  assert.equal(elements.count.textContent, '1 of 2 demos');
});
test('industry and search combine, empty state and reset work', () => {
  const {elements, cards} = catalog();
  elements.industry.value = 'Education';
  elements.industry.listeners.change();
  assert.equal(cards[0].hidden, true);
  assert.equal(cards[1].hidden, false);
  elements.search.value = 'missing';
  elements.search.listeners.input();
  assert.equal(elements.empty.hidden, false);
  assert.equal(elements.count.textContent, '0 of 2 demos');
  elements.reset.listeners.click();
  assert.equal(elements.count.textContent, '2 of 2 demos');
  assert.equal(elements.empty.hidden, true);
  assert.equal(elements.search.focused, true);
  assert.ok(cards.every(card => !card.hidden));
});
