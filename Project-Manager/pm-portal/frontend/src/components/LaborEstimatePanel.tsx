import React, { useEffect, useMemo, useState } from "react";
import { createLaborEstimate } from "../api";
import type { ProjectReadiness } from "../types";
import laborPresetRules from "../config/laborPresetRules.json";

const MODULES: Array<"strategy" | "development" | "operationalization" | "governance" | "marketing" | "gtm"> = [
  "strategy",
  "development",
  "operationalization",
  "governance",
  "marketing",
  "gtm",
];

type CostPreset = "lean" | "standard" | "scale";
type LaborPresetRule = {
  preset: CostPreset;
  matchAny: string[];
};

const COST_PRESETS: Record<
  CostPreset,
  {
    hourlyRate: number;
    hostingOneTime: number;
    hostingMonthly: number;
    storageOneTime: number;
    storageMonthly: number;
    toolsOneTime: number;
    toolsMonthly: number;
    securityOneTime: number;
    securityMonthly: number;
    opsOneTime: number;
    opsMonthly: number;
    contingencyOneTime: number;
    contingencyMonthly: number;
  }
> = {
  lean: {
    hourlyRate: 125,
    hostingOneTime: 250,
    hostingMonthly: 120,
    storageOneTime: 100,
    storageMonthly: 50,
    toolsOneTime: 200,
    toolsMonthly: 80,
    securityOneTime: 200,
    securityMonthly: 60,
    opsOneTime: 200,
    opsMonthly: 90,
    contingencyOneTime: 300,
    contingencyMonthly: 40,
  },
  standard: {
    hourlyRate: 150,
    hostingOneTime: 600,
    hostingMonthly: 280,
    storageOneTime: 250,
    storageMonthly: 120,
    toolsOneTime: 500,
    toolsMonthly: 220,
    securityOneTime: 450,
    securityMonthly: 180,
    opsOneTime: 400,
    opsMonthly: 240,
    contingencyOneTime: 900,
    contingencyMonthly: 120,
  },
  scale: {
    hourlyRate: 190,
    hostingOneTime: 1200,
    hostingMonthly: 750,
    storageOneTime: 600,
    storageMonthly: 350,
    toolsOneTime: 900,
    toolsMonthly: 480,
    securityOneTime: 1200,
    securityMonthly: 550,
    opsOneTime: 800,
    opsMonthly: 650,
    contingencyOneTime: 2000,
    contingencyMonthly: 300,
  },
};

export function LaborEstimatePanel({ project, onRefresh }: { project: ProjectReadiness; onRefresh: () => Promise<void> }) {
  const [hourlyRate, setHourlyRate] = useState(150);
  const [createdBy, setCreatedBy] = useState("Melissa Stock");
  const [costPreset, setCostPreset] = useState<CostPreset>("standard");
  const [confidence, setConfidence] = useState<"low" | "medium" | "high">("medium");
  const [recommendedPreset, setRecommendedPreset] = useState<CostPreset>("standard");
  const [presetInitializedForProject, setPresetInitializedForProject] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [hours, setHours] = useState<Record<string, string>>({
    strategy: "",
    development: "",
    operationalization: "",
    governance: "",
    marketing: "",
    gtm: "",
  });
  const [notes, setNotes] = useState<Record<string, string>>({
    strategy: "Include competitive review, SWOT, positioning, and priority roadmap.",
    development: "",
    operationalization: "",
    governance: "",
    marketing: "",
    gtm: "",
  });
  const [nonLabor, setNonLabor] = useState({
    hosting_one_time: "",
    hosting_monthly: "",
    storage_one_time: "",
    storage_monthly: "",
    tools_one_time: "",
    tools_monthly: "",
    security_one_time: "",
    security_monthly: "",
    ops_one_time: "",
    ops_monthly: "",
    contingency_one_time: "",
    contingency_monthly: "",
  });
  const latestEstimate = project.labor_estimates[0];
  const estimatedTotalHours = useMemo(
    () =>
      MODULES.reduce((acc, moduleKey) => {
        const parsed = Number(hours[moduleKey] || "0");
        return acc + (Number.isFinite(parsed) ? parsed : 0);
      }, 0),
    [hours]
  );
  const estimatedTotalCost = useMemo(
    () => Math.round(estimatedTotalHours * hourlyRate * 100) / 100,
    [estimatedTotalHours, hourlyRate]
  );
  const nonLaborMonthly = useMemo(() => {
    const keys = ["hosting_monthly", "storage_monthly", "tools_monthly", "security_monthly", "ops_monthly", "contingency_monthly"] as const;
    return keys.reduce((acc, key) => acc + Number(nonLabor[key] || "0"), 0);
  }, [nonLabor]);
  const nonLaborOneTime = useMemo(() => {
    const keys = ["hosting_one_time", "storage_one_time", "tools_one_time", "security_one_time", "ops_one_time", "contingency_one_time"] as const;
    return keys.reduce((acc, key) => acc + Number(nonLabor[key] || "0"), 0);
  }, [nonLabor]);
  const buildCost = Math.round((estimatedTotalCost + nonLaborOneTime) * 100) / 100;
  const tco12m = Math.round((buildCost + (nonLaborMonthly * 12)) * 100) / 100;

  function strategySubcomponents() {
    return ["competitive-review", "swot", "positioning", "offer-architecture", "priority-roadmap"];
  }

  function inferPresetFromProjectContext(): CostPreset {
    const category = String(project.project.category || "").toLowerCase();
    const lane = String(project.project.lane || "").toLowerCase();
    const role = String(project.project.role || "").toLowerCase();
    const stage = String(project.project.intake_stage || "").toLowerCase();
    const profile = `${category} ${lane} ${role} ${stage}`;

    const rules = (laborPresetRules.rules ?? []) as LaborPresetRule[];
    for (const rule of rules) {
      for (const keyword of rule.matchAny) {
        if (profile.includes(keyword.toLowerCase())) {
          return rule.preset;
        }
      }
    }
    return (laborPresetRules.defaultPreset as CostPreset) || "standard";
  }

  function applyPreset(preset: CostPreset) {
    const selected = COST_PRESETS[preset];
    setCostPreset(preset);
    setHourlyRate(selected.hourlyRate);
    setNonLabor({
      hosting_one_time: String(selected.hostingOneTime),
      hosting_monthly: String(selected.hostingMonthly),
      storage_one_time: String(selected.storageOneTime),
      storage_monthly: String(selected.storageMonthly),
      tools_one_time: String(selected.toolsOneTime),
      tools_monthly: String(selected.toolsMonthly),
      security_one_time: String(selected.securityOneTime),
      security_monthly: String(selected.securityMonthly),
      ops_one_time: String(selected.opsOneTime),
      ops_monthly: String(selected.opsMonthly),
      contingency_one_time: String(selected.contingencyOneTime),
      contingency_monthly: String(selected.contingencyMonthly),
    });
  }

  useEffect(() => {
    const inferred = inferPresetFromProjectContext();
    setRecommendedPreset(inferred);
    if (presetInitializedForProject !== project.project.name) {
      applyPreset(inferred);
      setPresetInitializedForProject(project.project.name);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [project.project.name, project.project.category, project.project.lane, project.project.role, project.project.intake_stage]);

  async function submitEstimate() {
    try {
      setBusy(true);
      setError("");
      const modules = MODULES.map((moduleKey) => {
        const parsed = Number(hours[moduleKey] || "0");
        return {
          module_key: moduleKey,
          estimated_hours: Number.isFinite(parsed) ? parsed : 0,
          notes: notes[moduleKey] || "",
          subcomponents: moduleKey === "strategy" ? strategySubcomponents() : [],
        };
      }).filter((item) => item.estimated_hours > 0);
      if (modules.length === 0) {
        throw new Error("Add at least one module hour estimate.");
      }
      await createLaborEstimate({
        project: project.project.name,
        hourly_rate_usd: hourlyRate,
        confidence,
        assumptions: ["Estimate intended for post-intake pre-onboarding planning."],
        created_by: createdBy,
        modules,
        non_labor_costs: [
          { category: "hosting", one_time_usd: Number(nonLabor.hosting_one_time || "0"), monthly_recurring_usd: Number(nonLabor.hosting_monthly || "0"), usage_variable_monthly_usd: 0, notes: "Hosting and runtime" },
          { category: "storage", one_time_usd: Number(nonLabor.storage_one_time || "0"), monthly_recurring_usd: Number(nonLabor.storage_monthly || "0"), usage_variable_monthly_usd: 0, notes: "Storage and backups" },
          { category: "third_party_tools", one_time_usd: Number(nonLabor.tools_one_time || "0"), monthly_recurring_usd: Number(nonLabor.tools_monthly || "0"), usage_variable_monthly_usd: 0, notes: "Third-party tooling and integrations" },
          { category: "security_compliance", one_time_usd: Number(nonLabor.security_one_time || "0"), monthly_recurring_usd: Number(nonLabor.security_monthly || "0"), usage_variable_monthly_usd: 0, notes: "Security and compliance overhead" },
          { category: "operations_support", one_time_usd: Number(nonLabor.ops_one_time || "0"), monthly_recurring_usd: Number(nonLabor.ops_monthly || "0"), usage_variable_monthly_usd: 0, notes: "Support and operations load" },
          { category: "contingency", one_time_usd: Number(nonLabor.contingency_one_time || "0"), monthly_recurring_usd: Number(nonLabor.contingency_monthly || "0"), usage_variable_monthly_usd: 0, notes: "Contingency buffer" },
        ],
      });
      await onRefresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <h3 className="pm-section-title pm-section-title-spaced">Labor Estimate (Post-Intake, Pre-Onboarding)</h3>
      <p className="pm-subtitle">
        End-to-end estimate for expected effort and cost before onboarding. Use this with the client and legal counsel to review assumptions, budget impact, and change risk.
      </p>
      {error ? <p className="pm-error">{error}</p> : null}
      <div className="pm-card pm-card-block">
        <div className="pm-action-row">
          <input className="pm-input" value={createdBy} onChange={(e) => setCreatedBy(e.target.value)} placeholder="Prepared by" />
          <input
            className="pm-input"
            type="number"
            value={hourlyRate}
            onChange={(e) => setHourlyRate(Number(e.target.value || "0"))}
            placeholder="Hourly rate (USD)"
          />
          <select className="pm-input" value={confidence} onChange={(e) => setConfidence(e.target.value as "low" | "medium" | "high")}>
            <option value="low">Low confidence</option>
            <option value="medium">Medium confidence</option>
            <option value="high">High confidence</option>
          </select>
          <select className="pm-input" value={costPreset} onChange={(e) => applyPreset(e.target.value as CostPreset)}>
            <option value="lean">Lean preset</option>
            <option value="standard">Standard preset</option>
            <option value="scale">Scale preset</option>
          </select>
          <button className="pm-action-btn secondary" onClick={() => applyPreset(recommendedPreset)}>
            Use Recommended ({recommendedPreset})
          </button>
          <button className="pm-action-btn secondary" onClick={() => applyPreset(costPreset)}>
            Apply Preset
          </button>
        </div>

        {MODULES.map((moduleKey) => (
          <div key={moduleKey} className="pm-card pm-card-block">
            <div className="pm-meta-label">{moduleKey.charAt(0).toUpperCase() + moduleKey.slice(1)}</div>
            <div className="pm-action-row">
              <input
                className="pm-input"
                type="number"
                placeholder="Estimated hours for this module"
                value={hours[moduleKey]}
                onChange={(e) => setHours((prev) => ({ ...prev, [moduleKey]: e.target.value }))}
              />
              <input
                className="pm-input"
                placeholder="Client-facing notes (assumptions, exclusions, legal constraints)"
                value={notes[moduleKey]}
                onChange={(e) => setNotes((prev) => ({ ...prev, [moduleKey]: e.target.value }))}
              />
            </div>
          </div>
        ))}

        <p className="pm-muted-metadata">
          Labor preview: {estimatedTotalHours} hours | ${estimatedTotalCost.toLocaleString()} estimated labor cost
        </p>
        <div className="pm-card pm-card-block">
          <div className="pm-meta-label">Non-labor costs (infrastructure and operating costs)</div>
          <div className="pm-action-row">
            <input className="pm-input" type="number" placeholder="Hosting one-time" value={nonLabor.hosting_one_time} onChange={(e) => setNonLabor((p) => ({ ...p, hosting_one_time: e.target.value }))} />
            <input className="pm-input" type="number" placeholder="Hosting monthly" value={nonLabor.hosting_monthly} onChange={(e) => setNonLabor((p) => ({ ...p, hosting_monthly: e.target.value }))} />
          </div>
          <div className="pm-action-row">
            <input className="pm-input" type="number" placeholder="Storage one-time" value={nonLabor.storage_one_time} onChange={(e) => setNonLabor((p) => ({ ...p, storage_one_time: e.target.value }))} />
            <input className="pm-input" type="number" placeholder="Storage monthly" value={nonLabor.storage_monthly} onChange={(e) => setNonLabor((p) => ({ ...p, storage_monthly: e.target.value }))} />
          </div>
          <div className="pm-action-row">
            <input className="pm-input" type="number" placeholder="Tools one-time" value={nonLabor.tools_one_time} onChange={(e) => setNonLabor((p) => ({ ...p, tools_one_time: e.target.value }))} />
            <input className="pm-input" type="number" placeholder="Tools monthly" value={nonLabor.tools_monthly} onChange={(e) => setNonLabor((p) => ({ ...p, tools_monthly: e.target.value }))} />
          </div>
          <div className="pm-action-row">
            <input className="pm-input" type="number" placeholder="Security one-time" value={nonLabor.security_one_time} onChange={(e) => setNonLabor((p) => ({ ...p, security_one_time: e.target.value }))} />
            <input className="pm-input" type="number" placeholder="Security monthly" value={nonLabor.security_monthly} onChange={(e) => setNonLabor((p) => ({ ...p, security_monthly: e.target.value }))} />
          </div>
          <div className="pm-action-row">
            <input className="pm-input" type="number" placeholder="Ops one-time" value={nonLabor.ops_one_time} onChange={(e) => setNonLabor((p) => ({ ...p, ops_one_time: e.target.value }))} />
            <input className="pm-input" type="number" placeholder="Ops monthly" value={nonLabor.ops_monthly} onChange={(e) => setNonLabor((p) => ({ ...p, ops_monthly: e.target.value }))} />
          </div>
          <div className="pm-action-row">
            <input className="pm-input" type="number" placeholder="Contingency one-time" value={nonLabor.contingency_one_time} onChange={(e) => setNonLabor((p) => ({ ...p, contingency_one_time: e.target.value }))} />
            <input className="pm-input" type="number" placeholder="Contingency monthly" value={nonLabor.contingency_monthly} onChange={(e) => setNonLabor((p) => ({ ...p, contingency_monthly: e.target.value }))} />
          </div>
          <p className="pm-muted-metadata">
            Build cost (labor + one-time costs): ${buildCost.toLocaleString()} | Monthly run cost: ${nonLaborMonthly.toLocaleString()} | 12-month total cost (TCO): ${tco12m.toLocaleString()}
          </p>
        </div>
        <button className="pm-action-btn" disabled={busy} onClick={submitEstimate}>
          Save Labor Estimate
        </button>
      </div>

      {latestEstimate ? (
        <div className="pm-card pm-card-block">
          <div className="pm-meta-label">Latest saved estimate</div>
          <p className="pm-muted-metadata">
            {latestEstimate.total_hours} labor hours | ${latestEstimate.total_cost_usd.toLocaleString()} labor | {latestEstimate.confidence} confidence
          </p>
          <p className="pm-muted-metadata">
            Build: ${latestEstimate.total_build_cost_usd.toLocaleString()} | Monthly run: ${latestEstimate.total_monthly_run_cost_usd.toLocaleString()} | 12m TCO: ${latestEstimate.projected_12m_tco_usd.toLocaleString()}
          </p>
          {latestEstimate.modules.map((module) => (
            <p key={module.module_key} className="pm-muted-metadata">
              {module.module_key}: {module.estimated_hours}h (${module.estimated_cost_usd.toLocaleString()})
            </p>
          ))}
        </div>
      ) : null}
    </div>
  );
}
