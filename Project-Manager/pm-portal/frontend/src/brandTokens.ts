export const brandTokens = {
  navy: "var(--mjsds-navy)",
  navyDeep: "var(--mjsds-navy-deep)",
  gold: "var(--mjsds-gold)",
  goldLight: "var(--mjsds-gold-light)",
  goldPale: "var(--mjsds-gold-pale)",
  offWhite: "var(--mjsds-off-white)",
  white: "var(--mjsds-white)",
  slate: "var(--mjsds-slate)",
  ink: "var(--mjsds-ink)",
  inkMid: "var(--mjsds-ink-mid)",
  divider: "var(--mjsds-divider)",
  risk: "var(--mjsds-risk)"
} as const;

export type BrandTokenKey = keyof typeof brandTokens;

export function token(name: BrandTokenKey): string {
  return brandTokens[name];
}

