#!/usr/bin/env python3
import sys, platform, hashlib, subprocess
from pathlib import Path
from datetime import datetime

TRACES = {
    "trace_sanity.txt": "1\n2\n3\n2\n4\n1\n",
    "trace_hits.txt": "1\n2\n3\n1\n2\n3\n",
    "trace_evictions.txt": "1\n2\n3\n4\n5\n6\n",
    "trace_repeat.txt": "1\n1\n1\n2\n2\n3\n3\n",
    "trace_comments.txt": "# this is a comment\n1\n\n2\n# another comment\n3\n2\n",
    "trace_single_frame.txt": "1\n2\n1\n2\n1\n",
}

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def run_case(py, memsim, trace):
    proc = subprocess.run([py, str(memsim)], input=trace, text=True, capture_output=True)
    return proc.returncode, proc.stdout, proc.stderr

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 generate_test_report.py /path/to/memsim.py", file=sys.stderr); sys.exit(2)
    memsim = Path(sys.argv[1]).resolve()
    if not memsim.exists():
        print(f"Error: {memsim} not found", file=sys.stderr); sys.exit(2)
    out_dir = Path.cwd()
    traces_dir = out_dir / "traces"; traces_dir.mkdir(exist_ok=True)
    for name, content in TRACES.items():
        (traces_dir / name).write_text(content, encoding="utf-8")
    py = sys.executable or "python3"
    env = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "platform": platform.platform(),
        "python": sys.version.replace("\\n", " "),
        "python_exe": py,
        "memsim": str(memsim),
        "sha256": sha256_file(memsim),
    }
    md = []
    md.append(f"# Test Report – memsim.py\n\n")
    md.append(f"**Generated:** {env['timestamp']}\n\n")
    md.append(f"**Platform:** {env['platform']}\n\n")
    md.append(f"**Python:** {env['python']}\n\n")
    md.append(f"**Python Executable:** {env['python_exe']}\n\n")
    md.append(f"**memsim.py:** `{env['memsim']}`\n\n")
    md.append(f"**SHA256(memsim.py):** `{env['sha256']}`\n\n---\n\n")
    results = []
    for name in TRACES:
        trace_path = traces_dir / name
        rc, out, err = run_case(py, memsim, trace_path.read_text(encoding="utf-8"))
        md.append(f"## Case: {name}\n\n")
        md.append(f"**Command:** `python3 memsim.py < {name}`\n\n")
        md.append(f"**Trace (`traces/{name}`)**\n\n```\n{TRACES[name].strip()}\n```\n\n")
        md.append("**Observed Output**\n\n```\n" + (out.strip()) + "\n```\n")
        if err.strip():
            md.append("\n**stderr (if any)**\n\n```\n" + err.strip() + "\n```\n")
        md.append("\n---\n\n")
    (out_dir / "Test_Report.md").write_text("".join(md), encoding="utf-8")
    print("Wrote Test_Report.md and traces/")

if __name__ == "__main__":
    main()
