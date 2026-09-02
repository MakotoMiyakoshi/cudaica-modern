#!/usr/bin/env python3
"""Deterministic CUDAICA v0.1.0 regression test (standard library only)."""

import argparse
import hashlib
import math
import pathlib
import shutil
import struct
import subprocess
import tempfile

CHANNELS = 16
FRAMES = 40000
EXPECTED_BYTES = CHANNELS * CHANNELS * 4
FIXTURE_SHA256 = "a76487004b105ea612707aadffbd070b0037a21be1b7b872ae803582791365c7"
EXPECTED = {
    "weights.bin": "2e68f5067d57bb1010ef47eda24689ed4399ba109706fee9f14e7044965743e6",
    "sphere.bin": "5ff106a5d72b912825012b85a2cfefbbe9bc64e3f4c0c2ccad9663a4314b8f05",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_fixture(path):
    expected_size = CHANNELS * FRAMES * 4
    if path.stat().st_size != expected_size:
        raise RuntimeError(f"fixture size is {path.stat().st_size}, expected {expected_size}")
    actual = sha256(path)
    if actual != FIXTURE_SHA256:
        raise RuntimeError(f"fixture SHA256 is {actual}, expected {FIXTURE_SHA256}")
    print(f"PASS fixture integrity: {actual}")


def check_output(path, expected_hash):
    data = path.read_bytes()
    if len(data) != EXPECTED_BYTES:
        raise RuntimeError(f"{path.name} size is {len(data)}, expected {EXPECTED_BYTES}")
    values = struct.unpack(f"={CHANNELS * CHANNELS}f", data)
    if not all(math.isfinite(value) for value in values):
        raise RuntimeError(f"{path.name} contains a non-finite value")
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected_hash:
        raise RuntimeError(f"{path.name} SHA256 is {actual}, expected {expected_hash}")
    return actual


def run_once(binary, fixture, run_dir):
    local_fixture = run_dir / "input.fdt"
    shutil.copyfile(fixture, local_fixture)
    weights = run_dir / "weights.bin"
    sphere = run_dir / "sphere.bin"
    config = run_dir / "regression.cfg"
    config.write_text(
        "\n".join(
            [
                f"DataFile {local_fixture}",
                f"chans {CHANNELS}",
                f"frames {FRAMES}",
                "epochs 1",
                f"WeightsOutFile {weights}",
                f"SphereFile {sphere}",
                "sphering on",
                "bias on",
                "extended 0",
                "pca 0",
                "seed 12345",
                "verbose off",
                "",
            ]
        ),
        encoding="utf-8",
    )
    completed = subprocess.run([str(binary), "-f", str(config)], cwd=run_dir)
    if completed.returncode != 0:
        raise RuntimeError(f"CUDAICA exited with status {completed.returncode}")
    return {name: check_output(run_dir / name, digest) for name, digest in EXPECTED.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", default="./cudaica", type=pathlib.Path)
    parser.add_argument("--verify-fixture-only", action="store_true")
    args = parser.parse_args()

    repo = pathlib.Path(__file__).resolve().parents[1]
    fixture = (repo / "tests" / "fixtures" / "input_16x40000.fdt").resolve()
    check_fixture(fixture)
    if args.verify_fixture_only:
        return

    binary = args.binary.resolve()
    if not binary.is_file():
        raise RuntimeError(f"CUDAICA binary not found: {binary}")

    with tempfile.TemporaryDirectory(prefix="cudaica-regression-") as temp:
        root = pathlib.Path(temp)
        (root / "run1").mkdir()
        (root / "run2").mkdir()
        first = run_once(binary, fixture, root / "run1")
        second = run_once(binary, fixture, root / "run2")
        if first != second:
            raise RuntimeError("repeated executions were not bitwise deterministic")
    print("PASS CUDAICA regression: outputs finite, known-good, and deterministic")


if __name__ == "__main__":
    main()
