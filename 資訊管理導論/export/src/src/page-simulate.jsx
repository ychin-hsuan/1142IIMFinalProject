// Simulate page
function PageSimulate() {
  const [picked, setPicked] = useState({}); // code -> true
  const [semName, setSemName] = useState("3上");

  function toggle(code) {
    setPicked(p => ({...p, [code]: !p[code]}));
  }

  const baseEarned = SUMMARY.required.earned + SUMMARY.college.earned + SUMMARY.deptElec.earned + SUMMARY.general.earned;
  const baseInProg = SUMMARY.required.inProgress + SUMMARY.college.inProgress + SUMMARY.deptElec.inProgress;
  const pickedCourses = RECOMMENDED.filter(c => picked[c.code]);
  const pickedCredits = pickedCourses.reduce((s,c)=>s+c.credits, 0);
  const projectedTotal = baseEarned + baseInProg + pickedCredits;
  const projectedPct = Math.min(100, Math.round(projectedTotal / RULES.total * 100));

  // delta to gap categories
  function bucketOf(c) {
    if (c.type === "系選修") return "deptElec";
    if (c.type === "管院共構") return "college";
    if (c.type?.startsWith("通識")) return "general";
    return "deptElec";
  }
  const deltas = { required: 0, college: 0, deptElec: 0, general: 0 };
  pickedCourses.forEach(c => { deltas[bucketOf(c)] += c.credits; });

  return (
    <div className="page page-sim">
      <div className="page-head">
        <div>
          <div className="page-eyebrow">SIMULATE · 模擬選課</div>
          <h2 className="page-title">模擬選課規劃</h2>
        </div>
        <div className="head-meta">
          <div className="meta-block"><div className="meta-l">模擬學期</div><div className="meta-v">{semName}</div></div>
          <div className="meta-block"><div className="meta-l">已加入</div><div className="meta-v">{pickedCourses.length}<span className="meta-tail"> 門</span></div></div>
          <div className="meta-block"><div className="meta-l">本期學分</div><div className="meta-v">{pickedCredits}</div></div>
        </div>
      </div>

      <div className="sim-grid">
        <section className="card card-pool">
          <div className="card-head">
            <div className="card-title">候選課程池</div>
            <div className="card-sub">點擊加入虛擬學期</div>
          </div>
          <div className="pool-list">
            {RECOMMENDED.map(c => (
              <button key={c.code} className={"pool-item " + (picked[c.code] ? "is-picked" : "")} onClick={()=>toggle(c.code)}>
                <div className="pool-left">
                  <div className="pool-name">{c.name}</div>
                  <div className="pool-meta">
                    <span className="pool-code mono">{c.code}</span>
                    <span className="pool-type">{c.type}</span>
                    <span className="pool-credit">{c.credits} 學分</span>
                  </div>
                </div>
                <div className="pool-right">
                  <div className="pool-score">推薦 {c.rec}</div>
                  <div className="pool-add">{picked[c.code] ? <Icon name="check" size={14}/> : <Icon name="plus" size={14}/>}</div>
                </div>
              </button>
            ))}
          </div>
        </section>

        <section className="card card-preview">
          <div className="card-head">
            <div className="card-title">虛擬學期 · {semName}</div>
            <div className="card-sub">{pickedCourses.length} 門 · {pickedCredits} 學分</div>
          </div>
          {pickedCourses.length === 0 && (
            <div className="empty-sem">
              <div className="empty-icon"><Icon name="flask" size={28}/></div>
              <div className="empty-h">尚未加入課程</div>
              <div className="empty-d">從左側候選池選擇課程，<br/>系統會即時計算對畢業完成度的影響。</div>
            </div>
          )}
          {pickedCourses.length > 0 && (
            <ul className="picked-list">
              {pickedCourses.map(c => (
                <li key={c.code} className="picked-item">
                  <div>
                    <div className="picked-name">{c.name}</div>
                    <div className="picked-meta mono">{c.code} · {c.type} · {c.credits} 學分</div>
                  </div>
                  <button className="rm-btn" onClick={()=>toggle(c.code)}>移除</button>
                </li>
              ))}
            </ul>
          )}

          <div className="impact">
            <div className="impact-head">完成度預估</div>
            <div className="impact-row">
              <div className="impact-now">
                <div className="impact-l">目前</div>
                <div className="impact-v">{Math.round(baseEarned/RULES.total*100)}%</div>
                <div className="impact-d mono">{baseEarned} / {RULES.total}</div>
              </div>
              <div className="impact-arrow">→</div>
              <div className="impact-next">
                <div className="impact-l">{semName} 結束後</div>
                <div className="impact-v" style={{color:"var(--accent)"}}>{projectedPct}%</div>
                <div className="impact-d mono">{projectedTotal} / {RULES.total}</div>
              </div>
            </div>
            <div className="delta-grid">
              <Delta label="系訂必修" base={SUMMARY.required.earned} delta={deltas.required+SUMMARY.required.inProgress} req={RULES.required}/>
              <Delta label="管院共構" base={SUMMARY.college.earned} delta={deltas.college+SUMMARY.college.inProgress} req={RULES.collegeCommon}/>
              <Delta label="系選修（本系）" base={SUMMARY.deptElec.earned} delta={deltas.deptElec+SUMMARY.deptElec.inProgress} req={RULES.deptElective}/>
              <Delta label="通識" base={SUMMARY.general.earned} delta={deltas.general} req={RULES.generalEdu}/>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

function Delta({label, base, delta, req}) {
  const total = base + delta;
  const pct = Math.min(100, Math.round(total/req*100));
  return (
    <div className="delta-cell">
      <div className="delta-l">{label}</div>
      <div className="delta-bar">
        <div className="delta-fill" style={{width: Math.min(100, base/req*100)+"%"}}/>
        {delta > 0 && <div className="delta-add" style={{width: Math.min(100-base/req*100, delta/req*100)+"%"}}/>}
      </div>
      <div className="delta-num mono">
        {base}{delta>0 && <span className="delta-plus"> +{delta}</span>} / {req}
      </div>
    </div>
  );
}

Object.assign(window, { PageSimulate, Delta });
