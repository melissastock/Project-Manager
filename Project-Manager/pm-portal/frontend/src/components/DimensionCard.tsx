import React from "react";
import type { DimensionScore } from "../types";

export function DimensionCard({ dimension }: { dimension: DimensionScore }) {
  return (
    <div className="pm-card pm-card-block">
      <div className="pm-flex-between">
        <strong>{dimension.dimension.replace("_", " ")}</strong>
        <span>{dimension.score}</span>
      </div>
      <ul className="pm-inline-list">
        {dimension.evidence.map((e) => <li key={e}>{e}</li>)}
      </ul>
    </div>
  );
}
