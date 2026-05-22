// Course Records page
function PageCourses() {
  const [tab, setTab] = useState("required");
  const [q, setQ] = useState("");
  const [filter, setFilter] = useState("all"); // all / passed / in-progress / pending

  const groups = {
    required: { title: "系訂必修", req: RULES.required, data: REQUIRED_COURSES, hint: "17 門 · 48 學分" },
    college:  { title: "管院共構", req: RULES.collegeCommon, data: COLLEGE_COMMON, hint: "4 門 · 12 學分" },
    elective: { title: "系選修（本系）", req: RULES.deptElective, data: DEPT_ELECTIVES, hint: "至少 30 學分" },
    general:  { title: "通識課程", req: RULES.generalEdu, data: GENERAL_EDU, hint: "全人 / 英文 / 核心 / 多元 / 體育" },
  };

  const data = groups[tab].data
    .filter(c => filter === "all" || c.status === filter)
    .filter(c => !q || (c.name+c.code).toLowerCase().includes(q.toLowerCase()));

  const earned = sumCredits(groups[tab].data);
  const inProg = groups[tab].data.filter(c=>c.status==="in-progress").reduce((s,c)=>s+c.credits,0);

  return (
    <div className="page page-courses">
      <div className="page-head">
        <div>
          <div className="page-eyebrow">COURSES · 修課紀錄</div>
          <h2 className="page-title">修課明細查詢</h2>
        </div>
        <div className="head-meta">
          <div className="meta-block"><div className="meta-l">本類已修</div><div className="meta-v">{earned}<span className="meta-tail">/ {groups[tab].req}</span></div></div>
          <div className="meta-block"><div className="meta-l">在修</div><div className="meta-v">{inProg}</div></div>
        </div>
      </div>

      <div className="tab-row">
        {Object.entries(groups).map(([k,g]) => (
          <button key={k} className={"tab "+(tab===k?"is-active":"")} onClick={()=>setTab(k)}>
            <span className="tab-title">{g.title}</span>
            <span className="tab-hint">{g.hint}</span>
          </button>
        ))}
      </div>

      <div className="toolbar">
        <div className="search">
          <Icon name="search" size={14}/>
          <input placeholder="搜尋課程代碼或名稱…" value={q} onChange={e=>setQ(e.target.value)}/>
        </div>
        <div className="chips">
          {["all","passed","in-progress","pending"].map(f => (
            <button key={f} className={"chip "+(filter===f?"is-active":"")} onClick={()=>setFilter(f)}>
              {{all:"全部",passed:"已修",["in-progress"]:"在修",pending:"待修"}[f]}
            </button>
          ))}
        </div>
      </div>

      <div className="table-card">
        <div className="trow trow-head">
          <div className="tc tc-code">代碼</div>
          <div className="tc tc-name">課程名稱</div>
          <div className="tc tc-cred">學分</div>
          <div className="tc tc-sem">學期</div>
          <div className="tc tc-grade">成績</div>
          <div className="tc tc-status">狀態</div>
        </div>
        {data.length === 0 && <div className="trow-empty">沒有符合條件的課程</div>}
        {data.map((c,i) => <CourseRow key={c.code} c={c} tab={tab}/>)}
      </div>

      <div className="hint-row mono">
        Source: Notion Database · 個人修課紀錄 · 自動 Rollup 學分欄位
      </div>
    </div>
  );
}

function CourseRow({c, tab}) {
  const statusMap = {
    passed: { label: "已修", tone: "good" },
    "in-progress": { label: "在修", tone: "warn" },
    pending: { label: "待修", tone: "muted" },
  };
  const s = statusMap[c.status];
  return (
    <div className="trow">
      <div className="tc tc-code mono">{c.code}</div>
      <div className="tc tc-name">
        <div className="tc-name-main">{c.name}</div>
        {c.category && <div className="tc-name-tag">通識 · {c.category}</div>}
      </div>
      <div className="tc tc-cred">{c.credits}</div>
      <div className="tc tc-sem">{c.sem}</div>
      <div className="tc tc-grade">{c.grade || "—"}</div>
      <div className="tc tc-status">
        <span className={"pill pill-"+s.tone}>{s.label}</span>
      </div>
    </div>
  );
}

Object.assign(window, { PageCourses, CourseRow });
