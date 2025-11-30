---
marp: true
title: Strassenverkehrsamt ZH // E-Dossier AKTIVIERUNG
paginate: true
theme: default
class: gaming
---

<style>
/* === Global Gaming Theme === */
section.gaming {
  background: #0d0d0d;
  background-image:
    linear-gradient(90deg, rgba(0,255,255,0.06) 1px, transparent 1px),
    linear-gradient(rgba(0,255,255,0.05) 1px, transparent 1px);
  background-size: 20px 20px;
  color: #e0e0e0;
  padding: 40px;
  /* KORREKTUR: Geschwindigkeit von 20s auf 5s erhöht (sollte jetzt sichtbar sein) */
  animation: gridScroll 5s linear infinite, crtGlitch 0.6s cubic-bezier(0.3, 0, 0.7, 1) both; 
}

/* NEU: Keyframes für das langsame, nahtlose Scrollen des Grids */
@keyframes gridScroll {
  from {
    background-position: 0 0;
  }
  to {
    /* Bewegt das Gitter um die Größe des Rasters (20px) für einen nahtlosen Loop */
    background-position: 20px 20px;
  }
}

section.gaming h1, section.gaming h2, section.gaming h3 {
  color: #00eaff;
  text-shadow: 0 0 10px #00eaff;
  font-family: "Press Start 2P", monospace;
  animation: textGlitchRandom 6s infinite;
}

/* === Text Glitch für Inhaltstext === */
section.gaming p, section.gaming li, section.gaming code {
  animation: textGlitchRandom 6s infinite;
  animation-delay: 1.5s; 
}

@keyframes textGlitchRandom {
  0%, 100% {
    text-shadow: 0 0 5px rgba(0,234,255,0.3);
    transform: translateX(0);
  }
  18% { text-shadow: 0 0 5px rgba(0,234,255,0.3); transform: translateX(0); }
  18.3% { text-shadow: -1px 0 rgba(255,0,255,0.4), 1px 0 rgba(0,255,0,0.4); transform: translateX(-1px) skewX(-1deg); }
  18.6% { text-shadow: 1px 0 rgba(255,0,255,0.4), -1px 0 rgba(0,255,0,0.4); transform: translateX(1px) skewX(1deg); }
  19% { text-shadow: 0 0 5px rgba(0,234,255,0.3); transform: translateX(0); }
  42% { text-shadow: 0 0 5px rgba(0,234,255,0.3); transform: translateX(0); }
  42.2% { text-shadow: -1.5px 0 rgba(255,0,255,0.5), 1.5px 0 rgba(0,255,0,0.5); transform: translateX(1.5px) skewX(1.5deg); }
  42.5% { text-shadow: 1.5px 0 rgba(255,0,255,0.5), -1.5px 0 rgba(0,255,0,0.5); transform: translateX(-1.5px) skewX(-1.5deg); }
  42.8% { text-shadow: 0 0 5px rgba(0,234,255,0.3); transform: translateX(0); }
  79% { text-shadow: 0 0 5px rgba(0,234,255,0.3); transform: translateX(0); }
  79.2% { text-shadow: -1px 0 rgba(255,0,255,0.4), 1px 0 rgba(0,255,0,0.4); transform: translateX(-1px) skewX(-1deg); }
  79.5% { text-shadow: 1px 0 rgba(255,0,255,0.4), -1px 0 rgba(0,255,0,0.4); transform: translateX(1px) skewX(1deg); }
  79.8% { text-shadow: 0 0 5px rgba(0,234,255,0.3); transform: translateX(0); }
}

/* === CRT TRANSITION === */
section {
  position: relative;
  overflow: hidden;
  animation: crtGlitch 0.6s cubic-bezier(0.3, 0, 0.7, 1) both;
  transform-style: preserve-3d;
  perspective: 1000px;
}

/* === CRT SCREEN CURVATURE (Vignette) === */
section::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(
    ellipse at center,
    transparent 0%,
    transparent 50%,
    rgba(0,0,0,0.15) 85%,
    rgba(0,0,0,0.4) 100%
  );
  z-index: 9997;
  border-radius: 3% / 2%;
}

section {
  border-radius: 3% / 2%;
  box-shadow: inset 0 0 100px rgba(0,0,0,12);
}

@keyframes crtGlitch {
  0% { opacity: 0; transform: translateY(30px) scale(0.95); filter: contrast(300%) saturate(300%) hue-rotate(20deg); }
  5% { clip-path: inset(0 0 90% 0); transform: translateX(-20px) skewX(10deg); filter: contrast(200%) hue-rotate(-15deg); }
  10% { clip-path: inset(0 0 85% 0); transform: translateX(15px) skewX(-8deg); }
  15% { clip-path: inset(70% 0 0 0); transform: translateX(-12px) scale(1.05); }
  20% { clip-path: inset(65% 0 0 0); transform: translateX(18px) skewX(5deg); }
  25% { clip-path: inset(20% 0 60% 0); transform: translateX(-15px); }
  30% { clip-path: inset(20% 0 45% 0); transform: translateX(10px) skewX(-6deg); }
  35% { clip-path: inset(50% 0 10% 0); transform: translateX(-8px); }
  40% { clip-path: inset(40% 0 10% 0); transform: translateX(12px) skewX(4deg); }
  45% { clip-path: inset(10% 0 70% 0); transform: translateX(-6px); }
  50% { clip-path: inset(0 0 0 0); transform: translateX(0) scale(1.02); }
  60% { opacity: 1; filter: contrast(150%) saturate(150%) hue-rotate(5deg); }
  70% { transform: translateX(3px); }
  80% { transform: translateX(-2px); }
  100% { opacity: 1; transform: none; filter: none; }
}

/* === STATIC SCANLINE OVERLAY === */
section.gaming { position: relative; }

section.gaming > *::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  background-image: 
    repeating-linear-gradient(
      to bottom,
      rgba(255,255,255,0.08) 0px,
      rgba(255,255,255,0.08) 2px,
      rgba(0,0,0,0.12) 2px,
      rgba(0,0,0,0.12) 4px
    );
  mix-blend-mode: overlay;
  opacity: 0.35;
  animation: crtFlicker 0.15s infinite alternate ease-in-out;
  z-index: 9999;
}

@keyframes crtFlicker {
  0%   { opacity: 0.4; filter: brightness(0.8); }
  50%  { opacity: 0.8; filter: brightness(1.2); }
  100% { opacity: 0.5; filter: brightness(0.9); }
}

/* === MOVING SCANLINE (Overlay, ::after) === */
section.gaming::after {
  content: "";
  position: fixed;
  top: -150px;
  left: 0;
  width: 100%;
  height: 150px;
  pointer-events: none;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(0,255,255,0.08) 50%, 
    transparent 100%
  );
  animation: scanlineMove 2s linear infinite; 
  mix-blend-mode: screen;
  z-index: 9999; 
}

@keyframes scanlineMove {
  from { top: -150px; }
  to { top: 100%; }
}

/* === FOOTER UNSICHTBAR (Fix für mitfahrende Nummer) === */
.marp-footer {
    position: fixed; 
    bottom: 30px;    
    right: 30px;     
    z-index: 10000;  
    
    color: #0d0d0d;  
    text-shadow: none; 
}

/* === VHS TRACKING ERROR BARS === */
section.gaming::before {
  content: "";
  position: fixed;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8) 20%, rgba(255,255,255,0.8) 80%, transparent);
  pointer-events: none;
  z-index: 9998;
  opacity: 0;
  animation: trackingError 12s infinite;
}

@keyframes trackingError {
  0%, 100% { top: -10px; opacity: 0; }
  15% { top: -10px; opacity: 0; }
  15.5% { opacity: 0.9; top: 20%; }
  16% { opacity: 0; top: 25%; }
  71% { top: -10px; opacity: 0; }
  71.3% { opacity: 0.8; top: 65%; }
  71.8% { opacity: 0; top: 70%; }
}
</style>
# 💾 E-DOSSIER INITIATIVE // **DIGITALE EXZELLENZ**
## *SYSTEM START: Transformationsstrategie des Strassenverkehrsamtes Zürich*

---

# 👾 AGENDA: DIGITALE MIGRATION

- **CORE PROTOKOLLE:** Ziele, Nutzen und Vision
- **INFRASTRUKTUR-MIGRATION:** Projektphasen und Zeitplan
- **DATEN-ASSIMILATION:** Prozessabläufe und Schnittstellen
- **SICHERHEITS-ARCHITEKTUR:** Datenschutz und Zugriffsrechte
- **RESSOURCEN-PLANUNG:** Schulung und Budget-Allokation
- **ROLLOUT-SEQUENZ**

---

# 🕹️ CORE PROTOKOLLE: ZIELE & NUTZEN

- **PAPIERLOSER VERKEHR:** Eliminierung physischer Akten für **95% weniger Archivraum**.
- **INSTANT-ZUGRIFF:** Reduzierung der Bearbeitungszeit pro Dossier von **Minuten auf Sekunden**.
- **DATEN-INTEGRITÄT:** Erhöhung der Datenqualität durch **automatisierte Validierung**.
- **EFFIZIENZSTEIGERUNG:** Freisetzung von **Mitarbeiterkapazität** für Kernaufgaben.
- **RECHTLICHE COMPLIANCE:** Einhaltung der **gesetzlichen Archivierungsvorschriften** in digitaler Form.

---

# ⚙️ DATEN-ASSIMILATION: PROZESSABLAUF

1. **DIGITALISIERUNG:** Scannen und Indizieren bestehender Papierakten (Phase 1).
2. **ERFASSUNG:** Direkteingabe neuer Dokumente über **definierte Schnittstellen** (z.B. MFK-Prüfstellen).
3. **VALIDIERUNG:** Automatische Prüfung auf **Vollständigkeit und Korrektheit** der Daten.
4. **ARCHIVIERUNG:** Sichere, revisionssichere Speicherung im **zentralen eDossier-System**.
5. **SUCHE & ZUGRIFF:** Direkter, rollenbasierter Zugriff auf alle Dokumente über **Web-Interface**.

---

# 🛡️ SICHERHEITS-ARCHITEKTUR: DATENSCHUTZ

### Kern-Sicherheitsprotokolle
- **AUTHENTIFIZIERUNG:** Multi-Faktor-Authentifizierung (MFA) für alle **internen User**.
- **ROLLEN-KONZEPT:** Granulare **Zugriffsbeschränkungen** basierend auf der Funktion.
- **VERSCHLÜSSELUNG:** Ende-zu-Ende-Verschlüsselung der **Datenbank und Übertragungswege**.
- **AUDIT-TRAIL:** Lückenlose Protokollierung aller **Zugriffe und Änderungen** am Dossier.
- **GEOLOKALISIERUNG:** Speicherung der Daten ausschliesslich in **zertifizierten Schweizer Rechenzentren**.

---

# 💻 Code Example — Zugriffslogik

```csharp
public bool CheckDossierAccess(Mitarbeiter user, Dossier dossier)
{
    // Zugriff basierend auf der Rolle des Mitarbeiters prüfen
    if (user.Rolle == "Leitung_Zulassung" && dossier.Typ == DossierTyp.Fahrzeug)
    {
        return true; // Voller Zugriff auf Fahrzeugdossiers
    }
    else if (user.Rolle == "Sachbearbeiter" && dossier.Typ == DossierTyp.Führerausweis)
    {
        return user.Abteilung == "Führerausweise"; // Nur Zugriff, wenn korrekte Abteilung
    }
    else if (user.Rolle == "Archiv")
    {
        return dossier.Status == DossierStatus.Archiviert; // Nur Leserechte auf archivierte Daten
    }
    return false; // Standardmässig verweigert
}