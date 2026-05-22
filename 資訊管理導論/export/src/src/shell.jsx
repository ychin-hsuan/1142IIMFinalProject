// App shell: sidebar nav + page container
const { useState, useEffect, useMemo, useRef } = React;

const NAV = [
  { id: "home",      label: "首頁",         en: "Home",       icon: "home" },
  { id: "dashboard", label: "畢業進度",     en: "Dashboard",  icon: "chart" },
  { id: "courses",   label: "修課明細",     en: "Courses",    icon: "list" },
  { id: "advisor",   label: "AI 選課顧問",  en: "Advisor",    icon: "sparkles" },
  { id: "simulate",  label: "模擬選課",     en: "Simulate",   icon: "flask" },
];

function Icon({ name, size = 18 }) {
  const stroke = "currentColor";
  const sw = 1.6;
  const common = { width: size, height: size, viewBox: "0 0 24 24", fill: "none", stroke, strokeWidth: sw, strokeLinecap: "round", strokeLinejoin: "round" };
  switch (name) {
    case "home":     return <svg {...common}><path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>;
    case "chart":    return <svg {...common}><path d="M4 20V8"/><path d="M10 20V4"/><path d="M16 20v-9"/><path d="M3 20h18"/></svg>;
    case "list":     return <svg {...common}><path d="M8 6h13"/><path d="M8 12h13"/><path d="M8 18h13"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/></svg>;
    case "sparkles": return <svg {...common}><path d="M12 3l1.6 4.4L18 9l-4.4 1.6L12 15l-1.6-4.4L6 9l4.4-1.6L12 3z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/></svg>;
    case "flask":    return <svg {...common}><path d="M9 3h6"/><path d="M10 3v6L5 18a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/><path d="M7 14h10"/></svg>;
    case "check":    return <svg {...common}><path d="M5 12l4 4L19 6"/></svg>;
    case "clock":    return <svg {...common}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>;
    case "alert":    return <svg {...common}><circle cx="12" cy="12" r="9"/><path d="M12 8v5"/><circle cx="12" cy="16" r="0.6" fill={stroke}/></svg>;
    case "search":   return <svg {...common}><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>;
    case "send":     return <svg {...common}><path d="M21 3L3 11l7 2 2 7 9-17z"/></svg>;
    case "plus":     return <svg {...common}><path d="M12 5v14"/><path d="M5 12h14"/></svg>;
    case "external": return <svg {...common}><path d="M14 4h6v6"/><path d="M10 14L20 4"/><path d="M20 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h5"/></svg>;
    case "notion":   return <svg {...common}><rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M8 7v10"/><path d="M8 7l8 10"/><path d="M16 7v10"/></svg>;
    case "ai":       return <svg {...common}><rect x="4" y="6" width="16" height="12" rx="3"/><circle cx="9" cy="12" r="1.2"/><circle cx="15" cy="12" r="1.2"/><path d="M12 3v3"/><path d="M9 18v2"/><path d="M15 18v2"/></svg>;
    default: return null;
  }
}

function Sidebar({ page, onNav }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-mark">GAS</div>
        <div className="brand-text">
          <div className="brand-title">畢業初審系統</div>
          <div className="brand-sub">Graduation Audit</div>
        </div>
      </div>

      <div className="sidebar-section">
        <div className="sidebar-label">NAVIGATION</div>
        <nav className="sidebar-nav">
          {NAV.map(item => (
            <button
              key={item.id}
              className={"nav-item" + (page === item.id ? " is-active" : "")}
              onClick={() => onNav(item.id)}
            >
              <Icon name={item.icon} />
              <span className="nav-label">{item.label}</span>
              <span className="nav-en">{item.en}</span>
            </button>
          ))}
        </nav>
      </div>

      <div className="sidebar-section">
        <div className="sidebar-label">SOURCES</div>
        <div className="source-row"><Icon name="notion" size={14}/> Notion API <span className="dot dot-ok"/></div>
        <div className="source-row"><Icon name="ai" size={14}/> OpenAI gpt-4o-mini <span className="dot dot-ok"/></div>
      </div>

      <div className="sidebar-foot">
        <div className="user-card">
          <div className="user-avatar">{STUDENT.avatar}</div>
          <div className="user-info">
            <div className="user-name">{STUDENT.name}</div>
            <div className="user-id">{STUDENT.id} · {STUDENT.grade}</div>
          </div>
        </div>
        <div className="foot-meta">114 入學版 · v1.0 · {STUDENT.dept}</div>
      </div>
    </aside>
  );
}

function Topbar({ page }) {
  const item = NAV.find(n => n.id === page) || NAV[0];
  const now = new Date();
  const last = `${now.getFullYear()}/${String(now.getMonth()+1).padStart(2,'0')}/${String(now.getDate()).padStart(2,'0')} 14:32`;
  return (
    <header className="topbar">
      <div className="crumbs">
        <span className="crumb-root">畢業審查</span>
        <span className="crumb-sep">/</span>
        <span className="crumb-current">{item.label}</span>
      </div>
      <div className="topbar-actions">
        <div className="sync-pill">
          <span className="dot dot-ok"/> 已同步 Notion · {last}
        </div>
        <button className="btn btn-ghost"><Icon name="search" size={14}/> 搜尋課程</button>
      </div>
    </header>
  );
}

Object.assign(window, { Sidebar, Topbar, Icon, NAV });
