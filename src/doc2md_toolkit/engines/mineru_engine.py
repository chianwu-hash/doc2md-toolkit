from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def convert(src: Path, output_dir: Path, *, backend: str = "pipeline") -> Path:
    mineru = shutil.which("mineru")
    if mineru is None:
        raise RuntimeError('MinerU is not installed. Install with `pip install "mineru[all]"` in a suitable environment.')

    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [mineru, "-p", str(src), "-o", str(output_dir), "-b", backend]
    subprocess.run(cmd, check=True)
    return output_dir
