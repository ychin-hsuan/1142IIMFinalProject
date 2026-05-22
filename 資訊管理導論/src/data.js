// 114 入學版 — 長庚大學 資訊管理學系 畢業審查資料
// Original mock data for prototype

const STUDENT = {
  id: "B1344061",
  name: "王馨卉",
  dept: "資訊管理學系",
  enrollYear: "114",
  grade: "大二下",
  email: "b1344061@stmail.cgu.edu.tw",
  avatar: "WH",
};

const RULES = {
  required: 48,            // 系訂必修
  collegeCommon: 12,       // 管院共構
  deptElective: 30,        // 系選修 (本系)
  electiveThreshold: 42,   // 系選修門檻 (含他系/管院)
  generalEdu: 18,          // 通識
  pe: 0,                   // 體育不計學分
  total: 128,              // 畢業總學分
};

// 系訂必修 (17 門 / 48 學分)
const REQUIRED_COURSES = [
  { code: "IM101", name: "資訊管理導論", credits: 3, sem: "1上", status: "passed", grade: "A" },
  { code: "IM102", name: "程式設計（一）", credits: 3, sem: "1上", status: "passed", grade: "A-" },
  { code: "IM103", name: "微積分（一）", credits: 3, sem: "1上", status: "passed", grade: "B+" },
  { code: "IM104", name: "計算機概論", credits: 3, sem: "1上", status: "passed", grade: "A" },
  { code: "IM105", name: "程式設計（二）", credits: 3, sem: "1下", status: "passed", grade: "A" },
  { code: "IM106", name: "微積分（二）", credits: 3, sem: "1下", status: "passed", grade: "B" },
  { code: "IM107", name: "資料結構", credits: 3, sem: "1下", status: "passed", grade: "A-" },
  { code: "IM108", name: "管理學", credits: 3, sem: "1下", status: "passed", grade: "A" },
  { code: "IM201", name: "資料庫管理", credits: 3, sem: "2上", status: "passed", grade: "A" },
  { code: "IM202", name: "系統分析與設計", credits: 3, sem: "2上", status: "passed", grade: "A-" },
  { code: "IM203", name: "物件導向程式設計", credits: 3, sem: "2上", status: "passed", grade: "A" },
  { code: "IM204", name: "離散數學", credits: 3, sem: "2上", status: "passed", grade: "B+" },
  { code: "IM205", name: "演算法", credits: 3, sem: "2下", status: "in-progress", grade: null },
  { code: "IM206", name: "網路概論", credits: 3, sem: "2下", status: "in-progress", grade: null },
  { code: "IM301", name: "資訊管理專題（一）", credits: 3, sem: "3上", status: "pending", grade: null },
  { code: "IM302", name: "資訊管理專題（二）", credits: 3, sem: "3下", status: "pending", grade: null },
  { code: "IM303", name: "作業系統", credits: 3, sem: "3上", status: "pending", grade: null },
];

// 管院共構 (4 門 / 12 學分)
const COLLEGE_COMMON = [
  { code: "MGT101", name: "經濟學（一）", credits: 3, sem: "1上", status: "passed", grade: "B+" },
  { code: "MGT102", name: "會計學", credits: 3, sem: "1下", status: "passed", grade: "A-" },
  { code: "MGT201", name: "統計學", credits: 3, sem: "2上", status: "passed", grade: "B+" },
  { code: "MGT202", name: "經濟學（二）", credits: 3, sem: "2下", status: "in-progress", grade: null },
];

// 系選修 (本系) — 已修 / 在修
const DEPT_ELECTIVES = [
  { code: "IM251", name: "人工智慧導論", credits: 3, sem: "2上", status: "passed", grade: "A" },
  { code: "IM252", name: "雲端運算", credits: 3, sem: "2上", status: "passed", grade: "A-" },
  { code: "IM253", name: "資料探勘", credits: 3, sem: "2下", status: "in-progress", grade: null },
  { code: "IM254", name: "網頁程式設計", credits: 3, sem: "2下", status: "in-progress", grade: null },
];

// 通識
const GENERAL_EDU = [
  { code: "GE001", name: "心理學概論", credits: 2, sem: "1上", status: "passed", grade: "A", category: "全人" },
  { code: "GE002", name: "大學英文（一）", credits: 2, sem: "1上", status: "passed", grade: "B+", category: "英文" },
  { code: "GE003", name: "中國文學選讀", credits: 2, sem: "1下", status: "passed", grade: "A-", category: "核心" },
  { code: "GE004", name: "大學英文（二）", credits: 2, sem: "1下", status: "passed", grade: "B+", category: "英文" },
  { code: "GE005", name: "音樂賞析", credits: 2, sem: "2上", status: "passed", grade: "A", category: "多元" },
  { code: "GE006", name: "全人體育（一）", credits: 0, sem: "1上", status: "passed", grade: "通過", category: "體育" },
  { code: "GE007", name: "全人體育（二）", credits: 0, sem: "1下", status: "passed", grade: "通過", category: "體育" },
  { code: "GE008", name: "全人體育（三）", credits: 0, sem: "2上", status: "passed", grade: "通過", category: "體育" },
];

// 推薦課程 (AI / 模擬選課用)
const RECOMMENDED = [
  { code: "IM351", name: "機器學習", credits: 3, type: "系選修", rec: 95, reason: "已修人工智慧導論，可延續學習路徑" },
  { code: "IM352", name: "深度學習應用", credits: 3, type: "系選修", rec: 92, reason: "AI 進階課程，銜接專題方向" },
  { code: "IM353", name: "區塊鏈技術", credits: 3, type: "系選修", rec: 78, reason: "新興技術，補足跨域能力" },
  { code: "IM354", name: "資訊安全", credits: 3, type: "系選修", rec: 88, reason: "與網路概論互補" },
  { code: "MGT301", name: "行銷管理", credits: 3, type: "管院共構", rec: 72, reason: "強化商管基礎" },
  { code: "IM355", name: "使用者經驗設計", credits: 3, type: "系選修", rec: 85, reason: "結合系統分析與設計" },
  { code: "IM356", name: "行動應用開發", credits: 3, type: "系選修", rec: 90, reason: "實作導向，強化作品集" },
  { code: "GE101", name: "科技與社會", credits: 2, type: "通識-核心", rec: 80, reason: "通識核心領域尚缺" },
];

function getAllPassed() {
  return [...REQUIRED_COURSES, ...COLLEGE_COMMON, ...DEPT_ELECTIVES, ...GENERAL_EDU]
    .filter(c => c.status === "passed");
}
function getAllInProgress() {
  return [...REQUIRED_COURSES, ...COLLEGE_COMMON, ...DEPT_ELECTIVES, ...GENERAL_EDU]
    .filter(c => c.status === "in-progress");
}
function sumCredits(arr, includeInProgress = false) {
  return arr.filter(c => c.status === "passed" || (includeInProgress && c.status === "in-progress"))
            .reduce((s, c) => s + c.credits, 0);
}

const SUMMARY = {
  required: { earned: sumCredits(REQUIRED_COURSES), inProgress: sumCredits(REQUIRED_COURSES.filter(c=>c.status==="in-progress"), true), required: RULES.required },
  college: { earned: sumCredits(COLLEGE_COMMON), inProgress: sumCredits(COLLEGE_COMMON.filter(c=>c.status==="in-progress"), true), required: RULES.collegeCommon },
  deptElec: { earned: sumCredits(DEPT_ELECTIVES), inProgress: sumCredits(DEPT_ELECTIVES.filter(c=>c.status==="in-progress"), true), required: RULES.deptElective },
  general: { earned: sumCredits(GENERAL_EDU.filter(c=>c.credits>0)), inProgress: 0, required: RULES.generalEdu },
};

Object.assign(window, {
  STUDENT, RULES,
  REQUIRED_COURSES, COLLEGE_COMMON, DEPT_ELECTIVES, GENERAL_EDU, RECOMMENDED,
  SUMMARY, getAllPassed, getAllInProgress, sumCredits,
});
