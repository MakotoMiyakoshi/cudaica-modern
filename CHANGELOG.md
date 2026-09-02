# Changelog

## 0.1.0 — 2026-09-02

- Published a source-only modernization based on upstream commit `7631813`.
- Replaced allocation-based GPU memory probing with `cudaMemGetInfo()`.
- Removed redundant repeated accumulation from `varsort()` by precomputing
  `backproj_power`.
- Added a deterministic 16-channel regression fixture and exact-output test.
- Added an optional oneMKL runtime launcher; oneMKL is not bundled.
- Documented provenance, licensing, benchmark evidence, and optimization scope.
- Omitted the unused, unlicensed `lib/include/mt19937.h` header.

No algorithm change, thread-block retuning, persistent oneMKL link change, or
additional CUDAICA optimization is included.
