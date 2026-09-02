# Source-only distribution audit

Audit date: 2026-09-02  
Result: PASS

The proposed `v0.1.0` Git tree was recursively reviewed for third-party and
binary material. It contains source, scripts, documentation, exact source
patches, and one small deterministic regression input.

## Included intentionally

- CUDAICA C/CUDA, MATLAB, and Python source from the identified upstream Git
  history, under the root GPL license.
- Carter R250 C source and headers with original EFC markers and attribution.
- The two retained modernization changes and their patches.
- A 2,560,000-byte synthetic float32 regression fixture.

## Excluded

- Intel oneMKL libraries and all other Intel binaries.
- NVIDIA CUDA Toolkit libraries, headers, drivers, and redistributables.
- compiled CUDAICA executables, objects, archives, and generated build output.
- large benchmark datasets and generated benchmark outputs.
- unlicensed, unused `lib/include/mt19937.h`.
- secrets, tokens, credentials, email messages, and private provenance records.
- rejected optimization experiments and profiling artifacts.

The optional oneMKL launcher only locates a user-supplied local runtime; it
does not download, copy, install, or redistribute one.
