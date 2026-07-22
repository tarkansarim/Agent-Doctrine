# Codex Pressure-Lab Routing

<!-- agent-doctrine-rule:routing.pressure-lab -->
- Load `pressure-lab` only for substantive agent-facing behavior that needs
  robustness or variation testing, repeated failures under realistic variation,
  or an explicit hardening request. Narrow wording, metadata, and trigger changes
  use source validation and focused tests without Pressure Lab.
