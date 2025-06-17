document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('form-convite');
  const lista = document.getElementById('lista-membros');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const resp = await fetch('/api/equipe/invite/', {method: 'POST', body: formData});
    if (resp.ok) {
      location.reload();
    }
  });

  lista.addEventListener('click', async (e) => {
    if (e.target.dataset.remove) {
      const id = e.target.dataset.remove;
      const resp = await fetch(`/api/equipe/remove/${id}/`, {method: 'POST', headers:{'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value}});
      if (resp.ok) {
        e.target.closest('tr').remove();
      }
    }
  });

  document.getElementById('gerar-cargos').addEventListener('click', async () => {
    const num = document.getElementById('num-cargos').value;
    const fd = new FormData();
    fd.append('tipo', 'cargos');
    fd.append('quantidade', num);
    const resp = await fetch('/api/ai/sugestoes/', {method: 'POST', body: fd});
    if (resp.ok) {
      const data = await resp.json();
      document.getElementById('resultado-cargos').textContent = data.sugestao;
    }
  });

  document.getElementById('gerar-atividades').addEventListener('click', async () => {
    const cargo = document.getElementById('cargo-nome').value;
    const fd = new FormData();
    fd.append('tipo', 'atividades');
    fd.append('cargo', cargo);
    const resp = await fetch('/api/ai/sugestoes/', {method: 'POST', body: fd});
    if (resp.ok) {
      const data = await resp.json();
      document.getElementById('resultado-atividades').textContent = data.sugestao;
    }
  });
});
