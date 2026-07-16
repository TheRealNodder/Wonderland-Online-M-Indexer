"use strict";

const SECTIONS = [
  ["search", "Global Search"],
  ["monsters", "Monsters"],
  ["items", "Items"],
  ["drops", "Drops"],
  ["maps", "Maps"],
  ["step_afk_locations", "Step-Based AFK Locations"],
  ["visible_spawns", "Visible Spawns"],
  ["dungeons", "Dungeons"],
  ["npcs", "NPC Directory"],
  ["shops", "Shops"],
  ["quests", "Quests"],
  ["quest_chains", "Quest Chains"],
  ["quest_rewards", "Quest Rewards"],
  ["map_requirements", "Map Requirements"],
  ["portals_teleports", "Portals and Teleports"],
  ["compounds", "Compounding"],
  ["localization", "Localization"],
  ["evidence", "Extraction Evidence"],
  ["unresolved", "Unresolved Records"],
  ["verification_issues", "Verification Issues"],
];

const COLUMN_DEFS = {
  items: [["item_id", "Item ID"], ["display_name", "Name"], ["category", "Category"], ["icon_asset", "Asset"], ["confidence", "Confidence"]],
  monsters: [["monster_id", "Monster ID"], ["display_name", "Name"], ["level", "Level"], ["element", "Element"], ["encounter_type", "Encounter"], ["confidence", "Confidence"]],
  drops: [["drop_table_id", "Drop Table"], ["monster_name", "Monster"], ["item_name", "Item"], ["quantity", "Quantity"], ["calculated_percentage", "Rate"], ["confidence", "Confidence"]],
  maps: [["map_id", "Map ID"], ["display_name", "Name"], ["region", "Region"], ["floor", "Floor"], ["minimap_asset", "Asset"], ["confidence", "Confidence"]],
  npcs: [["npc_id", "NPC ID"], ["display_name", "Name"], ["function", "Function"], ["map_name", "Map"], ["coordinates", "Coordinates"], ["confidence", "Confidence"]],
  shops: [["shop_id", "Shop ID"], ["shop_name", "Shop"], ["npc_id", "NPC"], ["map_id", "Map"], ["inventory_count", "Items"], ["confidence", "Confidence"]],
  quests: [["quest_id", "Quest ID"], ["display_title", "Title"], ["category", "Category"], ["starting_npc_name", "Starts At"], ["completion_npc_name", "Completes At"], ["confidence", "Confidence"]],
  localization: [["localization_key", "Key"], ["language", "Language"], ["display_text", "Text"], ["category", "Category"], ["confidence", "Confidence"]],
  evidence: [["entity_type", "Entity"], ["entity_id", "ID"], ["field_name", "Field"], ["source_file", "Source"], ["confidence", "Confidence"]],
  unresolved: [["relationship_type", "Relationship"], ["source_id", "Source"], ["reason", "Reason"], ["next_step", "Next Step"], ["confidence", "Confidence"]],
  verification_issues: [["severity", "Severity"], ["issue_type", "Type"], ["entity_type", "Entity"], ["entity_id", "ID"], ["details", "Details"]],
};

const PAGE_SIZE = 250;
const state = { data: null, active: "search", query: "", confirmedOnly: false, confidence: "", page: 0 };

const els = {};

function text(value) {
  if (value === null || value === undefined || value === "") return "—";
  if (Array.isArray(value)) return value.length ? value.join(", ") : "—";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function escapeHtml(value) {
  return text(value).replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
}

function sectionRows(key) {
  if (!state.data) return [];
  if (key === "search") {
    if (!state.query.trim()) return [];
    return SECTIONS.filter(([section]) => !["search"].includes(section)).flatMap(([section, label]) =>
      (state.data[section] || []).map(record => ({ ...record, _section: label, _sectionKey: section }))
    );
  }
  return state.data[key] || [];
}

function confidenceClass(value) {
  if (["direct_client_record", "direct_localization_match", "direct_asset_relationship"].includes(value)) return "direct";
  if (value === "unresolved") return "unresolved";
  return "warning";
}

function isConfirmed(record) {
  return ["direct_client_record", "direct_localization_match", "direct_asset_relationship"].includes(record.confidence);
}

function searchable(record) {
  return JSON.stringify(record).toLocaleLowerCase();
}

function filteredRows() {
  let rows = sectionRows(state.active);
  const query = state.query.trim().toLocaleLowerCase();
  if (query) rows = rows.filter(record => searchable(record).includes(query));
  if (state.confirmedOnly) rows = rows.filter(isConfirmed);
  if (state.confidence) rows = rows.filter(record => record.confidence === state.confidence);
  return rows;
}

function inferColumns(rows) {
  if (state.active === "search") return [["_section", "Section"], ["_identity", "Record"], ["confidence", "Confidence"], ["source_file", "Source"]];
  if (COLUMN_DEFS[state.active]) return COLUMN_DEFS[state.active];
  const keys = rows.length ? Object.keys(rows[0]).filter(key => !key.startsWith("_")).slice(0, 6) : [];
  return keys.map(key => [key, key.replaceAll("_", " ")]);
}

function identity(record) {
  const idKey = Object.keys(record).find(key => /(^|_)id$/.test(key));
  const nameKey = Object.keys(record).find(key => /(display_name|display_title|shop_name|item_name|monster_name|internal_name)/.test(key) && record[key]);
  return [nameKey ? record[nameKey] : "Record", idKey ? `#${record[idKey]}` : ""].filter(Boolean).join(" ");
}

function renderCell(record, key) {
  let value = key === "_identity" ? identity(record) : record[key];
  if (key === "confidence") return `<span class="tag ${confidenceClass(value)}">${escapeHtml(value)}</span>`;
  if (key.endsWith("asset") && value) {
    const title = record.display_name || record.internal_name || identity(record);
    return `<div class="primary-cell"><img class="record-image" src="${escapeHtml(value)}" alt=""><div><strong>${escapeHtml(title)}</strong><small>${escapeHtml(value)}</small></div></div>`;
  }
  if (key === "source_file") return `<span class="mono muted">${escapeHtml(value)}</span>`;
  if (/(^|_)id$/.test(key) || key.includes("_key")) return `<span class="mono">${escapeHtml(value)}</span>`;
  return escapeHtml(value);
}

function renderTable() {
  const rows = filteredRows();
  const columns = inferColumns(rows);
  const pageCount = Math.max(1, Math.ceil(rows.length / PAGE_SIZE));
  state.page = Math.min(state.page, pageCount - 1);
  const pageRows = rows.slice(state.page * PAGE_SIZE, (state.page + 1) * PAGE_SIZE);
  els.recordCount.textContent = `${rows.length.toLocaleString()} ${rows.length === 1 ? "record" : "records"}`;
  els.tableHead.innerHTML = `<tr>${columns.map(([, label]) => `<th>${escapeHtml(label)}</th>`).join("")}</tr>`;
  els.tableBody.innerHTML = pageRows.map((record, index) =>
    `<tr data-row="${index}">${columns.map(([key]) => `<td>${renderCell(record, key)}</td>`).join("")}</tr>`
  ).join("");
  els.emptyState.hidden = rows.length !== 0;
  els.tableWrap.hidden = rows.length === 0;
  els.tableBody.querySelectorAll("tr").forEach(row => row.addEventListener("click", () => openRecord(pageRows[Number(row.dataset.row)])));
  els.pagination.hidden = rows.length <= PAGE_SIZE;
  els.pageLabel.textContent = `Page ${state.page + 1} of ${pageCount}`;
  els.prevPage.disabled = state.page === 0;
  els.nextPage.disabled = state.page >= pageCount - 1;
}

function renderNav() {
  els.sectionNav.innerHTML = SECTIONS.map(([key, label]) => {
    const count = key === "search" ? "" : (state.data[key] || []).length.toLocaleString();
    return `<button type="button" class="nav-button ${key === state.active ? "active" : ""}" data-section="${key}"><span>${escapeHtml(label)}</span><span class="nav-count">${count}</span></button>`;
  }).join("");
  els.sectionNav.querySelectorAll("button").forEach(button => button.addEventListener("click", () => {
    state.active = button.dataset.section;
    state.page = 0;
    const section = SECTIONS.find(([key]) => key === state.active);
    els.viewTitle.textContent = section[1];
    els.viewEyebrow.textContent = state.active === "search" ? "INDEX" : "CURRENT CLIENT";
    renderNav();
    renderTable();
    window.scrollTo({ top: 0, behavior: "auto" });
  }));
}

function renderSummary() {
  const meta = state.data.meta || {};
  const values = [
    ["Files scanned", meta.files_scanned || 0],
    ["Items", (state.data.items || []).length],
    ["Maps", (state.data.maps || []).length],
    ["Localization", meta.localization_count || 0],
    ["Evidence", (state.data.evidence || []).length],
    ["Unresolved", (state.data.unresolved || []).length],
  ];
  els.summaryBand.innerHTML = values.map(([label, value]) => `<div class="summary-stat"><span>${escapeHtml(label)}</span><strong>${Number(value).toLocaleString()}</strong></div>`).join("");
}

function openRecord(record) {
  els.dialogKind.textContent = record._section || SECTIONS.find(([key]) => key === state.active)?.[1] || "Record";
  els.dialogTitle.textContent = identity(record);
  const image = record.icon_asset || record.minimap_asset || record.full_map_asset;
  const rows = Object.entries(record).filter(([key]) => !key.startsWith("_")).map(([key, value]) =>
    `<div class="detail-row"><dt>${escapeHtml(key.replaceAll("_", " "))}</dt><dd class="${key.includes("id") || key.includes("key") || key === "source_file" ? "mono" : ""}">${escapeHtml(value)}</dd></div>`
  ).join("");
  els.dialogBody.innerHTML = `${image ? `<img class="detail-image" src="${escapeHtml(image)}" alt="">` : ""}<dl>${rows}</dl>`;
  els.recordDialog.showModal();
}

function bind() {
  els.globalSearch.addEventListener("input", event => { state.query = event.target.value; state.page = 0; renderTable(); });
  els.confirmedOnly.addEventListener("change", event => { state.confirmedOnly = event.target.checked; state.page = 0; renderTable(); });
  els.confidenceFilter.addEventListener("change", event => { state.confidence = event.target.value; state.page = 0; renderTable(); });
  els.prevPage.addEventListener("click", () => { if (state.page > 0) { state.page -= 1; renderTable(); } });
  els.nextPage.addEventListener("click", () => { state.page += 1; renderTable(); });
  els.closeDialog.addEventListener("click", () => els.recordDialog.close());
  els.recordDialog.addEventListener("click", event => { if (event.target === els.recordDialog) els.recordDialog.close(); });
  window.addEventListener("keydown", event => { if (event.key === "/" && document.activeElement !== els.globalSearch) { event.preventDefault(); els.globalSearch.focus(); } });
}

async function start() {
  ["clientLabel", "buildStatus", "sectionNav", "globalSearch", "confirmedOnly", "confidenceFilter", "summaryBand", "viewEyebrow", "viewTitle", "recordCount", "emptyState", "tableWrap", "tableHead", "tableBody", "pagination", "prevPage", "nextPage", "pageLabel", "recordDialog", "dialogKind", "dialogTitle", "dialogBody", "closeDialog"].forEach(id => els[id] = document.getElementById(id));
  bind();
  try {
    const response = await fetch("./data/runtime-index.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.data = await response.json();
    els.clientLabel.textContent = `${state.data.meta?.unity_version || "Current Steam client"} · ${state.data.meta?.verification_status || "current_client_extracted"}`;
    els.buildStatus.textContent = `Indexed ${state.data.meta?.generated_at || ""}`;
    document.querySelector(".status-dot").classList.add("ready");
  } catch (error) {
    state.data = Object.fromEntries(SECTIONS.filter(([key]) => key !== "search").map(([key]) => [key, []]));
    state.data.meta = {};
    els.buildStatus.textContent = "Index unavailable";
    console.error(error);
  }
  renderSummary();
  renderNav();
  renderTable();
}

start();
