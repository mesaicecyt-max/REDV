
const btn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');
function openMenu(){ sidebar?.classList.add('open'); overlay?.classList.remove('hidden');}
function closeMenu(){ sidebar?.classList.remove('open'); overlay?.classList.add('hidden');}
btn?.addEventListener('click', ()=> sidebar.classList.contains('open') ? closeMenu() : openMenu());
overlay?.addEventListener('click', closeMenu);
// Search
const idx = [
  {slug:'index', title:'Inicio — REDES V', group:'Inicio'},
  {slug:'mapa', title:'Mapa del sitio', group:'Anexo'},
  {slug:'objetivos-aprendizaje-1', title:"1.1 Objetivos de Aprendizaje I", group:"UNIDAD I"},
  {slug:'evolucion-historica', title:"1.2 Evolución Histórica de las Redes", group:"UNIDAD I"},
  {slug:'capa-1-fisica', title:"1.3 Capa 1: Física", group:"UNIDAD I"},
  {slug:'actividad-capa-1', title:"1.4 Actividad — Capa 1", group:"UNIDAD I"},
  {slug:'capa-2-enlace', title:"1.5 Capa 2: Enlace de Datos", group:"UNIDAD I"},
  {slug:'actividad-capa-2', title:"1.6 Actividad — Capa 2", group:"UNIDAD I"},
  {slug:'capa-3-red', title:"1.7 Capa 3: Red", group:"UNIDAD I"},
  {slug:'actividad-capa-3', title:"1.8 Actividad — Capa 3", group:"UNIDAD I"},
  {slug:'capa-4-transporte', title:"1.9 Capa 4: Transporte", group:"UNIDAD I"},
  {slug:'actividad-capa-4', title:"1.10 Actividad — Capa 4", group:"UNIDAD I"},
  {slug:'capas-5-7', title:"1.11 Capas 5–7: Sesión, Presentación y Aplicación", group:"UNIDAD I"},
  {slug:'actividad-capas-567', title:"1.12 Actividad — Capas 5/6/7", group:"UNIDAD I"},
  {slug:'examen-capa-1', title:"1.13 Examen — Capa 1 Física", group:"UNIDAD I"},
  {slug:'examen-capa-2', title:"1.14 Examen — Capa 2 Enlace", group:"UNIDAD I"},
  {slug:'examen-capa-3', title:"1.15 Examen — Capa 3 Red", group:"UNIDAD I"},
  {slug:'punto-a-punto', title:"2.1 Punto a Punto", group:"UNIDAD II"},
  {slug:'topologia-bus', title:"2.2 Topología Bus", group:"UNIDAD II"},
  {slug:'topologia-anillo', title:"2.3 Topología Anillo", group:"UNIDAD II"},
  {slug:'topologia-estrella', title:"2.4 Topología Estrella", group:"UNIDAD II"},
  {slug:'topologia-malla', title:"2.5 Topología Malla", group:"UNIDAD II"},
  {slug:'topologia-hibrida', title:"2.6 Topología Híbrida", group:"UNIDAD II"},
  {slug:'fisica-vs-logica', title:"2.7 Física vs Lógica", group:"UNIDAD II"},
  {slug:'evaluacion-topologias', title:"2.8 Evaluación — Topologías", group:"UNIDAD II"},
  {slug:'medios-transmision', title:"2.9 Medios de Transmisión", group:"UNIDAD II"},
  {slug:'tendencias-actuales', title:"2.10 Tendencias Actuales", group:"UNIDAD II"},
  {slug:'componentes-lan', title:"2.11 Componentes de Red LAN", group:"UNIDAD II"},
  {slug:'cableado-rj45', title:"3.1 Cableado Ethernet RJ45", group:"UNIDAD III"},
  {slug:'redes-virtuales', title:"3.2 Redes Virtuales (VLAN)", group:"UNIDAD III"},
  {slug:'presupuesto-lan', title:"3.3 Presupuesto Red LAN", group:"UNIDAD III"},
  {slug:'wifi6-vs-wifi5', title:"3.4 Wi-Fi 6 vs Wi-Fi 5", group:"UNIDAD III"},
  {slug:'estructura-logica', title:"4.1 Estructura Lógica", group:"PROGRAMACIÓN LÓGICA"},
  {slug:'ejercicios-secuencia', title:"4.2 Ejercicios Secuencia Lógica", group:"PROGRAMACIÓN LÓGICA"},
  {slug:'diagramas-flujo', title:"4.3 Diagramas de Flujo", group:"PROGRAMACIÓN LÓGICA"},
];
const box = document.getElementById('searchBox');
const res = document.getElementById('searchResults');
function renderResults(q){
  if(!q || q.length<2){ res.classList.add('hidden'); res.innerHTML=''; return;}
  q=q.toLowerCase();
  const hits = idx.filter(x=> (x.title.toLowerCase().includes(q) || x.group.toLowerCase().includes(q) || x.slug.includes(q))).slice(0,8);
  if(!hits.length){ res.innerHTML=`<div class="search-item"><strong>Sin resultados</strong><span>Prueba con “capa”, “topología”, “VLAN”</span></div>`; res.classList.remove('hidden'); return;}
  res.innerHTML = hits.map(h=> `<a class="search-item" href="${h.slug}.html"><strong>${h.title}</strong><span>${h.group} · ${h.slug}.html</span></a>`).join('');
  res.classList.remove('hidden');
}
box?.addEventListener('input', e=> renderResults(e.target.value));
box?.addEventListener('focus', e=> renderResults(e.target.value));
document.addEventListener('click', e=>{ if(!e.target.closest('.search-wrap')){ res?.classList.add('hidden'); }});
document.addEventListener('keydown', e=>{ if(e.key==='/' && document.activeElement!==box){ e.preventDefault(); box?.focus(); } if(e.key==='Escape'){ res?.classList.add('hidden'); closeMenu(); }});
// Progress: mark visited links (optional localStorage)
try{
  const v = JSON.parse(localStorage.getItem('redv_visited')||'[]');
  const cur = location.pathname.split('/').pop();
  if(cur && !v.includes(cur)){ v.push(cur); localStorage.setItem('redv_visited', JSON.stringify(v)); }
}catch(e){}
