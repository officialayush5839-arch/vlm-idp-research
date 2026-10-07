import json
import hashlib
from pathlib import Path

manifest_path = Path("experiments/phase14/frozen_phase13_sha256_manifest.json")
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

files_dict = manifest["files"]
repo_root = Path(".")
mismatches = 0
checked = 0
for rel_path, expected_hash in files_dict.items():
    if rel_path.startswith(".pytest_cache"):
        continue
    p = repo_root / rel_path
    if not p.exists():
        print(f"MISSING: {rel_path}")
        mismatches += 1
        continue
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != expected_hash:
        print(f"MUTATED: {rel_path}")
        mismatches += 1
    checked += 1

print(f"Checked: {checked}/{len(manifest)} files.")
print(f"Total mismatches: {mismatches}")
if mismatches == 0:
    print("HISTORICAL IMMUTABILITY 100% VERIFIED!")
else:
    raise RuntimeError(f"Audit failed with {mismatches} mismatches!")
