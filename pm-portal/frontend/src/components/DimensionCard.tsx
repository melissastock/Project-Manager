import React from "react";
import type { DimensionScore } from "../types";

export function DimensionCard({ dimension }: { dimension: DimensionScore }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12, marginBottom: 8 }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <strong>{dimension.dimension.replace("_", " ")}</strong>
        <span>{dimension.score}</span>
      </div>
      <ul style={{ marginTop: 8 }}>
        {dimension.evidence.map((e) => <li key={e}>{e}</li>)}
      </ul>
    </div>
  );
}
