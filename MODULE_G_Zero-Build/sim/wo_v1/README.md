README.md

# MODULE G — Zero-Build WORK_ORDER_v1 Reference Implementation
**Status:** Pre-registered operational specification (30 August 2026)  
**Parent:** [LifeNode777/PHASE_1](https://github.com/LifeNode777/PHASE_1)  
**License:** CC-BY-NC-SA 4.0
This directory contains a clean, pinned Python implementation of the LN-EPS pipeline (steps 1–7) exactly as specified in `docs/WORK_ORDER_v1.md` §§4–5.
## Quick start
```bash
cd sim/wo_v1
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Single record (fast test)
python scripts/pipeline.py --db mitdb --record 100 --max-windows 8 --no-nulls
# First 10 mitdb records (TIER-1 subset)
python scripts/pipeline.py --cohort --max-windows 12
