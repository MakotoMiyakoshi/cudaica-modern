# Pre-publication audit

Audit date: 2026-09-02  
Candidate: `v0.1.0`  
Result: PASS FOR SOURCE PUBLICATION

## Provenance and licensing

- `LICENSE_AUDIT.md` has no unresolved `BLOCKING` item.
- Carter's written R250 permission is recorded as confirmed/resolved; the
  public notice retains attribution without personal signature details.
- Original EFC markers remain in `r250.c`, `randlcg.c`, and `randlcg.h`.
- The private permission transcript is outside this Git tree and its SHA256 is
  `f3c7dc9282a22ac25d14b9de0c66f072748e13c7c5bcc01418caac4f2e366adc`.

## Optimization scope

- Release `src/device.cu` and `src/postprocess.cu` are byte-identical to the
  corresponding files extracted from the verified production archive.
- Reverse application checks pass for both patches in `patches/`.
- `MAX_MULTIPROCESSORS=32`, `gpu.nthreads=8` outside the legacy compute-2
  branch, and `DEFAULT_POSACT=1` are preserved.
- No rejected 108-SM, `geproj_gpu`, profiling, or later-stage optimization is
  present.

## Distribution contents

- Recursive extension and file-magic scans found no executable, object,
  archive, shared library, compressed archive, CUDA binary, or generated
  benchmark output in the candidate tree.
- The only non-text payload is the documented 2,560,000-byte synthetic
  regression fixture.
- Secret-pattern and unnecessary Carter personal-information scans returned no
  finding.
- No Intel oneMKL binary, CUDA library/toolkit file, or prebuilt CUDAICA
  executable is included.

## Checks performed on the packaging host

- Regression fixture size and SHA256: PASS.
- Python regression harness compilation: PASS.
- POSIX shell syntax for the optional oneMKL launcher: PASS.
- Git whitespace/error check: PASS.
- Known-good production regression outputs are encoded as exact SHA256 values
  in the harness; the preserved production runs produced those values
  repeatedly for both weights and sphere matrices.

The packaging host is Windows and lacks the Linux Autotools/GCC/GFortran/BLAS
build stack, so the candidate executable was not rebuilt locally. A clean
Ubuntu/CUDA compilation is defined in `.github/workflows/ci.yml`; fresh-clone
build status and GPU-runtime validation are reported separately after
publication. This limitation does not change the source-only license decision.
