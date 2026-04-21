import React from "react";

export function ScoreBadge({ score, band }: { score: number; band: string }) {
  const colors: Record<string, string> = {
    ready: "#146c2e",
    monitor: "#8a6d1d",
    "at-risk": "#9b3d00",
    critical: "#8a1325"
  };
  return (
    <div style={{ display: "inline-flex", gap: 8, alignItems: "center" }}>
      <strong>{score}</strong>
      <span style={{ background: colors[band] || "#333", color: "white", borderRadius: 12, padding: "2px 10px", fontSize: 12 }}>{band}</span>
    </div>
  );
}
