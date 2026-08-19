/* buscador.js — Autocompletado en vivo del buscador global de pacientes (barra superior).
   Construye el DOM con textContent/createElement (nunca innerHTML con datos del
   servidor): nombres y documentos de paciente son texto libre introducido por
   el personal de la clínica y no deben poder inyectar HTML/JS en el navegador
   de quien use el buscador. */
(function(){
  document.addEventListener('DOMContentLoaded', function(){
    var input = document.getElementById('cr-buscador-input');
    var results = document.getElementById('cr-buscador-results');
    if(!input || !results) return;

    var timer = null;
    var currentQuery = '';

    function el(tag, cls, text){
      var e = document.createElement(tag);
      if(cls) e.className = cls;
      if(text !== undefined) e.textContent = text;
      return e;
    }

    function clear(node){ while(node.firstChild) node.removeChild(node.firstChild); }

    function renderVacio(q){
      clear(results);
      var wrap = el('div', 'cr-search-empty');
      wrap.appendChild(el('p', null, 'Sin coincidencias para "' + q + '"'));
      var btn = el('button', 'cr-btn cr-btn-primario cr-btn-sm cr-btn-full', 'Crear paciente "' + q + '"');
      btn.type = 'button';
      btn.addEventListener('click', function(){
        crDrawer.open({url: '/pacientes/nuevo/panel/?q=' + encodeURIComponent(q), title: 'Nuevo paciente'});
      });
      wrap.appendChild(btn);
      results.appendChild(wrap);
      results.classList.add('is-open');
    }

    function render(data, q){
      if(!data.pacientes || data.pacientes.length === 0){
        renderVacio(q);
        return;
      }
      clear(results);
      data.pacientes.forEach(function(p){
        var a = el('a', 'cr-search-item');
        a.href = p.url;
        var info = el('div');
        info.appendChild(el('div', 'cr-search-item-name', p.nombre));
        info.appendChild(el('div', 'cr-search-item-doc', p.tipo_doc + ' ' + p.documento));
        a.appendChild(info);
        var badge = el('span', 'cr-badge cr-badge-' + (p.pendientes > 0 ? 'pendiente' : 'neutro'),
          p.pendientes > 0 ? (p.pendientes + ' pendiente' + (p.pendientes > 1 ? 's' : '')) : 'al día');
        a.appendChild(badge);
        results.appendChild(a);
      });
      results.classList.add('is-open');
    }

    input.addEventListener('input', function(){
      var q = input.value.trim();
      currentQuery = q;
      clearTimeout(timer);
      if(q.length < 2){ results.classList.remove('is-open'); return; }
      timer = setTimeout(function(){
        fetch('/pacientes/buscar-json/?q=' + encodeURIComponent(q))
          .then(function(r){ return r.json(); })
          .then(function(data){ if(q === currentQuery) render(data, q); })
          .catch(function(){
            clear(results);
            var wrap = el('div', 'cr-search-empty');
            wrap.appendChild(el('p', null, 'Error de búsqueda.'));
            results.appendChild(wrap);
            results.classList.add('is-open');
          });
      }, 220);
    });

    document.addEventListener('click', function(e){
      if(!input.contains(e.target) && !results.contains(e.target)) results.classList.remove('is-open');
    });
  });
})();
