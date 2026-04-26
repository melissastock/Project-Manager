# First-party evidence — integrated summary (F24-1036-462)

**Purpose:** Single governed narrative that ties **portal/docket text**, the **2026-04-26 court setting** image, and **known discovery gaps** (police/EMS/hospital/Colorado) so operators know what is in-repo versus what must be pulled from archive or counsel.

**Local disk vs. this git workspace:** The cloud copy of the portfolio (used by agents) only sees files that are **checked out under** `/workspace` (or the same paths on a developer machine). If police reports, hospital PDFs, Denver/TCLEOSE prints, and email exports live on **your** hard drive, they are **invisible to automation here** until you **copy, rsync, or mount** that tree into the repo (often under `Archiavellian-Archive/`, per `Project-Manager/docs/bg-legal-folder-migration.md`) or you record absolute paths in a **local-only** `local-paths.md` (not committed; see `local-paths.md.example`). A prior iCloud file index in this repository referenced `BrandonDewayneGarner-InteliusReport.pdf` under an **Archiavellian-Archive/…/Aneumind/** ingest path on a local Mac — that file is **not** present in the current cloud workspace.

**Case:** F24-1036-462 — Denton County, Texas, County Criminal Court No. 5 (sitting as a felony court).  
**Defendant (records):** Brandon Dewayne Garner / Brandon Garner Sr. (portal shows DOB 06/03/1985; address Aurora, CO on case display).  
**Charge:** Intoxication manslaughter with vehicle (Penal Code 49.08(b)), second-degree felony.  
**Alleged offense date:** 2021-12-25 (treated as the crash/incident date on the public case header; confirm on indictment and police report).

---

## 1. Crash timing vs. law enforcement and EMS response (what we can say from current inputs)

| Topic | In-repo / attached status | Notes |
| --- | --- | --- |
| Crash or offense date | **In portal summary** | **2021-12-25** is the offense date field on the case display. This is not yet tied in-repo to a specific clock time. |
| Police arrival time / first unit on scene | **Not in attached images** | No dash times on the docket exports provided. **Next step:** index the Krum (or other) agency **offense or crash report** and CAD/dispatch if obtained in discovery. |
| Police report (narrative, measurements, SFT/blood) | **Not in attached images** | Required for time-on-scene, witness list, and DA theory alignment. |
| EMS / fire response times | **Not in attached images** | Docket shows **State subpoena applications 2025-09-04 and 2025-09-11** to **Medical City Denton**, **THR Presby Denton**, and **Krum Fire Department** — that implies the State was gathering **records** from those entities; it does not yield times until the **returned records** or officer summaries are in the file. |
| Hospital records (treatment timeline) | **Not in attached images** | Same as EMS: follow **subpoena returns** or defense copies of medical records for admission/triage times. |

**Integration note:** The timeline CSV rows for September 2025 are court **subpoena applications** only. They are **not** a substitute for the underlying EMS/hospital or police time logs.

---

## 2. Court & DA / plea posture (from attached court setting)

- **Next setting shown on image:** 2026-07-10 at 9:00 a.m. — purpose **final announcement**; document states it is the **sole** notice to the defendant for that appearance.  
- **Plea position stated on the same image:** State’s recommendation **12 TDC** (12 years TDC) on **guilty/true**, open through the **announcement docket**; if not accepted, offer treated as rejected once set for jury or contested revocation docket.  
- **Prosecution contact on image:** Katie Campbell (Assistant District Attorney), signed.  
- **PSI line on image:** 940-349-3195 (as printed on the form).

Add **defense and defendant contact** and any **email** references from **original PDFs in archive**, not from this scan (defense phone appears partially handwritten on the image; do not treat OCR-from-chat as a verified number for outreach).

---

## 3. Denver / Colorado: TCIC, arrest, and out-of-state criminal history

- **TCIC (Texas) vs. Colorado:** “TCIC” in Texas is the state criminal information system. **Out-of-state** Denver-area arrests or Colorado records typically appear in **CCH/rap sheet** or **NCIC** style summaries obtained via defense discovery or background vendors — **the attached docket images do not include a TCIC printout** or a Denver PD arrest file.  
- **Integration gap:** If the user’s “Denver arrest files” exist in **Archiavellian-Archive** or local intake, they were **not present in this workspace**; add them under client-controlled storage and cross-link here by **bates or filename** when indexed.

**Emails re “the mistake”:** The county portal docket (as described in the user’s second image) includes a **generic** line that an **email was sent to the attorney with a new date** (e.g. around **2025-06-17**). That is **not** the same as an email *about a mistake* in evidence. **Preserve the actual .eml or PDF** from discovery or FOI; quote them in a future appendix when available.

---

## 4. How this maps to `docket-events.csv`

Machine-readable docket lines live in `docket-events.csv` in this directory. New rows from this integration use `source_connector=denton-curated` and include the **2026-07-10** court setting and **2025-09-04 / 2025-09-11** subpoena applications. **Related cases** and **related_case_numbers** are left blank until a formal link to a Colorado or municipal matter is identified and verified.

---

## 5. Evidence still required for a complete time sequence

1. **Police / Sheriff:** Full report + CAD with **dispatch, on-scene, and clearance** times.  
2. **EMS / fire:** Krum Fire and any other EMS run sheets tied to the incident.  
3. **Hospitals:** Subpoena returns or consents for **Medical City Denton** and **THR Presby Denton** (arrival, imaging, blood draws if any).  
4. **Toxicology / lab** chain: align **draw time** with driving / crash narrative.  
5. **Colorado / Denver:** Any arrest or TCIC/rap-sheet artifacts counsel intends to use for impeachment or notice — **separate** index when files exist.

---

*Last updated 2026-04-26 (added local-disk vs. cloud workspace note and `local-paths.md.example`). Not legal advice. Verify every date and time against original certified or signed documents.*
