/* Optional progressive feedback helper. Does not execute the business action.
   In a framework, port these states to component lifecycle/event handlers. */
(() => {
  const wrappers = Array.from(document.querySelectorAll('[data-muse-icon-control]'));
  const controls = wrappers.map(wrapper => [wrapper, wrapper.querySelector('button, a')]);
  controls.forEach(([wrapper, control]) => {
    if (!control) return;
    control.addEventListener('pointerenter', event => {
      if (event.pointerType === 'mouse') {
        wrapper.dataset.input = 'mouse';
        delete wrapper.dataset.touchLabel;
        delete wrapper.dataset.labelDismissed;
      }
    });
    control.addEventListener('focus', () => delete wrapper.dataset.labelDismissed);
    control.addEventListener('pointerdown', event => {
      if (control.disabled) return;
      delete wrapper.dataset.labelDismissed;
      wrapper.dataset.pressed = 'true';
      wrapper.dataset.input = event.pointerType === 'mouse' ? 'mouse' : 'touch';
      if (wrapper.dataset.input === 'touch') wrapper.dataset.touchLabel = 'true';
    });
    control.addEventListener('pointercancel', () => {
      delete wrapper.dataset.pressed;
      delete wrapper.dataset.touchLabel;
    });
  });
  document.addEventListener('pointerup', () => wrappers.forEach(wrapper => delete wrapper.dataset.pressed));
  document.addEventListener('pointerdown', event => {
    wrappers.forEach(wrapper => {
      if (!wrapper.contains(event.target)) delete wrapper.dataset.touchLabel;
    });
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') wrappers.forEach(wrapper => {
      wrapper.dataset.labelDismissed = 'true';
      delete wrapper.dataset.touchLabel;
    });
  });
})();
