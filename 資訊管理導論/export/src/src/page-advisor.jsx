// AI Advisor page — uses window.claude.complete
function PageAdvisor() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "嗨 馨卉！我是你的 AI 選課顧問。我已讀取你的修課紀錄與 114 入學版畢業規則。\n\n你現在的最大缺口是 **系選修（本系）**，已修 6 學分、在修 6 學分，門檻 30 學分。需要我幫你做大三選課規劃嗎？" },
  ]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages, busy]);

  const quick = [
    "我下學期該優先修哪些課？",
    "怎麼補滿系選修的 30 學分？",
    "通識還缺哪個領域？",
    "如果我想做 AI 方向的專題，要先修什麼？",
  ];

  async function send(text) {
    const q = (text ?? input).trim();
    if (!q || busy) return;
    setInput("");
    const next = [...messages, { role: "user", content: q }];
    setMessages(next);
    setBusy(true);

    const context = `你是長庚大學資管系畢業審查 AI 顧問。學生：${STUDENT.name} (${STUDENT.id})，114 入學，目前${STUDENT.grade}。
畢業規則（114版）：系訂必修48、管院共構12、系選修(本系)至少30、通識18、總學分128。
目前進度：
- 系訂必修 ${SUMMARY.required.earned}/${RULES.required} (在修 ${SUMMARY.required.inProgress})
- 管院共構 ${SUMMARY.college.earned}/${RULES.collegeCommon}
- 系選修(本系) ${SUMMARY.deptElec.earned}/${RULES.deptElective}
- 通識 ${SUMMARY.general.earned}/${RULES.generalEdu}
已修課程包含：人工智慧導論、雲端運算、資料庫管理、系統分析與設計、物件導向程式設計。
在修中：演算法、網路概論、資料探勘、網頁程式設計、經濟學二。
推薦池：機器學習、深度學習應用、區塊鏈技術、資訊安全、行動應用開發、UX設計、行銷管理。
請用繁體中文，回答精簡、條列、給具體建議；不要使用 markdown 標題符號 #。`;

    try {
      const reply = await window.claude.complete({
        messages: [
          { role: "user", content: context + "\n\n學生問題：" + q }
        ]
      });
      setMessages(m => [...m, { role: "assistant", content: reply }]);
    } catch (e) {
      setMessages(m => [...m, { role: "assistant", content: "（連線錯誤，請稍後再試）" }]);
    }
    setBusy(false);
  }

  // Top recommendations
  const top = [...RECOMMENDED].sort((a,b)=>b.rec-a.rec).slice(0,3);

  return (
    <div className="page page-advisor">
      <div className="page-head">
        <div>
          <div className="page-eyebrow">AI ADVISOR · OpenAI · Powered by Claude</div>
          <h2 className="page-title">AI 選課顧問</h2>
        </div>
        <div className="head-meta">
          <div className="meta-block"><div className="meta-l">系選修缺口</div><div className="meta-v" style={{color:"var(--warn)"}}>−24</div></div>
          <div className="meta-block"><div className="meta-l">建議下學期修</div><div className="meta-v">12-15</div></div>
        </div>
      </div>

      <div className="advisor-grid">
        <section className="card card-chat">
          <div className="chat-head">
            <div className="chat-avatar"><Icon name="ai"/></div>
            <div className="chat-meta">
              <div className="chat-name">畢業審查助手</div>
              <div className="chat-sub"><span className="dot dot-ok"/> 已讀取你的修課紀錄</div>
            </div>
          </div>
          <div className="chat-body" ref={scrollRef}>
            {messages.map((m,i) => (
              <div key={i} className={"msg msg-"+m.role}>
                {m.role==="assistant" && <div className="msg-icon"><Icon name="sparkles" size={14}/></div>}
                <div className="msg-bubble">{renderMD(m.content)}</div>
              </div>
            ))}
            {busy && (
              <div className="msg msg-assistant">
                <div className="msg-icon"><Icon name="sparkles" size={14}/></div>
                <div className="msg-bubble msg-typing"><span/><span/><span/></div>
              </div>
            )}
          </div>
          <div className="chat-quick">
            {quick.map((q,i) => (
              <button key={i} className="quick-chip" onClick={()=>send(q)} disabled={busy}>{q}</button>
            ))}
          </div>
          <div className="chat-input">
            <input
              placeholder="輸入問題… 例如：我下學期該修哪些課？"
              value={input}
              onChange={e=>setInput(e.target.value)}
              onKeyDown={e=>{ if(e.key==="Enter") send(); }}
              disabled={busy}
            />
            <button className="send-btn" onClick={()=>send()} disabled={busy || !input.trim()}>
              <Icon name="send" size={16}/>
            </button>
          </div>
        </section>

        <aside className="advisor-side">
          <section className="card card-reco">
            <div className="card-head">
              <div className="card-title">本週推薦課程</div>
              <div className="card-sub">依缺修狀況計算</div>
            </div>
            <ul className="reco-list">
              {top.map(c => (
                <li className="reco-item" key={c.code}>
                  <div className="reco-head">
                    <div className="reco-name">{c.name}</div>
                    <div className="reco-score">{c.rec}</div>
                  </div>
                  <div className="reco-meta">
                    <span className="reco-type">{c.type}</span>
                    <span className="reco-credit">{c.credits} 學分</span>
                    <span className="reco-code mono">{c.code}</span>
                  </div>
                  <div className="reco-reason">{c.reason}</div>
                </li>
              ))}
            </ul>
          </section>

          <section className="card card-gap">
            <div className="card-head">
              <div className="card-title">缺修分析</div>
            </div>
            <div className="gap-list">
              <GapRow label="系訂必修" need={Math.max(0,RULES.required-SUMMARY.required.earned-SUMMARY.required.inProgress)} tone="accent"/>
              <GapRow label="管院共構" need={Math.max(0,RULES.collegeCommon-SUMMARY.college.earned-SUMMARY.college.inProgress)} tone="good"/>
              <GapRow label="系選修（本系）" need={Math.max(0,RULES.deptElective-SUMMARY.deptElec.earned-SUMMARY.deptElec.inProgress)} tone="warn"/>
              <GapRow label="通識" need={Math.max(0,RULES.generalEdu-SUMMARY.general.earned)} tone="ink"/>
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}

function GapRow({label, need, tone}) {
  return (
    <div className="gap-row">
      <div className="gap-label">{label}</div>
      <div className={"gap-need tone-"+tone}>{need>0 ? `缺 ${need}` : "已達標"}</div>
    </div>
  );
}

// Minimal markdown: bold + newlines
function renderMD(text) {
  const lines = String(text).split(/\n/);
  return lines.map((ln, i) => {
    const parts = ln.split(/(\*\*[^*]+\*\*)/g);
    return (
      <div key={i} className="md-line">
        {parts.map((p,j) => {
          if (/^\*\*[^*]+\*\*$/.test(p)) return <b key={j}>{p.slice(2,-2)}</b>;
          return <span key={j}>{p}</span>;
        })}
      </div>
    );
  });
}

Object.assign(window, { PageAdvisor, GapRow, renderMD });
