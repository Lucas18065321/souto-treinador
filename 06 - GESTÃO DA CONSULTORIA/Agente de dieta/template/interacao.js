// Dica dos gráficos (só na tela): passar o mouse ou tocar num ponto mostra data, valor e o plano daquela data.
(function () {
  var dica = document.getElementById('dica');
  if (!dica) return;
  function mostrar(alvo, x, y) {
    dica.innerHTML = alvo.getAttribute('data-dica');
    dica.style.display = 'block';
    var w = dica.offsetWidth, h = dica.offsetHeight;
    var left = Math.min(x + 14, window.innerWidth - w - 8), top = y - h - 14;
    if (top < 8) top = y + 18;
    dica.style.left = Math.max(8, left) + 'px';
    dica.style.top = top + 'px';
  }
  function esconder() { dica.style.display = 'none'; }
  document.addEventListener('mousemove', function (ev) {
    var alvo = ev.target.closest && ev.target.closest('[data-dica]');
    if (alvo) mostrar(alvo, ev.clientX, ev.clientY); else esconder();
  });
  document.addEventListener('click', function (ev) {
    var alvo = ev.target.closest && ev.target.closest('[data-dica]');
    if (alvo) { var r = alvo.getBoundingClientRect(); mostrar(alvo, r.left + r.width / 2, r.top); } else esconder();
  });
  window.addEventListener('scroll', esconder, { passive: true });
})();
