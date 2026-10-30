(() => {
  // Dismissible feedback messages.
  document.querySelectorAll('.flash').forEach((item) => {
    window.setTimeout(() => { if (item.isConnected) item.remove(); }, 5000);
  });

  // Confirmation prompts for irreversible form actions.
  document.querySelectorAll('form [data-confirm]').forEach((button) => {
    button.closest('form')?.addEventListener('submit', (event) => {
      if (!window.confirm(button.dataset.confirm)) event.preventDefault();
    });
  });

  // Live exam timer and answer progress. The server remains responsible for
  // scoring and persisting the submitted answers.
  const timer = document.getElementById('exam-timer');
  const form = document.getElementById('exam-form');
  if (timer && form) {
    let remaining = Number(timer.dataset.minutes || 30) * 60;
    const renderTime = () => {
      const minutes = Math.floor(Math.max(remaining, 0) / 60).toString().padStart(2, '0');
      const seconds = (Math.max(remaining, 0) % 60).toString().padStart(2, '0');
      timer.textContent = `${minutes}:${seconds}`;
      if (remaining <= 300) timer.style.color = '#d94c65';
    };
    renderTime();
    const tick = window.setInterval(() => {
      remaining -= 1;
      renderTime();
      if (remaining <= 0) {
        window.clearInterval(tick);
        form.requestSubmit();
      }
    }, 1000);
    const radios = [...form.querySelectorAll('input[type="radio"]')];
    const updateProgress = () => {
      const answered = new Set(radios.filter((r) => r.checked).map((r) => r.name)).size;
      const total = document.querySelectorAll('.question-card').length;
      document.getElementById('answered-count').textContent = answered;
      document.getElementById('answer-progress').style.width = `${total ? answered / total * 100 : 0}%`;
    };
    radios.forEach((radio) => radio.addEventListener('change', updateProgress));
  }
})();
