// Home page
function PageHome({ onNav }) {
  const totalEarned = SUMMARY.required.earned + SUMMARY.college.earned + SUMMARY.deptElec.earned + SUMMARY.general.earned;
  const totalInProgress = SUMMARY.required.inProgress + SUMMARY.college.inProgress + SUMMARY.deptElec.inProgress;
  const pct = Math.round((totalEarned / RULES.total) * 100);
  const semester = "114-2";

  return (
    <div className="page page-home">
      <div className="hello-block">
        <div className="hello-eyebrow">114-2 學期 · 畢業審查總覽</div>
        <h1 className="hello-title">嗨，{STUDENT.name}。<span className="hello-faint">距離畢業還差 <b>{RULES.total - totalEarned}</b> 學分。</span></h1>
        <div className="hello-sub">系統已自動從你的 Notion 修課資料庫讀取 {[...REQUIRED_COURSES,...COLLEGE_COMMON,...DEPT_ELECTIVES,...GENERAL_EDU].filter(c=>c.status!=="pending").length} 門課程紀錄，並依「114 入學版」資管系畢業規則完成比對。</div>
      </div>

      <div className="home-grid">
        <section className="card card-hero">
          <div className="hero-row">
            <div className="hero-progress">
              <ProgressRing value={pct} size={148} stroke={12} />
              <div className="hero-progress-meta">
                <div className="metric-big">{totalEarned}<span className="metric-tail">/ {RULES.total}</span></div>
                <div className="metric-label">已修畢學分數</div>
                <div className="metric-extra">在修 +{totalInProgress} · 待修 {RULES.total - totalEarned - totalInProgress}</div>
              </div>
            </div>
            <div className="hero-bars">
              <MiniBar label="系訂必修" earned={SUMMARY.required.earned} req={RULES.required} tone="accent"/>
              <MiniBar label="管院共構" earned={SUMMARY.college.earned} req={RULES.collegeCommon} tone="good"/>
              <MiniBar label="系選修（本系）" earned={SUMMARY.deptElec.earned} req={RULES.deptElective} tone="warn"/>
              <MiniBar label="通識" earned={SUMMARY.general.earned} req={RULES.generalEdu} tone="ink"/>
            </div>
          </div>
          <div className="hero-cta">
            <button className="btn btn-primary" onClick={()=>onNav("dashboard")}>查看完整儀表板 →</button>
            <button className="btn btn-ghost" onClick={()=>onNav("advisor")}><Icon name="sparkles" size={14}/> 問 AI 顧問</button>
          </div>
        </section>

        <section className="card card-stat">
          <div className="stat-eyebrow">學期</div>
          <div className="stat-value">{semester}</div>
          <div className="stat-row">
            <div className="stat-cell"><div className="stat-cell-n">5</div><div className="stat-cell-l">在修課程</div></div>
            <div className="stat-cell"><div className="stat-cell-n">14</div><div className="stat-cell-l">已修課程</div></div>
          </div>
          <div className="stat-foot">下次同步：自動 · 每 30 分鐘</div>
        </section>

        <section className="card card-action" onClick={()=>onNav("dashboard")}>
          <div className="action-icon"><Icon name="chart"/></div>
          <div className="action-title">畢業進度儀表板</div>
          <div className="action-desc">五大門檻學分達成率、課程分類占比，一目了然。</div>
          <div className="action-link">前往 →</div>
        </section>
        <section className="card card-action" onClick={()=>onNav("courses")}>
          <div className="action-icon"><Icon name="list"/></div>
          <div className="action-title">修課明細查詢</div>
          <div className="action-desc">查看系必修、共構、系選修與通識的完整課程清單與成績。</div>
          <div className="action-link">前往 →</div>
        </section>
        <section className="card card-action" onClick={()=>onNav("advisor")}>
          <div className="action-icon"><Icon name="sparkles"/></div>
          <div className="action-title">AI 選課顧問</div>
          <div className="action-desc">依缺修狀況智慧推薦，可用自然語言追問。</div>
          <div className="action-link">前往 →</div>
        </section>
        <section className="card card-action" onClick={()=>onNav("simulate")}>
          <div className="action-icon"><Icon name="flask"/></div>
          <div className="action-title">模擬選課規劃</div>
          <div className="action-desc">把候選課加入虛擬學期，預覽畢業完成度變化。</div>
          <div className="action-link">前往 →</div>
        </section>

        <section className="card card-news">
          <div className="news-head">
            <div className="news-title">系統提醒</div>
            <div className="news-tag">3 則</div>
          </div>
          <ul className="news-list">
            <li>
              <span className="news-dot dot-warn"/>
              <div>
                <div className="news-h">系選修（本系）尚缺 <b>24 學分</b></div>
                <div className="news-d">建議大三上修 4 門以維持進度</div>
              </div>
            </li>
            <li>
              <span className="news-dot dot-ok"/>
              <div>
                <div className="news-h">必修進度超前</div>
                <div className="news-d">已完成 36/48 · 達成 75%</div>
              </div>
            </li>
            <li>
              <span className="news-dot dot-accent"/>
              <div>
                <div className="news-h">通識「核心」領域待加強</div>
                <div className="news-d">建議下學期補修一門核心領域課程</div>
              </div>
            </li>
          </ul>
        </section>
      </div>
    </div>
  );
}

function ProgressRing({ value, size = 120, stroke = 10 }) {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const off = c - (value / 100) * c;
  return (
    <svg width={size} height={size} className="ring">
      <circle cx={size/2} cy={size/2} r={r} stroke="var(--rule)" strokeWidth={stroke} fill="none"/>
      <circle cx={size/2} cy={size/2} r={r} stroke="var(--accent)" strokeWidth={stroke} fill="none"
              strokeDasharray={c} strokeDashoffset={off} strokeLinecap="round"
              transform={`rotate(-90 ${size/2} ${size/2})`}/>
      <text x="50%" y="50%" textAnchor="middle" dy=".35em" className="ring-text">{value}%</text>
    </svg>
  );
}

function MiniBar({ label, earned, req, tone="accent" }) {
  const pct = Math.min(100, Math.round((earned/req)*100));
  return (
    <div className="minibar">
      <div className="minibar-head">
        <span className="minibar-label">{label}</span>
        <span className={"minibar-val tone-"+tone}>{earned}<span className="minibar-req"> / {req}</span></span>
      </div>
      <div className="minibar-track"><div className={"minibar-fill tone-"+tone} style={{width: pct+"%"}}/></div>
    </div>
  );
}

Object.assign(window, { PageHome, ProgressRing, MiniBar });
