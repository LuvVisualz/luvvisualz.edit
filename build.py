#!/usr/bin/env python3
"""Build self-contained static ES/EN HTML from the same structural template.
No dependencies, local server, framework, or build service are required to host the output.
"""
from pathlib import Path
from html import escape
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
MEDIA = 'https://luvvisualz.github.io/work/'
BRAND = 'https://luvvisualz.github.io/brand/luv-visualz-logo.webp'
PHONE = '5491138848176'  # Verified on existing public Luv Visualz portfolio
PROJECTS = [
    dict(key='conoflex', image='conoflex/cover.webp', video='conoflex/videos/poste-vial.mp4'),
    dict(key='bienestar', image='bienestar/cover.webp', video='bienestar/videos/silla-e60-hd.mp4'),
    dict(key='lupart', image='lupart/cover.webp', video='lupart/videos/mundial-2026-hangcha.mp4'),
    dict(key='lost', image='artistic/cover.webp', video='artistic/videos/lost-files-01.mp4'),
]
COPY = {
'es': {
 'title':'Editor de vídeo remoto para agencias y empresas | Luv Visualz',
 'description':'Edición de vídeo remota y recurrente para agencias, empresas y creadores. Reels, YouTube y contenido corporativo. Editor externo desde Buenos Aires.',
 'skip':'Saltar al contenido', 'logoAlt':'Luv Visualz — Inicio', 'langSwitch':'English', 'langAria':'View in English', 'availability':'Abierto a colaboraciones', 'menu':'Menú', 'menuOpen':'Abrir menú', 'menuClose':'Cerrar menú',
 'navTop':'Navegación / 2026','nav':[('Servicios','servicios'),('Trabajos','trabajos'),('Proceso','proceso'),('Colaboración','colaboracion'),('Contacto','contacto')], 'navFoot':'Edición de vídeo · Remota',
 'eyebrow':'Luv Visualz / Remote Video Editing', 'hero':['¿TU MATERIAL','ESTÁ CRUDO?','YO TE LO','COCINO'],
 'heroDescription':'Soy editor de vídeo independiente. Convierto tus grabaciones en piezas listas para publicar, para agencias, marcas y creadores que necesitan edición puntual o recurrente.',
 'cta':'Hablemos de tus vídeos', 'seeWork':'Ver trabajos', 'heroAside':'Un editor externo.\nUn proceso claro.', 'heroIndex':'REMOTO / 2026',
 'ticker':['EDIT','DELIVER','REPEAT','CREATE'],
 'servicesKicker':'01 / Qué puedo editar', 'servicesHeading':['EDICIÓN PARA','LO QUE VIENE.'], 'servicesIntro':'Tanto si tienes un equipo de marketing como si necesitas resolver la edición sin ampliar plantilla, puedo integrarme al ritmo de producción que ya tienes.',
 'services':[
  ('01','↗','Contenido vertical','Reels, TikToks y Shorts con ritmo, subtítulos y versiones listas para cada plataforma.'),
  ('02','▶','YouTube y formatos largos','Montaje narrativo, selección de tomas, limpieza de audio y estructura que ayuda a seguir viendo.'),
  ('03','▧','Vídeo de marca y empresa','Piezas comerciales, de producto, institucionales y de comunicación interna o externa.'),
  ('04','≋','Postproducción integral','Montaje, música, efectos, subtítulos, ajustes básicos de color y animaciones sencillas.'),
  ('05','⧉','Versiones y adaptaciones','Distintas duraciones, relaciones de aspecto y exportaciones según cada canal.'),
  ('06','↺','Edición recurrente','Colaboraciones por paquetes de vídeos o acuerdos mensuales, con el flujo y el alcance definidos juntos.'),
 ], 'servicePills':['Premiere Pro','Audio','Color','Subtítulos','Motion simple'],
 'workKicker':'02 / Trabajo real', 'workHeading':['DE LOS BRUTOS','AL RESULTADO.'], 'workIntro':'Una selección de piezas existentes. Abre cada vídeo para ver el resultado; la contribución exacta a cada proyecto puede detallarse al conversar.',
 'projectPlay':'Reproducir vídeo', 'projectLabel':'Edición / Muestra de trabajo',
 'projects':{
   'conoflex':('Conoflex','Producto · Seguridad vial','Contenido de producto y demostración técnica.','Poste vial'),
   'bienestar':('Bienestar & Soluciones','Producto · Formato vertical','Presentación clara de funciones y beneficios del producto.','Smart Lite E60'),
   'lupart':('Lupart / Hangcha','Marca · Industrial','Vídeo vertical de marca y equipamiento.','Mundial 2026 · Hangcha'),
   'lost':('Luv — Lost Files','Proyecto personal · Experimental','Pieza personal centrada en concepto, montaje y estética.','Lost Files 01'),
 },
 'workNote':'Los trabajos se muestran como ejemplos de edición y criterio audiovisual; no representan resultados comerciales medidos ni testimonios. Los créditos por pieza se pueden ampliar.',
 'manifestoTop':'Tu producción no tiene por qué detenerse en el montaje.', 'manifesto':['UN FLUJO DE EDICIÓN','QUE ACOMPAÑA TU RITMO.'],
 'processKicker':'03 / Así trabajamos', 'processHeading':['TU FLUJO.','UN EDITOR MÁS.'], 'processIntro':'Sin convertir tu proceso en algo más complicado. Acordamos criterios, recibo el material y mantenemos las entregas organizadas.',
 'steps':[
  ('01','Conocemos el encargo','Vemos qué publicas, qué material produces, con qué frecuencia y qué referencias visuales tienes.'),
  ('02','Alineamos criterios','Definimos formatos, estilo de edición, identidad de marca, entregables y modo de intercambio de archivos.'),
  ('03','Edito y comparto','Organizo los brutos, construyo el montaje y presento las piezas para revisión.'),
  ('04','Ajustamos y seguimos','Integro el feedback acordado, exporto los archivos y dejamos preparado el siguiente ciclo.'),
 ],
 'collabKicker':'04 / Pensado para la continuidad', 'collabHeading':['MENOS FRICCIÓN.','MÁS CAPACIDAD.'], 'collabText':'Puedes contar con edición externa cuando tu equipo ya está al límite, cuando necesitas una producción mensual constante o cuando simplemente prefieres delegar el montaje. El volumen, los plazos y el tipo de piezas se acuerdan según cada necesidad.',
 'collabPoints':[('01 / Integración','Trabajo con tu material y tus lineamientos.'),('02 / Flexibilidad','Paquetes por volumen o acuerdos mensuales.'),('03 / Claridad','Alcance, entregas y revisiones definidos antes de comenzar.')],
 'faqKicker':'05 / Preguntas habituales', 'faqTitle':['SIN','VUELTAS.'],
 'faq':[
  ('¿Necesito tener una agencia para trabajar contigo?','No. Trabajo tanto con agencias como con empresas, responsables de marketing y creadores que necesitan un editor externo.'),
  ('¿También aceptas un vídeo individual?','Sí. La prioridad son las colaboraciones recurrentes, pero podemos empezar por una pieza concreta si tiene sentido para el proyecto.'),
  ('¿Tengo que grabar el material?','Normalmente sí: el servicio está centrado en la edición remota de material que tú o tu equipo ya habéis producido. Podemos definir juntos qué archivos hacen falta.'),
  ('¿Cuánto cuesta un acuerdo mensual?','Depende de la cantidad de piezas, el tipo de edición, la duración y la frecuencia. Prefiero conocer tu flujo y preparar una propuesta adecuada.'),
  ('¿Cómo coordinamos desde otro país?','Trabajo desde Buenos Aires y coordinamos las entregas, comentarios y reuniones de acuerdo con el horario y la dinámica de cada equipo.'),
 ],
 'contactKicker':'06 / Empecemos a hablar', 'contactHeading':['TIENES EL MATERIAL.','HABLEMOS DE EDITARLO.'], 'contactText':'Cuéntame qué tipo de vídeos haces, cuántos necesitas al mes y cómo trabaja tu equipo. Podemos ver si encajamos y definir un primer paso.',
 'contactButton':'Contarme qué necesitas', 'contactLocation':'Buenos Aires, Argentina', 'contactRemote':'Colaboraciones remotas', 'contactPricing':'Propuestas a medida', 'footerTag':'Edición remota · Colaboraciones recurrentes', 'backTop':'Volver arriba ↑', 'modalClose':'Cerrar ✕',
 'waMessage':'Hola Luv, vi tu web de edición. Quiero contarte qué vídeos necesitamos editar y consultar una colaboración.',
},
'en': {
 'title':'Remote Video Editor for Agencies & Brands | Luv Visualz',
 'description':'Remote video editing for marketing agencies, brands and creators. Reels, YouTube videos and corporate content, with ongoing editing support.',
 'skip':'Skip to content', 'logoAlt':'Luv Visualz — Home', 'langSwitch':'Español', 'langAria':'Ver web en español', 'availability':'Open to collaborations', 'menu':'Menu', 'menuOpen':'Open menu', 'menuClose':'Close menu',
 'navTop':'Navigation / 2026','nav':[('Services','servicios'),('Work','trabajos'),('Process','proceso'),('Collaboration','colaboracion'),('Contact','contacto')], 'navFoot':'Video editing · Remote',
 'eyebrow':'Luv Visualz / Remote Video Editing', 'hero':['GOT RAW','FOOTAGE?','I’LL COOK IT'],
 'heroDescription':'I’m an independent video editor. I turn raw footage into finished videos for agencies, brands and creators — one-off projects or ongoing collaborations.',
 'cta':'Let’s talk editing', 'seeWork':'Explore the work', 'heroAside':'One external editor.\nOne clear workflow.', 'heroIndex':'REMOTE / 2026',
 'ticker':['EDIT','DELIVER','REPEAT','CREATE'],
 'servicesKicker':'01 / What I edit', 'servicesHeading':['VIDEO EDITING','FOR WHAT’S NEXT.'], 'servicesIntro':'Whether you run a marketing team or simply want to outsource editing without hiring in-house, I can fit into your existing production workflow.',
 'services':[
  ('01','↗','Short-form content','Reels, TikToks and Shorts with pacing, captions and platform-ready versions.'),
  ('02','▶','YouTube & long-form','Story-driven cuts, footage selection, audio cleanup and a structure built for watching.'),
  ('03','▧','Brand & corporate videos','Commercial, product, institutional and internal or external communications content.'),
  ('04','≋','Post-production','Editing, music, SFX, captions, basic color adjustment and simple motion graphics.'),
  ('05','⧉','Versions & cutdowns','Different lengths, aspect ratios and export formats for each channel.'),
  ('06','↺','Ongoing editing','Video bundles or monthly agreements, with scope and workflow defined together.'),
 ], 'servicePills':['Premiere Pro','Audio','Color','Captions','Simple motion'],
 'workKicker':'02 / Real work', 'workHeading':['FROM RAW','TO READY.'], 'workIntro':'A selection of existing pieces. Open each video to see the work; specific contributions can be discussed per project.',
 'projectPlay':'Play video', 'projectLabel':'Editing / Work sample',
 'projects':{
   'conoflex':('Conoflex','Product · Road safety','Product-focused content and technical demonstration.','Road post'),
   'bienestar':('Bienestar & Soluciones','Product · Vertical video','A clear look at product functions and benefits.','Smart Lite E60'),
   'lupart':('Lupart / Hangcha','Brand · Industrial','Vertical content for an industrial equipment brand.','2026 World Cup · Hangcha'),
   'lost':('Luv — Lost Files','Personal · Experimental','A personal piece focused on concept, pacing and visual style.','Lost Files 01'),
 },
 'workNote':'These are samples of audiovisual and editing work, not measured business results or testimonials. Project-specific credits can be shared.',
 'manifestoTop':'Your production should not get stuck in post.', 'manifesto':['EDITING THAT KEEPS','UP WITH YOUR TEAM.'],
 'processKicker':'03 / How we work', 'processHeading':['YOUR WORKFLOW.','ONE MORE EDITOR.'], 'processIntro':'No need to reinvent your process. We agree on the guidelines, I receive the footage, and we keep delivery organized.',
 'steps':[
  ('01','Talk through the brief','We review your content, footage, publishing rhythm and visual references.'),
  ('02','Align on standards','We define formats, editing style, brand assets, deliverables and file-sharing workflow.'),
  ('03','Edit & share','I organize the footage, shape the edit and send the videos for review.'),
  ('04','Refine & repeat','I apply the agreed feedback, export the final files and prepare for the next cycle.'),
 ],
 'collabKicker':'04 / Built for ongoing work', 'collabHeading':['LESS FRICTION.','MORE CAPACITY.'], 'collabText':'Bring in an external editor when your team is busy, when you need videos every month, or when you simply prefer to delegate post-production. We agree on volume, timelines and deliverables based on your needs.',
 'collabPoints':[('01 / Integration','I work with your footage and brand guidelines.'),('02 / Flexibility','Project bundles or monthly agreements.'),('03 / Clarity','Scope, deliveries and revision process agreed upfront.')],
 'faqKicker':'05 / Common questions', 'faqTitle':['CLEAR','ANSWERS.'],
 'faq':[
  ('Do I need to be an agency to work with you?','No. I work with agencies, companies, marketing teams and creators who need an external video editor.'),
  ('Can we start with a single video?','Yes. Ongoing work is the priority, but a single project can be a good way to get started.'),
  ('Do I need to film the footage?','Usually, yes. The service focuses on remote editing of footage that you or your team have already created. We can discuss the files needed.'),
  ('How much does monthly editing cost?','It depends on video count, editing complexity, duration and delivery frequency. I prefer to learn about your workflow before quoting.'),
  ('How do we collaborate across time zones?','I am based in Buenos Aires, Argentina. We coordinate meetings, feedback and deliveries around the needs and schedules of each team.'),
 ],
 'contactKicker':'06 / Start a conversation', 'contactHeading':['GOT THE FOOTAGE?','LET’S TALK EDITING.'], 'contactText':'Tell me what kind of videos you produce, how often you need them and how your team works. We can see if it is a good fit and choose a first step.',
 'contactButton':'Tell me what you need', 'contactLocation':'Buenos Aires, Argentina', 'contactRemote':'Remote collaborations', 'contactPricing':'Custom proposals', 'footerTag':'Remote editing · Ongoing collaborations', 'backTop':'Back to top ↑', 'modalClose':'Close ✕',
 'waMessage':'Hi Luv, I found your video editing website. I would like to discuss the videos we need edited and a possible collaboration.',
}}

def e(s): return escape(str(s), quote=True)

def html_for(lang):
 d = COPY[lang]
 in_en = lang == 'en'
 assets_prefix = '../' if in_en else './'
 en_href = '../' if in_en else 'en/'
 wa_link = 'https://wa.me/' + PHONE + '?text=' + quote(d['waMessage'])
 def hero_lines():
  classes = ['lead','question','bridge','answer'] if lang == 'es' else ['lead','question','answer']
  def wink():
   return ('<svg class="hero-wink" viewBox="0 0 130 126" width="68" height="66" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">'
           '<path d="M25 17H46L43 39H22Z" fill="currentColor"/>'
           '<path d="M27 66H49L42 94L17 108L30 84Z" fill="currentColor"/>'
           '<path d="M73 11L99 32L110 58L104 91L81 114" fill="none" stroke="currentColor" stroke-width="9" stroke-linejoin="miter"/>'
           '</svg><span class="sr-only"> ;)</span>')
  return ''.join('<span class="hero-line hero-line--'+classes[i]+'">'+e(t)+(wink() if i==len(d['hero'])-1 else '')+'</span>' for i,t in enumerate(d['hero']))
 def headline(lines):return f'{e(lines[0])}<br><span>{e(lines[1])}</span>'
 services = ''.join(f'''<article class="service-card reveal"><span class="num">{e(num)} / EDIT</span><div class="service-icon" aria-hidden="true">{e(icon)}</div><h3>{e(head)}</h3><p>{e(desc)}</p></article>''' for num,icon,head,desc in d['services'])
 projects = ''
 for i,pr in enumerate(PROJECTS):
  name,typ,description,vtitle = d['projects'][pr['key']]
  image = (assets_prefix + 'assets/media/work/' + pr['image'] if (ROOT/'assets/media/work'/pr['image']).is_file() else MEDIA + pr['image'])
  video = (assets_prefix + 'assets/media/work/' + pr['video'] if (ROOT/'assets/media/work'/pr['video']).is_file() else MEDIA + pr['video'])
  projects += f'''<button class="work-card reveal" type="button" data-video-url="{e(video)}" data-poster="{e(image)}" data-video-title="{e(name)} — {e(vtitle)}" aria-label="{e(d['projectPlay'] + ': ' + name)}"><div class="work-frame"><img loading="lazy" decoding="async" src="{e(image)}" alt="{e(name)} — {e(typ)}"><span class="project-code">0{i+1} / LVZ</span><span class="project-pill">▶ VIDEO</span><span class="play" aria-hidden="true">▶</span><span class="work-overlay">{e(d['projectPlay'])} ↗</span></div><h3>{e(name)}</h3><p>{e(typ)} · {e(description)}</p></button>'''
 steps = ''.join(f'''<article class="step reveal"><span class="step-num">{e(num)} / 04</span><h3>{e(head)}</h3><p>{e(desc)}</p></article>''' for num,head,desc in d['steps'])
 collab = ''.join(f'''<div><span>{e(head)}</span><strong>{e(desc)}</strong></div>''' for head,desc in d['collabPoints'])
 faq = ''.join(f'''<details><summary>{e(q)}</summary><p>{e(a)}</p></details>''' for q,a in d['faq'])
 nav = ''.join(f'''<a href="#{e(anchor)}"><small>0{i+1}</small>{e(label)}<b aria-hidden="true">↗</b></a>''' for i,(label,anchor) in enumerate(d['nav']))
 ticker_group = ''.join(f'''<span>{e(item)}</span><i aria-hidden="true">✦</i>''' for item in d['ticker'])
 ticker = '<div class="ticker-group">'+ticker_group+'</div>'
 logo = assets_prefix + 'assets/logo.webp' if (ROOT/'assets/logo.webp').is_file() else BRAND
 brand = f'''<span class="brand-mark"><img src="{e(logo)}" alt="" onerror="this.style.display='none';this.nextElementSibling.style.display='inline-grid'"><span class="brand-letter" aria-hidden="true" style="display:none">LVZ</span></span><span class="brand-name">LUV VISUALZ</span>'''
 return f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#07060a"><meta name="color-scheme" content="dark"><meta name="description" content="{e(d['description'])}"><meta property="og:type" content="website"><meta property="og:title" content="{e(d['title'])}"><meta property="og:description" content="{e(d['description'])}"><meta name="twitter:card" content="summary"><meta name="robots" content="index,follow"><title>{e(d['title'])}</title><link rel="stylesheet" href="{assets_prefix}assets/style-v4.css"><style id="lvz-critical-hero">.hero-wink{{display:inline-block;width:.83em;height:.8em;max-width:1em;max-height:1em;vertical-align:middle}}.ticker-track{{display:flex;flex-flow:row nowrap;white-space:nowrap}}.ticker-track>.ticker-group{{display:flex;flex:0 0 auto;white-space:nowrap;align-items:center}}</style><script defer src="{assets_prefix}assets/app.js"></script><link rel="preconnect" href="https://luvvisualz.github.io"><link rel="icon" href="{e(logo)}" type="image/webp"><script type="application/ld+json">{{"@context":"https://schema.org","@type":"ProfessionalService","name":"Luv Visualz","description":"Remote video editing and post-production","areaServed":"Worldwide","address":{{"@type":"PostalAddress","addressLocality":"Buenos Aires","addressCountry":"AR"}}}}</script></head>
<body><a href="#contenido" class="skip">{e(d['skip'])}</a><div class="noise" aria-hidden="true"></div>
<header class="site-header"><a href="#inicio" class="brand" aria-label="{e(d['logoAlt'])}">{brand}</a><div class="header-side"><a href="{en_href}" hreflang="{'es' if in_en else 'en'}" class="lang" aria-label="{e(d['langAria'])}"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.6 5.5 3.6 9S14.5 18.5 12 21c-2.5-2.5-3.6-5.5-3.6-9S9.5 5.5 12 3Z"/></svg>{e(d['langSwitch'])}</a><button type="button" data-menu-button aria-label="{e(d['menuOpen'])}" aria-expanded="false" aria-controls="mobile-menu" class="menu-toggle"><span class="label">{e(d['menu'])}</span><span class="hamburger" aria-hidden="true"><i></i><i></i></span></button></div></header>
<div class="menu-scrim" data-menu-scrim></div><aside class="menu-panel" id="mobile-menu" data-menu aria-hidden="true"><div class="menu-top">{e(d['navTop'])}</div><nav class="menu-nav" aria-label="{e(d['menu'])}">{nav}</nav><div class="menu-foot"><span>{e(d['navFoot'])}</span><a href="{wa_link}" target="_blank" rel="noopener noreferrer">WhatsApp ↗</a></div></aside>
<main id="contenido">
<section class="hero hero-v3" id="inicio"><div class="hero-grid" aria-hidden="true"></div><div class="hero-glow" aria-hidden="true"></div><div class="hero-geometry" aria-hidden="true"><svg viewBox="0 0 460 560" fill="none"><path d="M220 15L425 150L392 405L165 540L22 350L65 115Z"/><path d="M220 55L386 170L354 377L174 495L66 338L110 145Z"/><path d="M220 15V540M22 350L425 150M65 115L392 405"/><path d="M20 40H140M320 510H450"/></svg></div><div class="wrap"><p class="hero-kicker"><span class="hero-kicker-brand">LUV VISUALZ</span><span class="hero-kicker-divider" aria-hidden="true"></span><span class="hero-kicker-service">REMOTE VIDEO EDITING</span></p><h1 class="hero-heading">{hero_lines()}</h1><div class="hero-bottom"><div class="hero-offer"><p>{e(d['heroDescription'])}</p><div class="hero-actions"><a class="button" href="{wa_link}" target="_blank" rel="noopener noreferrer">{e(d['cta'])}<b aria-hidden="true">↗</b></a><a class="text-link" href="#trabajos">{e(d['seeWork'])} ↓</a></div></div></div></div></section>
<div class="ticker-frame" aria-hidden="true"><div class="ticker"><div class="ticker-track">{ticker*20}</div></div></div>
<section class="section" id="servicios"><div class="wrap"><div class="section-heading reveal"><div><p class="kicker">{e(d['servicesKicker'])}</p><h2>{headline(d['servicesHeading'])}</h2></div><p class="section-intro">{e(d['servicesIntro'])}</p></div><div class="service-grid">{services}</div><div class="service-foot">{''.join('<span class="pill">'+e(x)+'</span>' for x in d['servicePills'])}</div></div></section>
<section class="section work" id="trabajos"><div class="wrap"><div class="section-heading reveal"><div><p class="kicker">{e(d['workKicker'])}</p><h2>{headline(d['workHeading'])}</h2></div><p class="section-intro">{e(d['workIntro'])}</p></div><div class="work-grid">{projects}</div><p class="work-note">{e(d['workNote'])}</p></div></section>
<section class="manifesto"><div class="wrap"><div class="signal" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div><p>{e(d['manifestoTop'])}</p><h2>{headline(d['manifesto'])}</h2></div></section>
<section class="section" id="proceso"><div class="wrap"><div class="section-heading reveal"><div><p class="kicker">{e(d['processKicker'])}</p><h2>{headline(d['processHeading'])}</h2></div><p class="section-intro">{e(d['processIntro'])}</p></div><div class="process-grid">{steps}</div></div></section>
<section class="collab" id="colaboracion"><div class="wrap collab-inner"><div class="reveal"><p class="kicker">{e(d['collabKicker'])}</p><h2 class="headline">{headline(d['collabHeading'])}</h2><p>{e(d['collabText'])}</p><a class="text-link" href="#contacto">{e(d['cta'])} ↗</a></div><div class="collab-aside reveal">{collab}</div></div></section>
<section class="faq wrap" id="preguntas"><div class="faq-grid"><div class="reveal"><p class="kicker">{e(d['faqKicker'])}</p><h2>{headline(d['faqTitle'])}</h2></div><div>{faq}</div></div></section>
<section class="contact" id="contacto"><div class="contact-grid" aria-hidden="true"></div><div class="wrap"><p class="kicker">{e(d['contactKicker'])}</p><h2 class="headline">{headline(d['contactHeading'])}</h2><p class="contact-copy">{e(d['contactText'])}</p><a href="{wa_link}" target="_blank" rel="noopener noreferrer" class="button">{e(d['contactButton'])}<b aria-hidden="true">↗</b></a><div class="contact-meta"><span>{e(d['contactLocation'])}</span><span>{e(d['contactRemote'])}</span><span>{e(d['contactPricing'])}</span></div></div></section>
</main><footer class="footer wrap"><a class="brand" href="#inicio" aria-label="{e(d['logoAlt'])}">{brand}</a><p>{e(d['footerTag'])} · © 2026</p><a class="top" href="#inicio">{e(d['backTop'])}</a></footer>
<div class="video-modal" data-video-modal role="dialog" aria-modal="true" aria-hidden="true" aria-label="{e(d['projectPlay'])}"><div class="modal-inner"><div class="modal-bar"><span class="modal-label" data-video-title></span><button data-video-close type="button" class="modal-close">{e(d['modalClose'])}</button></div><video controls playsinline preload="none" controlsList="nodownload" aria-label="{e(d['projectPlay'])}"></video><p class="modal-description">{e(d['workNote'])}</p></div></div></body></html>'''

if __name__ == '__main__':
 (ROOT / 'index.html').write_text(html_for('es'), encoding='utf-8')
 (ROOT / 'en' / 'index.html').write_text(html_for('en'), encoding='utf-8')
 print('Generated ES and EN static pages')
