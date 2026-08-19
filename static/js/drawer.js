/* drawer.js — Panel lateral genérico (drawer) para acciones sin recargar la Ficha del Paciente.
   Uso:
     crDrawer.open({ url: '/pacientes/nuevo/panel/', title: 'Nuevo paciente' })
   El endpoint debe devolver un fragmento HTML (no una página completa).
   Si el fragmento contiene un <form>, el submit se intercepta vía fetch para
   evitar recarga; si el backend responde con {redirect: url}, navega ahí.
*/
(function(){
  function el(tag, cls){ var e=document.createElement(tag); if(cls) e.className=cls; return e; }

  var backdrop = el('div','cr-drawer-backdrop');
  var drawer = el('div','cr-drawer');
  var header = el('div','cr-drawer-header');
  var title = el('h3','cr-drawer-title');
  var closeBtn = el('button','cr-drawer-close'); closeBtn.type='button'; closeBtn.innerHTML='&times;';
  var body = el('div','cr-drawer-body');
  header.appendChild(title); header.appendChild(closeBtn);
  drawer.appendChild(header); drawer.appendChild(body);

  document.addEventListener('DOMContentLoaded', function(){
    document.body.appendChild(backdrop);
    document.body.appendChild(drawer);
  });

  function getCookie(name){
    var v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return v ? v.pop() : '';
  }

  function close(){
    drawer.classList.remove('is-open');
    backdrop.classList.remove('is-open');
  }
  backdrop.addEventListener('click', close);
  closeBtn.addEventListener('click', close);
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') close(); });

  function bindForms(){
    body.querySelectorAll('form[data-cr-ajax]').forEach(function(form){
      form.addEventListener('submit', function(e){
        e.preventDefault();
        var submitBtn = form.querySelector('button[type=submit]');
        if(submitBtn){ submitBtn.disabled = true; submitBtn.classList.add('is-loading'); }
        fetch(form.action, {
          method: form.method || 'POST',
          headers: {'X-CSRFToken': getCookie('csrftoken'), 'X-Requested-With': 'XMLHttpRequest'},
          body: new FormData(form)
        }).then(function(r){ return r.json().then(function(data){ return {status:r.status, data:data}; }); })
          .then(function(res){
            if(res.data.redirect){
              window.location.href = res.data.redirect;
            } else if(res.data.html){
              body.innerHTML = res.data.html;
              bindForms();
            }
          })
          .catch(function(){
            if(submitBtn){ submitBtn.disabled=false; submitBtn.classList.remove('is-loading'); }
          });
      });
    });
  }

  window.crDrawer = {
    open: function(opts){
      title.textContent = opts.title || '';
      body.innerHTML = '<div class="cr-skeleton" style="height:120px;border-radius:12px;"></div>';
      drawer.classList.add('is-open');
      backdrop.classList.add('is-open');
      fetch(opts.url, {headers:{'X-Requested-With':'XMLHttpRequest'}})
        .then(function(r){ return r.text(); })
        .then(function(html){ body.innerHTML = html; bindForms(); })
        .catch(function(){ body.innerHTML = '<p class="cr-error-text">No se pudo cargar. Intenta de nuevo.</p>'; });
    },
    close: close
  };
})();
