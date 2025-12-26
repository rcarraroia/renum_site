# 🎨 DESIGN SYSTEM RENUM

> **Configuração visual completa extraída do projeto RENUM para replicação no Builder (Dyad)**

---

## 📋 RESUMO EXECUTIVO

**Baseado em:** Shadcn/ui + Tailwind CSS  
**Tema:** Default (Slate)  
**Dark Mode:** Suportado via CSS Variables  
**Componentes:** 50+ componentes Shadcn instalados  
**Fonte:** Sistema (sem fonte customizada)  
**Breakpoints:** Padrão Tailwind + container customizado  

---

## 🎨 PALET
## 🎨 Paleta de Cores

### Cores Primárias
```css
:root {
  /* Azul Principal - Confiança e Tecnologia */
  --primary-50: #eff6ff;
  --primary-100: #dbeafe;
  --primary-200: #bfdbfe;
  --primary-300: #93c5fd;
  --primary-400: #60a5fa;
  --primary-500: #3b82f6;  /* Cor principal */
  --primary-600: #2563eb;
  --primary-700: #1d4ed8;
  --primary-800: #1e40af;
  --primary-900: #1e3a8a;
  --primary-950: #172554;
}
```

### Cores Secundárias
```css
:root {
  /* Verde - Sucesso e Crescimento */
  --success-50: #f0fdf4;
  --success-100: #dcfce7;
  --success-200: #bbf7d0;
  --success-300: #86efac;
  --success-400: #4ade80;
  --success-500: #22c55e;  /* Verde principal */
  --success-600: #16a34a;
  --success-700: #15803d;
  --success-800: #166534;
  --success-900: #14532d;

  /* Laranja - Energia e Inovação */
  --warning-50: #fff7ed;
  --warning-100: #ffedd5;
  --warning-200: #fed7aa;
  --warning-300: #fdba74;
  --warning-400: #fb923c;
  --warning-500: #f97316;  /* Laranja principal */
  --warning-600: #ea580c;
  --warning-700: #c2410c;
  --warning-800: #9a3412;
  --warning-900: #7c2d12;
}
```

### Cores de Sistema
```css
:root {
  /* Vermelho - Erro e Atenção */
  --error-50: #fef2f2;
  --error-100: #fee2e2;
  --error-200: #fecaca;
  --error-300: #fca5a5;
  --error-400: #f87171;
  --error-500: #ef4444;
  --error-600: #dc2626;
  --error-700: #b91c1c;
  --error-800: #991b1b;
  --error-900: #7f1d1d;

  /* Cinza - Neutros */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  --gray-950: #030712;
}
```

### Aplicação das Cores

**Backgrounds:**
- Fundo principal: `--gray-50`
- Cards/Modais: `white`
- Sidebar: `--gray-900`
- Header: `white` com sombra

**Textos:**
- Título principal: `--gray-900`
- Texto secundário: `--gray-600`
- Texto desabilitado: `--gray-400`
- Texto em fundo escuro: `white`

**Estados:**
- Hover: Escurecer 1 tom
- Active: Escurecer 2 tons
- Disabled: `--gray-300`
- Focus: Ring `--primary-500`

---

## 📝 Tipografia

### Família de Fontes
```css
:root {
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
}
```

### Escala Tipográfica
```css
:root {
  /* Tamanhos */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */
  --text-5xl: 3rem;      /* 48px */

  /* Pesos */
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Altura de linha */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
}
```

### Hierarquia de Títulos
```css
.h1 {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  color: var(--gray-900);
}

.h2 {
  font-size: var(--text-3xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
  color: var(--gray-900);
}

.h3 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-normal);
  color: var(--gray-800);
}

.h4 {
  font-size: var(--text-xl);
  font-weight: var(--font-medium);
  line-height: var(--leading-normal);
  color: var(--gray-800);
}

.body-large {
  font-size: var(--text-lg);
  font-weight: var(--font-normal);
  line-height: var(--leading-relaxed);
  color: var(--gray-700);
}

.body {
  font-size: var(--text-base);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
  color: var(--gray-700);
}

.body-small {
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
  color: var(--gray-600);
}

.caption {
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  line-height: var(--leading-normal);
  color: var(--gray-500);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

---

## 🔲 Componentes Base

### Botões

#### Variantes
```css
/* Botão Primário */
.btn-primary {
  background-color: var(--primary-600);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: var(--font-medium);
  font-size: var(--text-sm);
  transition: all 0.2s ease;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: var(--primary-700);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-primary:active {
  background-color: var(--primary-800);
  transform: translateY(0);
}

.btn-primary:disabled {
  background-color: var(--gray-300);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Botão Secundário */
.btn-secondary {
  background-color: white;
  color: var(--primary-600);
  border: 1px solid var(--primary-600);
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: var(--font-medium);
  font-size: var(--text-sm);
  transition: all 0.2s ease;
  cursor: pointer;
}

.btn-secondary:hover {
  background-color: var(--primary-50);
  border-color: var(--primary-700);
  color: var(--primary-700);
}

/* Botão Ghost */
.btn-ghost {
  background-color: transparent;
  color: var(--gray-600);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: var(--font-medium);
  font-size: var(--text-sm);
  transition: all 0.2s ease;
  cursor: pointer;
}

.btn-ghost:hover {
  background-color: var(--gray-100);
  color: var(--gray-900);
}

/* Botão de Perigo */
.btn-danger {
  background-color: var(--error-600);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: var(--font-medium);
  font-size: var(--text-sm);
  transition: all 0.2s ease;
  cursor: pointer;
}

.btn-danger:hover {
  background-color: var(--error-700);
}
```

#### Tamanhos
```css
.btn-xs {
  padding: 0.25rem 0.75rem;
  font-size: var(--text-xs);
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: var(--text-sm);
}

.btn-md {
  padding: 0.75rem 1.5rem;
  font-size: var(--text-sm);
}

.btn-lg {
  padding: 1rem 2rem;
  font-size: var(--text-base);
}

.btn-xl {
  padding: 1.25rem 2.5rem;
  font-size: var(--text-lg);
}
```

### Inputs

#### Input Base
```css
.input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--gray-300);
  border-radius: 0.5rem;
  font-size: var(--text-sm);
  background-color: white;
  transition: all 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input:disabled {
  background-color: var(--gray-50);
  color: var(--gray-500);
  cursor: not-allowed;
}

.input.error {
  border-color: var(--error-500);
}

.input.error:focus {
  border-color: var(--error-500);
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}
```

#### Select
```css
.select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--gray-300);
  border-radius: 0.5rem;
  font-size: var(--text-sm);
  background-color: white;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
  appearance: none;
  cursor: pointer;
}
```

#### Textarea
```css
.textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--gray-300);
  border-radius: 0.5rem;
  font-size: var(--text-sm);
  background-color: white;
  resize: vertical;
  min-height: 6rem;
  font-family: var(--font-sans);
}
```

### Cards

#### Card Base
```css
.card {
  background-color: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--gray-200);
  overflow: hidden;
  transition: all 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--gray-200);
}

.card-body {
  padding: 1.5rem;
}

.card-footer {
  padding: 1rem 1.5rem;
  background-color: var(--gray-50);
  border-top: 1px solid var(--gray-200);
}
```

#### Card de Estatística
```css
.stat-card {
  background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
  color: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transform: translate(30px, -30px);
}

.stat-value {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: var(--text-sm);
  opacity: 0.9;
}

.stat-change {
  font-size: var(--text-xs);
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat-change.positive {
  color: var(--success-200);
}

.stat-change.negative {
  color: var(--error-200);
}
```

### Modais

```css
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.modal {
  background-color: white;
  border-radius: 0.75rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  animation: slideIn 0.3s ease;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--gray-200);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--gray-900);
}

.modal-close {
  background: none;
  border: none;
  color: var(--gray-400);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.25rem;
}

.modal-close:hover {
  color: var(--gray-600);
  background-color: var(--gray-100);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
}

.modal-footer {
  padding: 1rem 1.5rem;
  background-color: var(--gray-50);
  border-top: 1px solid var(--gray-200);
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
```

### Badges e Tags

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-primary {
  background-color: var(--primary-100);
  color: var(--primary-800);
}

.badge-success {
  background-color: var(--success-100);
  color: var(--success-800);
}

.badge-warning {
  background-color: var(--warning-100);
  color: var(--warning-800);
}

.badge-error {
  background-color: var(--error-100);
  color: var(--error-800);
}

.badge-gray {
  background-color: var(--gray-100);
  color: var(--gray-800);
}

/* Status específicos */
.status-active {
  background-color: var(--success-100);
  color: var(--success-800);
}

.status-inactive {
  background-color: var(--gray-100);
  color: var(--gray-600);
}

.status-pending {
  background-color: var(--warning-100);
  color: var(--warning-800);
}

.status-blocked {
  background-color: var(--error-100);
  color: var(--error-800);
}
```

---

## 📐 Espaçamento e Layout

### Sistema de Espaçamento
```css
:root {
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */
}
```

### Grid System
```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.grid {
  display: grid;
  gap: var(--space-6);
}

.grid-cols-1 { grid-template-columns: repeat(1, 1fr); }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
.grid-cols-12 { grid-template-columns: repeat(12, 1fr); }

.col-span-1 { grid-column: span 1; }
.col-span-2 { grid-column: span 2; }
.col-span-3 { grid-column: span 3; }
.col-span-4 { grid-column: span 4; }
.col-span-6 { grid-column: span 6; }
.col-span-12 { grid-column: span 12; }

/* Responsivo */
@media (max-width: 768px) {
  .grid-cols-2,
  .grid-cols-3,
  .grid-cols-4 {
    grid-template-columns: 1fr;
  }
}
```

### Flexbox Utilities
```css
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-row { flex-direction: row; }

.items-start { align-items: flex-start; }
.items-center { align-items: center; }
.items-end { align-items: flex-end; }
.items-stretch { align-items: stretch; }

.justify-start { justify-content: flex-start; }
.justify-center { justify-content: center; }
.justify-end { justify-content: flex-end; }
.justify-between { justify-content: space-between; }
.justify-around { justify-content: space-around; }

.gap-1 { gap: var(--space-1); }
.gap-2 { gap: var(--space-2); }
.gap-3 { gap: var(--space-3); }
.gap-4 { gap: var(--space-4); }
.gap-6 { gap: var(--space-6); }
.gap-8 { gap: var(--space-8); }
```

---

## 🎭 Estados e Animações

### Estados de Loading
```css
.loading {
  position: relative;
  overflow: hidden;
}

.loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.6),
    transparent
  );
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

.skeleton {
  background-color: var(--gray-200);
  border-radius: 0.25rem;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

### Transições
```css
.transition-all {
  transition: all 0.2s ease;
}

.transition-colors {
  transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
}

.transition-transform {
  transition: transform 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.hover-scale:hover {
  transform: scale(1.05);
}
```

### Estados de Foco
```css
.focus-ring:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  border-color: var(--primary-500);
}

.focus-visible:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
```

---

## 📱 Responsividade

### Breakpoints
```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* Mobile First */
@media (min-width: 640px) {
  .sm\:block { display: block; }
  .sm\:hidden { display: none; }
  .sm\:grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 768px) {
  .md\:block { display: block; }
  .md\:hidden { display: none; }
  .md\:grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
  .md\:flex-row { flex-direction: row; }
}

@media (min-width: 1024px) {
  .lg\:block { display: block; }
  .lg\:hidden { display: none; }
  .lg\:grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
}
```

### Layout Responsivo
```css
.responsive-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

@media (min-width: 640px) {
  .responsive-container {
    padding: 0 var(--space-6);
  }
}

@media (min-width: 1024px) {
  .responsive-container {
    padding: 0 var(--space-8);
  }
}

/* Sidebar responsiva */
.sidebar {
  width: 280px;
  transition: transform 0.3s ease;
}

@media (max-width: 1024px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    z-index: 50;
    transform: translateX(-100%);
  }
  
  .sidebar.open {
    transform: translateX(0);
  }
}
```

---

## 🔧 Utilitários

### Visibilidade
```css
.hidden { display: none; }
.visible { visibility: visible; }
.invisible { visibility: hidden; }

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### Posicionamento
```css
.relative { position: relative; }
.absolute { position: absolute; }
.fixed { position: fixed; }
.sticky { position: sticky; }

.top-0 { top: 0; }
.right-0 { right: 0; }
.bottom-0 { bottom: 0; }
.left-0 { left: 0; }

.z-10 { z-index: 10; }
.z-20 { z-index: 20; }
.z-30 { z-index: 30; }
.z-40 { z-index: 40; }
.z-50 { z-index: 50; }
```

### Overflow
```css
.overflow-hidden { overflow: hidden; }
.overflow-auto { overflow: auto; }
.overflow-scroll { overflow: scroll; }
.overflow-x-auto { overflow-x: auto; }
.overflow-y-auto { overflow-y: auto; }
```

### Texto
```css
.text-left { text-align: left; }
.text-center { text-align: center; }
.text-right { text-align: right; }

.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

---

## 🎨 Temas e Customização

### Tema Escuro (Futuro)
```css
[data-theme="dark"] {
  --gray-50: #1f2937;
  --gray-100: #374151;
  --gray-200: #4b5563;
  --gray-300: #6b7280;
  --gray-400: #9ca3af;
  --gray-500: #d1d5db;
  --gray-600: #e5e7eb;
  --gray-700: #f3f4f6;
  --gray-800: #f9fafb;
  --gray-900: #ffffff;
}

[data-theme="dark"] .card {
  background-color: var(--gray-100);
  border-color: var(--gray-200);
}

[data-theme="dark"] .input {
  background-color: var(--gray-100);
  border-color: var(--gray-200);
  color: var(--gray-900);
}
```

### Customização por Cliente
```css
/* Variáveis customizáveis */
:root {
  --brand-primary: var(--primary-600);
  --brand-secondary: var(--success-600);
  --brand-accent: var(--warning-600);
  
  --brand-font-primary: var(--font-sans);
  --brand-font-secondary: var(--font-mono);
  
  --brand-radius: 0.5rem;
  --brand-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Aplicação das variáveis de marca */
.btn-brand {
  background-color: var(--brand-primary);
  border-radius: var(--brand-radius);
}

.card-brand {
  border-radius: var(--brand-radius);
  box-shadow: var(--brand-shadow);
}
```

---

## 📋 Checklist de Implementação

### Fase 1 - Fundação
- [ ] Configurar variáveis CSS customizadas
- [ ] Implementar reset/normalize CSS
- [ ] Definir tipografia base
- [ ] Configurar paleta de cores
- [ ] Implementar sistema de espaçamento

### Fase 2 - Componentes Base
- [ ] Botões (todas as variantes)
- [ ] Inputs e formulários
- [ ] Cards básicos
- [ ] Modais
- [ ] Badges e tags

### Fase 3 - Layout
- [ ] Grid system
- [ ] Flexbox utilities
- [ ] Responsividade
- [ ] Sidebar e navegação
- [ ] Header e footer

### Fase 4 - Estados e Interações
- [ ] Estados de loading
- [ ] Animações e transições
- [ ] Estados de foco
- [ ] Feedback visual
- [ ] Microinterações

### Fase 5 - Componentes Avançados
- [ ] Tabelas de dados
- [ ] Gráficos e dashboards
- [ ] Chat interface
- [ ] Formulários complexos
- [ ] Componentes específicos do RENUM

---

## 🔍 Validação e Testes

### Checklist de Qualidade
- [ ] Contraste de cores (WCAG AA)
- [ ] Navegação por teclado
- [ ] Screen readers
- [ ] Performance (Core Web Vitals)
- [ ] Responsividade em todos os breakpoints
- [ ] Consistência visual
- [ ] Estados de erro e loading
- [ ] Feedback de interações

### Ferramentas de Teste
- **Acessibilidade:** axe-core, WAVE
- **Performance:** Lighthouse, WebPageTest
- **Visual:** Percy, Chromatic
- **Cross-browser:** BrowserStack

---

## 📚 Recursos e Referências

### Inspirações
- **Tailwind CSS:** Sistema de utilitários
- **Material Design:** Princípios de design
- **Ant Design:** Componentes empresariais
- **Chakra UI:** API de componentes
- **Radix UI:** Primitivos acessíveis

### Ferramentas
- **Figma:** Design e prototipagem
- **Storybook:** Documentação de componentes
- **CSS Custom Properties:** Variáveis nativas
- **PostCSS:** Processamento CSS
- **Autoprefixer:** Compatibilidade de browsers

---

**Versão:** 1.0  
**Última atualização:** 26/12/2025  
**Responsável:** Equipe RENUM  
**Status:** Em desenvolvimento

---

## 📝 Notas de Implementação

Este Design System deve ser implementado gradualmente, começando pelos componentes mais básicos e evoluindo para os mais complexos. Cada componente deve ser testado individualmente antes da integração no sistema principal.

A consistência visual é fundamental para a experiência do usuário, portanto, todos os desenvolvedores devem seguir rigorosamente estas diretrizes.

Para dúvidas ou sugestões de melhorias, consulte a equipe de design ou abra uma issue no repositório do projeto.