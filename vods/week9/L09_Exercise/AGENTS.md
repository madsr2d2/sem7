# Repository Guidelines

## Project Structure & Module Organization
Core RTL lives in `marb/src/rtl`, `sat_filter/src/rtl`, and `summer/src/rtl`, each mirroring a matching cocotb/pyuvm testbench under `*/src/tb`. Testbench packages include UVCs, virtual sequencers, reference models, and scenario tests inside `tests/`. Support tooling is in `bin/` (Python requirements, helper scripts) and `client_setup/` (Docker & WSL bootstrap). Exercises and walkthrough material used in training sessions remain in `exercises/`; keep course artifacts separate from deliverable RTL. Place new IP blocks under `<block>/src/rtl` with a sibling `tb/` to stay aligned with the existing layout.

## Environment Setup
Use Python 3.10+ and a virtual environment to isolate simulator dependencies:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r bin/requirements.txt
```
On a fresh machine, run `client_setup/scripts/setup_wsl.sh` or `setup_docker.sh` to provision Icarus Verilog, GCC, and GTKWave.

## Build, Test, and Development Commands
- `cd marb/src/tb && make SIM=icarus MODULE=tests.cl_marb_basic_test`: compile RTL and execute the MARB smoke test.
- `cd sat_filter/src/tb && make SIM=icarus MODULE=tests.test_sat_filter_default_seq`: exercise the SAT filter default sequence.
- `cd summer/src/tb && make SIM=icarus MODULE=tests.summer_tb_test_1`: run the summer block regression.
- `make coverage` (from any `*/src/tb`): merge UCIS XML, invoke `pyucis-viewer`, and inspect functional coverage.
- `make clean` (from any `*/src/tb`): purge build artifacts, ref-model objects, and `__pycache__`.

## Coding Style & Naming Conventions
SystemVerilog files adhere to two-space indentation, aligned port lists, uppercase parameter names, and `logic` declarations for synthesizable regs. Keep block-level packages in `pkg_<block>_types.sv`. Python testbench code follows PEP8: four-space indentation, snake_case functions, and class prefixes such as `cl_` for components or UVM agents. Prefer `pytest --maxfail=1` or targeted make runs before committing Python tweaks; use `black` for larger script refactors when style drifts.

## Testing Guidelines
Scenario tests reside under `*/src/tb/tests`. Name new modules `tests.<block>_<scenario>_test` so they can be referenced via the `MODULE` make variable. Keep scoreboard updates and coverage bins synchronized with reference models in `tb/ref_model`. Capture new coverage goals using `pyvsc` sequences and validate with `make coverage`; investigate gaps via `merge_cov.xml` inside `sim_build/`.

## Commit & Pull Request Guidelines
Use short, present-tense commit summaries (e.g., `add marb dynamic priority test`) and include the affected block prefix. For pull requests, provide: scope summary, simulator logs (`results.xml` snippets or coverage deltas), linked exercise or issue IDs, and screenshots when GTKWave traces help reviewers. Ensure CI or local `make` runs succeed before requesting review; flag any required environment steps in the PR description.
