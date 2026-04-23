import React from "react";

export function ScoreBadge({ score, band }: { score: number; band: string }) {
  return (
    <div className="pm-score-badge">
      <strong className="pm-score-value">{score}</strong>
      <span className={`pm-pill ${band}`}>{band}</span>
    </div>
  );
}
