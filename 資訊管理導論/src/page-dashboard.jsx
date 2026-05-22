// Dashboard page
function PageDashboard() {
  const totalEarned = SUMMARY.required.earned + SUMMARY.college.earned + SUMMARY.deptElec.earned + SUMMARY.general.earned;
  const pct = Math.round((totalEarned / RULES.total) * 100);

  const cats = [
    { label: "系訂必修",     earned: SUMMARY.required.earned, req: RULES.required, color: "var(--accent)",        target: "畢業必要" },
    { label: "管院共構",     earned: SUMMARY.college.earned,  req: RULES.collegeCommon, color: "var(--good)",     target: "4 門 12 學分" },
    { label: "系選修（本系）", earned: SUMMARY.deptElec.earned, req: RULES.deptElective, color: "var(--warn)",     target: "至少 30 學分" },
    { label: "通識課程",     earned: SUMMARY.general.earned, req: RULES.generalEdu,    color: "#5a6680",          target: "18 學分" },
  ];

  // 通識分類資料
  const geCats = ["全人","英文","核心","多元","體育"].map(cat => {
    const list = GENERAL_EDU.filter(c => c.category === cat);
    const earned = list.filter(c=>c.status==="passed").reduce((s,c)=>s+(c.credits||0),0);
    const targets = { 全人:1, 英文:6, 核心:9, 多元:9, 體育:0 };
    return { cat, earned, target: targets[cat], count: list.length };
  });

  // 各學期學分
  const semData = [
    { sem: "1上", credits: 16 },
    { sem: "1下", credits: 17 },
    { sem: "2上", credits: 18 },
    { sem: "2下", credits: 15 },
    { sem: "3上", credits: 0, projected: true },
    { sem: "3下", credits: 0, projected: true },
  ];
  const maxSem = 20;

  return (
    <div className="page page-dashboard">
      <div className="page-head">
        <div>
          <div className="page-eyebrow">DASHBOARD · 114 入學版規則</div>
          <h2 className="page-title">畢業進度儀表板</h2>
        </div>
        <div className="head-meta">
          <div className="meta-block">
            <div className="meta-l">完成度</div>
            <div className="meta-v">{pct}%</div>
          </div>
          <div className="meta-block">
            <div className="meta-l">剩餘</div>
            <div className="meta-v">{RULES.total - totalEarned}</div>
          </div>
          <div className="meta-block">
            <div className="meta-l">預計畢業</div>
            <div className="meta-v">2028.06</div>
          </div>
        </div>
      </div>

      <div className="dash-grid">
        {cats.map((c,i) => (
          <ThresholdCard key={i} {...c}/>
        ))}
      </div>

      <div className="split-grid">
        <section className="card card-chart">
          <div className="card-head">
            <div className="card-title">每學期學分分布</div>
            <div className="card-sub">含必修、共構、選修、通識</div>
          </div>
          <div className="bars">
            {semData.map((s,i) => {
              const h = s.credits ? (s.credits / maxSem) * 100 : 0;
              return (
                <div className="bar-col" key={i}>
                  <div className="bar-track">
                    <div className={"bar-fill" + (s.projected ? " bar-projected" : "")} style={{height: (s.projected? 8 : h)+"%"}}>
                      {!s.projected && <span className="bar-num">{s.credits}</span>}
                    </div>
                  </div>
                  <div className="bar-label">{s.sem}{s.projected && <span className="bar-tag">預估</span>}</div>
                </div>
              );
            })}
            <div className="bar-rules">
              {[0,5,10,15,20].map(v => (
                <div className="rule" key={v} style={{bottom: (v/maxSem*100)+"%"}}>
                  <span className="rule-num">{v}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="card card-pie">
          <div className="card-head">
            <div className="card-title">課程類別占比</div>
            <div className="card-sub">已修 {totalEarned} 學分</div>
          </div>
          <div className="pie-wrap">
            <DonutChart segments={cats.map(c=>({label:c.label, value:c.earned, color:c.color}))}/>
            <div className="legend">
              {cats.map((c,i) => (
                <div className="legend-item" key={i}>
                  <span className="swatch" style={{background:c.color}}/>
                  <span className="legend-label">{c.label}</span>
                  <span className="legend-val">{c.earned}</span>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>

      <section className="card card-ge">
        <div className="card-head">
          <div className="card-title">通識課程分類達成</div>
          <div className="card-sub">全人 / 英文 / 核心 / 多元 / 體育</div>
        </div>
        <div className="ge-grid">
          {geCats.map((g,i) => {
            const pct = g.target ? Math.min(100, Math.round(g.earned/g.target*100)) : (g.count>0?100:0);
            return (
              <div className="ge-cell" key={i}>
                <div className="ge-cat">{g.cat}</div>
                <div className="ge-bar"><div className="ge-fill" style={{width: pct+"%"}}/></div>
                <div className="ge-meta">
                  <span className="ge-num">{g.earned}{g.target?` / ${g.target}`:""}</span>
                  <span className="ge-cnt">{g.count} 門</span>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <section className="card card-rules">
        <div className="card-head">
          <div className="card-title">畢業規則檢核</div>
          <div className="card-sub">依 114 入學版自動判斷</div>
        </div>
        <ul className="rule-list">
          <Rule pass={SUMMARY.required.earned >= RULES.required} title="系訂必修 48 學分" detail={`已修 ${SUMMARY.required.earned} 學分 (含在修 ${SUMMARY.required.inProgress})`}/>
          <Rule pass={SUMMARY.college.earned >= RULES.collegeCommon} title="管院共構 12 學分" detail={`已修 ${SUMMARY.college.earned} 學分 · 4 門（統計／會計／經濟學一二）`}/>
          <Rule pass={SUMMARY.deptElec.earned >= RULES.deptElective} title="系選修（本系） 至少 30 學分" detail={`已修 ${SUMMARY.deptElec.earned} 學分 · 尚缺 ${Math.max(0,RULES.deptElective-SUMMARY.deptElec.earned)}`}/>
          <Rule pass={SUMMARY.general.earned >= RULES.generalEdu} title="通識 18 學分" detail={`已修 ${SUMMARY.general.earned} 學分 · 含 5 大領域`}/>
          <Rule pass={totalEarned >= RULES.total} title={`畢業總學分 ${RULES.total}`} detail={`目前 ${totalEarned} 學分 · 完成度 ${pct}%`}/>
        </ul>
      </section>
    </div>
  );
}

function ThresholdCard({label, earned, req, color, target}) {
  const pct = Math.min(100, Math.round((earned/req)*100));
  return (
    <div className="th-card">
      <div className="th-row">
        <div className="th-label">{label}</div>
        <div className="th-pct" style={{color}}>{pct}%</div>
      </div>
      <div className="th-num"><b>{earned}</b> <span className="th-req">/ {req}</span></div>
      <div className="th-track"><div className="th-fill" style={{width: pct+"%", background: color}}/></div>
      <div className="th-target">{target}</div>
    </div>
  );
}

function DonutChart({segments}) {
  const total = segments.reduce((s,x)=>s+x.value,0);
  const r = 70, cx = 90, cy = 90, stroke = 22;
  let acc = 0;
  const c = 2 * Math.PI * r;
  return (
    <svg width={180} height={180} className="donut">
      <circle cx={cx} cy={cy} r={r} stroke="var(--rule)" strokeWidth={stroke} fill="none"/>
      {segments.map((s,i) => {
        const len = (s.value/total) * c;
        const off = c - len;
        const rot = (acc/total) * 360 - 90;
        acc += s.value;
        return (
          <circle key={i} cx={cx} cy={cy} r={r} stroke={s.color} strokeWidth={stroke} fill="none"
                  strokeDasharray={`${len} ${c-len}`}
                  strokeDashoffset={0}
                  transform={`rotate(${rot} ${cx} ${cy})`}/>
        );
      })}
      <text x={cx} y={cy-4} textAnchor="middle" className="donut-num">{total}</text>
      <text x={cx} y={cy+16} textAnchor="middle" className="donut-l">學分</text>
    </svg>
  );
}

function Rule({pass, title, detail}) {
  return (
    <li className={"rule-item " + (pass?"is-pass":"is-todo")}>
      <span className="rule-mark">
        {pass ? <Icon name="check" size={14}/> : <Icon name="clock" size={14}/>}
      </span>
      <div className="rule-body">
        <div className="rule-title">{title}</div>
        <div className="rule-detail">{detail}</div>
      </div>
      <div className="rule-status">{pass ? "已達標" : "進行中"}</div>
    </li>
  );
}

Object.assign(window, { PageDashboard, ThresholdCard, DonutChart, Rule });
