# AI-Based Emotional Support Conversation System: Project Baseline Report

**Document:** Baseline Audit and System Assessment  
**Project Category:** Research-Oriented B.Tech Major Project (Batch ID: CSM-B4)  
**Base Paper:** *ESC-Skills: Discovering and Self-Evolving Skills for Emotional Support Conversations*  
**Date of Audit:** October 29, 2026  
**Auditor / Role:** Senior Research & Python Engineering Assistant (Antigravity Agent Mode)  

---

## 1. Executive Summary

A comprehensive, read-only Phase 0 audit was conducted across local storage, Git repositories, directory structures, Python runtime environments, installed dependencies, processed datasets, model caches, and existing uncommitted work.

The project repository was located at:
`E:\C DATA\Documents\Projects\AI-Based-Emotional-Support-Conversation-System`

The repository is connected to the official guide-owned remote repository:
`https://github.com/bvreddymtech/AI-Based-Emotional-Support-Conversation-System.git`

The current branch is `main`, perfectly synchronized with `origin/main` at commit `edb19b8` ("Add ESConv dataset analysis script"). Crucially, the local workspace contains valuable uncommitted and untracked code and data files that must be strictly preserved.

---

## 2. Git Status and Repository Provenance

- **Repository Path:** `E:\C DATA\Documents\Projects\AI-Based-Emotional-Support-Conversation-System`
- **Remote Origin URL:** `https://github.com/bvreddymtech/AI-Based-Emotional-Support-Conversation-System.git`
- **Current Branch:** `main` (tracking `origin/main`, up to date)
- **Latest Commit:** `edb19b8536927a66a57a361e26a65862e70c89da`
- **Commit History Summary (14 commits total):**
  1. `edb19b8` - Add ESConv dataset analysis script
  2. `118d867` - Ignore local dataset files
  3. `5c4e136` - Add ESConv preprocessing script
  4. `cde9fdd` - Add dataset processing dependencies
  5. `ee5c762` - Update project dependencies
  6. `a955042` - Add machine learning dependencies
  7. `e6765c7` - Update project dependencies
  8. `435d880` - Add initial Python package structure
  9. `245529f` - Add Python requirements file
  10. `003936e` - Add gitignore for Python environment and secrets
  11. `6392b51` - Add project abstract for AI emotional support system
  12. `fb4c0d2` - Update README with project plan
  13. `e6e19bf` - Create ABSTRACT.md
  14. `a726502` - Initial commit
- **Git User Identity Config:**
  - `git config user.name`: Not configured locally or globally on this machine.
  - Earlier commits authored by: `Maheejachowdary <maheejasrinivas@gmail.com>`.
- **Untracked Local Files:**
  - `outputs/` (contains `outputs/backup_package_inventory.txt`)
  - `src/intervention_units/analyze_intervention_units.py`
  - `src/intervention_units/build_intervention_units.py`
  - `src/intervention_units/inspect_annotation_sample.py`
  - `src/intervention_units/inspect_response_changes.py`

---

## 3. What Exists in the Workspace

### 3.1 Project Files and Documentation
- `README.md` (23.8 KB): Detailed project documentation, problem statement, research methodology, architecture overview, and phased development roadmap.
- `ABSTRACT.md` (2.7 KB): Formal research abstract outlining the scope (non-clinical emotional support), dataset (ESConv), and evaluation objectives.
- `requirements.txt` (2.2 KB): Pinned Python package dependencies (encoded in UTF-16LE).
- `.gitignore`: Excludes `.venv/`, `__pycache__/`, `*.py[cod]`, `.env`, `data/raw/`, `data/processed/`.

### 3.2 Source Code Modules (`src/`)
- `src/__init__.py`: Package root.
- `src/data/`:
  - `preprocess_esconv.py`: Downloads `thu-coai/esconv` from Hugging Face Hub, parses JSON dialogue records, normalizes conversation fields, and writes train/validation/test JSONL files.
  - `analyze_esconv.py`: Analyzes distributions of emotions, problem types, experience types, supporter strategies, and dialogue lengths.
  - `__init__.py`
- `src/intervention_units/` (Local / Untracked):
  - `build_intervention_units.py`: Extracts contextual triads `(previous_user_text, supporter_text [with strategy], next_user_text)` from dialogue turns.
  - `analyze_intervention_units.py`: Computes statistical distributions and co-occurrences of strategies, emotions, and problems across extracted intervention units.
  - `inspect_annotation_sample.py`: Generates formatted text reports with manual annotation templates from sampled units.
  - `inspect_response_changes.py`: Draws reproducible random samples of intervention units to inspect conversational progressions.
  - `__init__.py`
- `src/skill_bank/__init__.py`: Stub/empty module.
- `src/retrieval/__init__.py`: Stub/empty module.
- `src/generation/__init__.py`: Stub/empty module.
- `src/evaluation/__init__.py`: Stub/empty module.
- `src/refinement/__init__.py`: Stub/empty module.

### 3.3 Test Suite (`tests/`)
- `tests/__init__.py`: Empty file (no automated tests currently exist in the repository).

### 3.4 Data Directory (`data/`)
- `data/raw/`: Empty directory.
- `data/processed/`: Contains preprocessed and generated files (ignored by `.gitignore` to avoid pushing large data to GitHub):
  - `esconv_train.jsonl` (4,067,206 bytes, 910 conversations)
  - `esconv_validation.jsonl` (872,775 bytes, 195 conversations)
  - `esconv_test.jsonl` (887,533 bytes, 195 conversations)
  - `intervention_units_train.jsonl` (7,874,620 bytes, 11,500 units)
  - `intervention_units_validation.jsonl` (1,714,898 bytes, 2,519 units)
  - `intervention_units_test.jsonl` (1,744,456 bytes, 2,674 units)
  - `annotation_sample_100.jsonl` (69,443 bytes, 100 pilot records)
  - `annotation_sample_100_inspection.txt` (131,541 bytes, inspection report and manual annotation templates)

### 3.5 Virtual Environments and Backups
- `.venv/`: Active virtual environment with Python 3.14.0.
- `.venv_backup/`: Secondary backup virtual environment.
- `outputs/backup_package_inventory.txt`: Text inventory of installed packages.

---

## 4. Verification: What Works vs. What Has Not Been Tested

### 4.1 Verified Working (Tested During Audit)
1. **Python Environment & ML Imports:**
   - Python version: 3.14.0 (Windows x64)
   - Verified successful runtime import of:
     - `torch` (2.14.0+cpu)
     - `transformers` (5.17.0)
     - `sentence_transformers` (6.0.1)
     - `datasets` (5.0.1)
     - `scikit-learn` (1.9.1)
     - `pandas` (3.0.5)
2. **ESConv Dataset Analysis Script (`src/data/analyze_esconv.py`):**
   - Successfully executed against `data/processed/esconv_*.jsonl`.
   - Verified statistics:
     - Train: 910 conversations, 26,648 turns (avg 29.28 turns/conv)
     - Validation: 195 conversations, 5,678 turns (avg 29.12 turns/conv)
     - Test: 195 conversations, 6,039 turns (avg 30.97 turns/conv)
     - Total: 1,300 conversations, 38,365 turns
     - Top emotions: anxiety (354), depression (334), sadness (308), anger (111), fear (95)
     - Top strategies: Question (3,801), Others (3,341), Providing Suggestions (2,954), Affirmation and Reassurance (2,827)
3. **Intervention Unit Analysis Script (`src/intervention_units/analyze_intervention_units.py`):**
   - Successfully executed against `data/processed/intervention_units_*.jsonl`.
   - Verified extracted units:
     - Train: 11,500 units from 910 conversations
     - Validation: 2,519 units from 195 conversations
     - Test: 2,674 units from 195 conversations
     - Total: 16,693 intervention units
4. **Git Repository Connectivity:**
   - Git remote verified as `https://github.com/bvreddymtech/AI-Based-Emotional-Support-Conversation-System.git`.
   - Branch status clean relative to remote head (`origin/main`).

### 4.2 Not Yet Tested / Needs Live Verification
1. **Live Preprocessing Execution (`src/data/preprocess_esconv.py`):**
   - The script was inspected, but live downloading from Hugging Face Hub was not re-run during Phase 0 to preserve existing processed files and avoid unneeded network usage.
2. **Intervention Unit Extraction Script Execution (`src/intervention_units/build_intervention_units.py`):**
   - The script code was inspected and validated against output data schemas, but not re-run to avoid mutating the existing generated `.jsonl` files.
3. **Pilot Sample Scripts (`inspect_annotation_sample.py` and `inspect_response_changes.py`):**
   - Inspected, verified against outputs, but not re-executed.

---

## 5. Dataset and Annotation Status

- **100-Record Annotation Pilot (`data/processed/annotation_sample_100.jsonl`):**
  - Total records: 100
  - Current Status: All 100 records have `annotation_status: "pending"` (0 / 100 records annotated).
  - Inspection Document: `data/processed/annotation_sample_100_inspection.txt` has templates ready for:
    - Pre-Seeker State
    - Fine-Grained Support Action
    - Response Change
    - Change Direction (positive / neutral / negative / indeterminable)
    - Post-Seeker State
    - Annotation Notes
- **Data Splitting & Leakage Prevention:**
  - Train (910 conversations), Validation (195), and Test (195) splits are strictly isolated in separate files.
  - All skill construction, pattern mining, and tuning must strictly use the **Train** split only (`esconv_train.jsonl` and `intervention_units_train.jsonl`), preserving Validation and Test for unbiased evaluation.

---

## 6. What is Incomplete or Missing

1. **Automated Test Suite:**
   - `tests/` contains only an empty `__init__.py`.
   - Need unit tests for data preprocessing schemas, record validation, intervention unit structure, and split isolation.
2. **Skill Bank Pipeline (Phases 6–7):**
   - Pattern mining module (`src/pattern_mining/`) does not exist.
   - Skill Bank construction and schema validation (`src/skill_bank/`) are unimplemented.
3. **Retrieval Pipeline (Phase 8):**
   - `src/retrieval/` contains only `__init__.py`.
4. **Generation Pipeline (Phase 9):**
   - `src/generation/` contains only `__init__.py`.
   - Experimental baselines (E1 direct LLM, E2 strategy-aware, E3 skill-guided, E4 oracle strategy) are not implemented.
5. **Research Evaluation Pipeline (Phase 10):**
   - `src/evaluation/` contains only `__init__.py`.
   - Automated metrics (BLEU, ROUGE, BERTScore, strategy alignment) and human-evaluation rubrics are unimplemented.
6. **Application (Phase 12):**
   - No backend API (`src/api/` or FastAPI app).
   - No frontend interface (`frontend/`).
7. **Documentation & Process Records:**
   - `docs/DAILY_PROGRESS.md` is not yet created.
   - `docs/DATASET_CARD.md`, `docs/ANNOTATION_GUIDELINES.md`, `docs/EXPERIMENT_PROTOCOL.md` are not yet created.
8. **Git Configuration:**
   - Local `user.name` and `user.email` are not configured in Git.

---

## 7. Critical Files and Data That Must Be Preserved

1. **Uncommitted Local Scripts:**
   - `src/intervention_units/build_intervention_units.py`
   - `src/intervention_units/analyze_intervention_units.py`
   - `src/intervention_units/inspect_annotation_sample.py`
   - `src/intervention_units/inspect_response_changes.py`
2. **Local Processed Datasets in `data/processed/`:**
   - `esconv_train.jsonl`, `esconv_validation.jsonl`, `esconv_test.jsonl`
   - `intervention_units_train.jsonl`, `intervention_units_validation.jsonl`, `intervention_units_test.jsonl`
   - `annotation_sample_100.jsonl`, `annotation_sample_100_inspection.txt`
3. **Environment & Records:**
   - `.venv/` and `.venv_backup/` (contains pre-installed PyTorch and ML packages)
   - `outputs/backup_package_inventory.txt`
   - Existing Git commit history (do not rebase, squash, or force-push).

---

## 8. Environment and Dependency Assessment

- **Hardware:** Dell laptop, Windows 11 64-bit, 16 GB RAM.
- **Storage:**
  - Drive C: 117.1 GB free
  - Drive D: 341.5 GB free
  - Drive E: 362.8 GB free (Repository resides here)
- **Runtime Assessment:**
  - Installed Python: 3.14.0.
  - While Python 3.14 is a very modern release, PyTorch 2.14.0+cpu and Transformers 5.17.0 are verified to import and run cleanly in the current `.venv`.
  - Cold imports of large packages take 20–30 seconds on CPU without SSD caching; runtime scripts should avoid repeated top-level heavy imports where unnecessary.
  - `requirements.txt` is encoded in UTF-16LE, which causes some text-based tools to flag it as binary. Converting it to UTF-8 without BOM will ensure cross-platform reproducibility while preserving exact pinned versions.

---

## 9. Safe Strategy for GitHub Remote and Commits

1. **Preserve Repository Integrity:**
   - Do NOT run `git reset --hard`, `git clean`, `git rebase`, or force-push (`--force`).
   - The remote repository is owned by the project guide (`bvreddymtech`). All commits must be cleanly additive.
2. **Configure Git Identity:**
   - Explicitly configure local `user.name` and `user.email` matching the project author (`Maheejachowdary` / `maheejasrinivas@gmail.com` or user-specified) before committing.
3. **Granular, Validated Commits:**
   - Group logically related files into clear, conventional commit messages (e.g. `feat(intervention_units): ...`, `docs: ...`, `test: ...`).
   - Run tests and inspect diffs prior to every commit.
4. **Push Workflow:**
   - Pull with `--ff-only` before pushing if remote changes occur.
   - Push to `origin main` only after verification and user consent.

---

## 10. Prioritized Development Checklist

- [x] **Phase 0:** Read-only audit and baseline report (`docs/PROJECT_BASELINE.md`).
- [ ] **Phase 1:** Environment standardization (`.gitignore` update, `.env.example`, UTF-8 `requirements.txt`, directory alignment).
- [ ] **Phase 2:** Initialize `docs/DAILY_PROGRESS.md` and log Phase 0/1 progress.
- [ ] **Phase 3:** Stage, verify, and commit existing untracked intervention unit scripts.
- [ ] **Phase 4:** Dataset validation suite (`tests/test_esconv_data.py`), `docs/DATASET_CARD.md`.
- [ ] **Phase 5:** Formalize `docs/ANNOTATION_GUIDELINES.md`, validate intervention unit schemas, and establish annotation pipeline for the 100-record pilot.
- [ ] **Phase 6:** Implement intervention pattern mining module (`src/pattern_mining/`).
- [ ] **Phase 7:** Construct and validate Emotional Support Skill Bank (`src/skill_bank/`).
- [ ] **Phase 8:** Implement context- and state-aware Skill Retrieval (`src/retrieval/`).
- [ ] **Phase 9:** Implement generation pipeline (E1 Direct LLM, E2 Strategy-Aware, E3 Skill-Guided, E4 Oracle).
- [ ] **Phase 10:** Research evaluation pipeline (automatic metrics & qualitative protocol).
- [ ] **Phase 11:** Error analysis and iterative skill refinement.
- [ ] **Phase 12:** Build FastAPI backend and research demonstration frontend.
- [ ] **Phase 13:** Comprehensive testing, final report, paper draft, and viva documentation.

