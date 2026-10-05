/* Moteur commun des séries d'exercices du cursus allemand.
   Aucune dépendance : chargé en <script src="moteur.js"> par chaque fichier d'exercices,
   il fonctionne aussi bien depuis le site que par double-clic sur le fichier (file://).

   Un fichier d'exercices appelle :
     Exos.demarrer({
       lecon: 4,                       // numéro de la leçon correspondante
       titre: "L'accusatif",
       chrono: 600,                    // secondes, facultatif : minuteur du niveau difficile
       series: { facile: [...], intermediaire: [...], difficile: [...] }
     });

   Types d'exercices acceptés dans une série :
     { t:"qcm",    q:"question",            opts:["a","b","c"], a:0, why:"explication" }
     { t:"trou",   q:"Ich habe ___ Laptop.", fr:"J'ai un portable.", opts:[…], a:0, why:"…" }
     { t:"saisie", q:"consigne",             fr:"indice",        rep:["réponse","variante"], why:"…" }
     { t:"dictee", say:"texte allemand",     rep:["texte allemand"], why:"…" }
     { t:"trad",   q:"phrase en français",   rep:["phrase en allemand","variante"], why:"…" }
*/
var Exos = (function () {
  "use strict";

  var KEY = "cursus.exos.v1";
  var NIVEAUX = [
    ["facile", "Facile", "reconnaître et choisir"],
    ["intermediaire", "Intermédiaire", "compléter et transformer"],
    ["difficile", "Difficile", "produire, traduire, écouter"]
  ];

  /* ---------- utilitaires ---------- */
  function rnd(n) { return Math.floor(Math.random() * n); }
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = rnd(i + 1); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]; }); }
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(o) { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) { } }

  /* supprime la ponctuation finale, réduit les espaces, ß = ss */
  function norm(s, keepCase) {
    var t = String(s == null ? "" : s).replace(/\s+/g, " ").trim().replace(/[.!?;,]+$/, "").replace(/ß/g, "ss");
    return keepCase ? t : t.toLowerCase();
  }
  function deUml(s) { return s.replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/Ä/g, "Ae").replace(/Ö/g, "Oe").replace(/Ü/g, "Ue"); }

  /* compare une saisie à une liste de réponses acceptées.
     retourne { etat:"ok"|"casse"|"umlaut"|"ko", attendu:"…" } */
  function juger(saisie, reps) {
    var i, r;
    for (i = 0; i < reps.length; i++) if (norm(saisie, true) === norm(reps[i], true)) return { etat: "ok", attendu: reps[0] };
    for (i = 0; i < reps.length; i++) if (norm(saisie, false) === norm(reps[i], false)) return { etat: "casse", attendu: reps[i] };
    for (i = 0; i < reps.length; i++) {
      r = reps[i];
      if (deUml(norm(saisie, false)) === deUml(norm(r, false))) return { etat: "umlaut", attendu: r };
    }
    return { etat: "ko", attendu: reps[0] };
  }

  /* ---------- voix allemande ---------- */
  var voix = null;
  function choisirVoix() {
    if (!("speechSynthesis" in window)) return;
    var vs = speechSynthesis.getVoices();
    voix = vs.filter(function (v) { return /^de/i.test(v.lang); })[0] || null;
    var w = document.getElementById("novoice");
    if (w) w.style.display = voix ? "none" : "block";
  }
  if ("speechSynthesis" in window) { choisirVoix(); speechSynthesis.onvoiceschanged = choisirVoix; }
  function dire(texte, vitesse) {
    if (!voix) return false;
    speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(String(texte).replace(/\s*\(.*?\)\s*/g, " "));
    u.voice = voix; u.lang = voix.lang; u.rate = vitesse || 0.85;
    speechSynthesis.speak(u);
    return true;
  }

  /* ---------- état ---------- */
  var CFG = null, niveau = "facile", etat = null, minuteur = null;

  function cle() { return String(CFG.lecon).padStart(4, "0"); }

  function majBarre() {
    var b = document.getElementById("exBar");
    var hist = (load()[cle()] || {});
    var lignes = NIVEAUX.map(function (n) {
      var h = hist[n[0]];
      return '<span><span class="k">' + n[1] + '</span> ' + (h ? h.ok + "/" + h.tot : "—") + "</span>";
    }).join("");
    b.innerHTML =
      '<span><span class="k">justes</span> <b>' + etat.ok + "</b></span>" +
      '<span><span class="k">répondus</span> ' + etat.rep + " / " + etat.total + "</span>" +
      '<span class="grow"></span>' + lignes +
      (etat.chrono != null ? '<span><span class="k">temps</span> <b id="exChrono">' + fmt(etat.chrono) + "</b></span>" : "") +
      '<div class="meterbar"><i style="width:' + (etat.total ? 100 * etat.rep / etat.total : 0) + '%"></i></div>';
  }
  function fmt(s) { var m = Math.floor(s / 60), r = s % 60; return m + ":" + (r < 10 ? "0" : "") + r; }

  function finir() {
    var d = document.getElementById("exDone");
    var pct = etat.total ? Math.round(100 * etat.ok / etat.total) : 0;
    var verdict = pct >= 90 ? "Excellent : ce niveau est acquis, passe au suivant."
      : pct >= 70 ? "Bien. Reprends les points ratés, puis refais la série : les items changent d'ordre."
        : "À retravailler. Relis la fiche de référence de la leçon, puis refais cette série avant de monter de niveau.";
    d.innerHTML =
      '<div class="big">' + etat.ok + " / " + etat.total + " <span class=\"badge " + niveau + "\">" + niveau + "</span></div>" +
      "<p>" + verdict + "</p>" +
      "<ul>" +
      (etat.casse ? "<li><b>" + etat.casse + "</b> réponse(s) justes au mot près mais fautives sur la <b>majuscule</b> : les noms allemands en portent toujours une.</li>" : "") +
      (etat.umlaut ? "<li><b>" + etat.umlaut + "</b> réponse(s) écrites sans Umlaut (ae pour ä). Toléré ici, refusé à l'examen.</li>" : "") +
      "<li>Erreurs : <b>" + (etat.total - etat.ok) + "</b>. Les explications restent affichées au-dessus.</li>" +
      "</ul>" +
      '<div class="acts">' +
      '<button id="exRefaire">Refaire cette série</button>' +
      (niveau !== "difficile" ? '<button class="ghost" id="exMonter">Passer au niveau suivant</button>' : "") +
      '<button class="ghost" id="exRetour">Revoir la leçon ' + CFG.lecon + "</button>" +
      "</div>";
    d.style.display = "block";
    document.getElementById("exRefaire").onclick = function () { rendre(niveau); };
    var mo = document.getElementById("exMonter");
    if (mo) mo.onclick = function () { rendre(niveau === "facile" ? "intermediaire" : "difficile"); };
    document.getElementById("exRetour").onclick = function () { window.location.href = CFG.lien; };
    var h = load(); h[cle()] = h[cle()] || {};
    h[cle()][niveau] = { ok: etat.ok, tot: etat.total, date: new Date().toISOString().slice(0, 10) };
    save(h);
    if (minuteur) { clearInterval(minuteur); minuteur = null; }
    majBarre();
    d.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function compter(ok, nuance) {
    etat.rep++;
    if (ok) etat.ok++;
    if (nuance === "casse") etat.casse++;
    if (nuance === "umlaut") etat.umlaut++;
    majBarre();
    if (etat.rep === etat.total) finir();
  }

  /* ---------- rendu d'un exercice ---------- */
  function bloc(ex, i) {
    var el = document.createElement("div");
    el.className = "ex";
    var head = '<div class="num">Exercice ' + (i + 1) + " / " + etat.total + "</div>";
    var fb = '<div class="fb"></div>';

    if (ex.t === "qcm" || ex.t === "trou") {
      var stem = ex.t === "trou"
        ? esc(ex.q).replace(/___/g, '<span class="gap">___</span>')
        : esc(ex.q);
      el.innerHTML = head + '<div class="stem">' + stem + "</div>" +
        (ex.fr ? '<div class="hint">' + esc(ex.fr) + "</div>" : "") +
        '<div class="opts' + (ex.opts.join("").length > 46 ? " col" : "") + '"></div>' + fb;
      var box = el.querySelector(".opts"), bon = ex.opts[ex.a];
      shuffle(ex.opts.slice()).forEach(function (o) {
        var b = document.createElement("button");
        b.type = "button"; b.textContent = o;
        b.onclick = function () {
          var ok = o === bon;
          Array.prototype.forEach.call(box.children, function (x) {
            x.disabled = true;
            if (x.textContent === bon) x.className = "good";
            else if (x === b) x.className = "bad";
          });
          var f = el.querySelector(".fb");
          f.className = ok ? "fb ok" : "fb ko";
          f.innerHTML = (ok ? "<b>Juste.</b> " : "<b>Non</b>, la réponse est « " + esc(bon) + " ». ") + esc(ex.why || "");
          if (ex.t === "trou") dire(ex.q.replace(/___/g, bon));
          compter(ok);
        };
        box.appendChild(b);
      });
      return el;
    }

    /* saisie, traduction, dictée : même mécanique d'évaluation */
    var consigne = ex.t === "dictee" ? "Écoute et écris ce que tu entends." : esc(ex.q);
    var indice = ex.t === "trad" ? "Écris la phrase en allemand." : (ex.fr ? esc(ex.fr) : "");
    el.innerHTML = head +
      '<div class="stem">' + consigne.replace(/___/g, '<span class="gap">___</span>') + "</div>" +
      (indice ? '<div class="hint">' + indice + "</div>" : "") +
      '<div class="row">' +
      (ex.t === "dictee" ? '<button class="act ghost" data-r="ecouter">Écouter</button><button class="act ghost" data-r="lent">Plus lentement</button>' : "") +
      '<input type="text" autocomplete="off" spellcheck="false" placeholder="ta réponse">' +
      '<button class="act" data-r="valider">Vérifier</button>' +
      "</div>" + fb;

    var inp = el.querySelector("input"), f = el.querySelector(".fb");
    if (ex.t === "dictee") {
      el.querySelector('[data-r=ecouter]').onclick = function () { if (!dire(ex.say)) alert("Aucune voix allemande installée. Lis la correction après avoir tenté ta réponse."); };
      el.querySelector('[data-r=lent]').onclick = function () { dire(ex.say, 0.6); };
    }
    function valider() {
      if (inp.disabled) return;
      var v = juger(inp.value, ex.rep);
      inp.disabled = true;
      el.querySelector('[data-r=valider]').disabled = true;
      var ok = v.etat === "ok" || v.etat === "casse" || v.etat === "umlaut";
      f.className = v.etat === "ok" ? "fb ok" : (ok ? "fb half" : "fb ko");
      var tete = v.etat === "ok" ? "<b>Juste.</b> "
        : v.etat === "casse" ? "<b>Presque :</b> la forme est bonne mais la majuscule ne l'est pas. On écrit « " + esc(v.attendu) + " ». "
          : v.etat === "umlaut" ? "<b>Presque :</b> écris l'Umlaut, « " + esc(v.attendu) + " ». "
            : "<b>Non.</b> Réponse attendue : « " + esc(v.attendu) + " ». ";
      f.innerHTML = tete + esc(ex.why || "") +
        (ex.rep.length > 1 ? ' <span class="fr">Autre formulation acceptée : « ' + esc(ex.rep[1]) + " ».</span>" : "");
      dire(v.attendu);
      compter(ok, v.etat);
    }
    el.querySelector('[data-r=valider]').onclick = valider;
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") valider(); });
    return el;
  }

  /* ---------- rendu d'une série ---------- */
  function rendre(nv) {
    niveau = nv;
    var serie = shuffle((CFG.series[nv] || []).slice());
    etat = { total: serie.length, rep: 0, ok: 0, casse: 0, umlaut: 0, chrono: (nv === "difficile" && CFG.chrono) ? CFG.chrono : null };
    Array.prototype.forEach.call(document.querySelectorAll(".levels button"), function (b) {
      b.className = b.dataset.l === nv ? "on" : "";
    });
    var root = document.getElementById("exList");
    root.innerHTML = "";
    serie.forEach(function (ex, i) { root.appendChild(bloc(ex, i)); });
    document.getElementById("exDone").style.display = "none";
    if (minuteur) { clearInterval(minuteur); minuteur = null; }
    majBarre();
    if (etat.chrono != null) {
      minuteur = setInterval(function () {
        etat.chrono--;
        var c = document.getElementById("exChrono");
        if (c) c.textContent = fmt(Math.max(0, etat.chrono));
        if (etat.chrono <= 0) { clearInterval(minuteur); minuteur = null; if (c) { c.textContent = "0:00"; c.style.color = "#c62828"; } }
      }, 1000);
    }
    root.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  /* ---------- démarrage ---------- */
  function demarrer(cfg) {
    CFG = cfg;
    CFG.lien = cfg.lien || ("../lessons/" + (cfg.fichierLecon || ""));
    var sel = document.getElementById("exLevels");
    sel.innerHTML = NIVEAUX.map(function (n) {
      var nb = (cfg.series[n[0]] || []).length;
      return '<button type="button" data-l="' + n[0] + '"><b>' + n[1] + "</b><small>" + n[2] + " · " + nb + " exercices</small></button>";
    }).join("");
    Array.prototype.forEach.call(sel.querySelectorAll("button"), function (b) {
      b.onclick = function () { rendre(b.dataset.l); };
    });
    rendre("facile");
  }

  return { demarrer: demarrer, dire: dire };
})();
