.PHONY: help install update uninstall test lint agent\:check agent-polish-gate \
	check-agent-drift check-feature-equivalence check-platform-targets \
	platform-targets-sync platform-targets-assert repo-standards-gate

help:
	@echo "install update uninstall test lint agent:check agent-polish-gate repo-standards-gate"

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

update:
	.venv/bin/pip install -U -r requirements.txt

uninstall:
	rm -rf .venv

test:
	.venv/bin/python verify_setup.py
	.venv/bin/python -m pytest tests/ -q

lint:
	.venv/bin/python -m compileall -q src scripts verify_setup.py tests

check-agent-drift:
	bash scripts/check-agent-drift.sh .

check-feature-equivalence:
	bash scripts/check-feature-equivalence.sh .

check-platform-targets:
	bash scripts/check-platform-targets.sh .

platform-targets-sync:
	bash scripts/check-platform-targets.sh . --sync

platform-targets-assert:
	bash scripts/check-platform-targets.sh . --assert-current

agent\:check: check-agent-drift check-feature-equivalence check-platform-targets

agent-polish-gate: platform-targets-sync platform-targets-assert agent\:check

repo-standards-gate: agent-polish-gate
