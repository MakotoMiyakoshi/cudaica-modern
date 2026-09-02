# CUDAICA modernized

CUDAICA is a CUDA implementation of Infomax independent component analysis
for EEG data. This `v0.1.0` modernization is a source-only release based on
upstream commit `763181395f0a4bfa79bfab3974f38eb82b1140bb`.

The release preserves the original algorithm and defaults. It contains only
two production changes: safer CUDA memory discovery with `cudaMemGetInfo()`
and an algebraically equivalent `varsort()` calculation that removes a
redundant inner loop. See [OPTIMIZATION_NOTES.md](OPTIMIZATION_NOTES.md).

## License and provenance

CUDAICA is distributed under GNU GPL version 3 or later. See [LICENSE](LICENSE),
[LICENSE_AUDIT.md](LICENSE_AUDIT.md), and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The R250 author attribution
and original EFC comments are retained.

This repository contains no Intel oneMKL binary, NVIDIA CUDA library, compiled
CUDAICA executable, object file, or large benchmark dataset. You must obtain
all build and runtime dependencies separately.

## Requirements

- Linux on x86-64
- an NVIDIA CUDA-capable GPU and compatible driver
- CUDA Toolkit with `nvcc`
- GCC/G++, GNU Fortran, Autoconf, Automake, and Make
- BLAS and LAPACK development libraries
- Python 3 for the regression harness

The preserved production build used Ubuntu 20.04 tooling, CUDA Toolkit 11.6,
GCC/G++/GFortran 9.4, and `sm_80`. Other combinations are not claimed here.

## Build

```sh
./reconf.sh
./configure --with-cuda=/usr/local/cuda --with-cuda-arch=80
make -j
```

Choose `--with-cuda-arch` for the target GPU. The configure help text lists
historical architectures, but the value is passed through to `nvcc`; `80` was
used for the verified A100 production build. Double precision is the default.

## Run

```sh
./cudaica -f your-config.txt
```

CUDAICA input is a headerless floating-point data file. A configuration names
the input, channel/frame dimensions, output weights and sphere files, and ICA
options. See `tests/run_regression.py` for a complete generated example.

To use an existing local oneMKL runtime without copying it into this project:

```sh
CUDAICA_MKL_PATH=/path/to/libmkl_rt.so \
MKL_NUM_THREADS=64 \
scripts/run_cudaica_mkl.sh -f your-config.txt
```

The launcher validates an explicit path, otherwise searches the system loader
cache and common Intel installation locations. If no oneMKL runtime is found,
it runs normally with the BLAS/LAPACK selected at build time. It never installs
or redistributes oneMKL. Thread count `64` is the documented benchmark setting,
not a launcher default.

## Regression test

After building on a CUDA-capable Linux host:

```sh
python3 tests/run_regression.py --binary ./cudaica
```

For a host without CUDA, repository/fixture integrity can still be checked:

```sh
python3 tests/run_regression.py --verify-fixture-only
```

## Benchmark summary

On the recorded A100 workload (64 channels × 180,000 samples, double
precision), Stage 3 reduced its isolated region from 7.508 s to 6.870 s
(8.5%). Runtime oneMKL substitution reduced mean wall time from 7.1505 s to
6.0551 s (15.3%, 1.18×). Outputs were bitwise identical in the captured runs.
Full conditions and limitations are in [BENCHMARKS.md](BENCHMARKS.md).

## Citation

Please cite the original CUDAICA paper listed in [CITATION.cff](CITATION.cff):
Raimondo et al., “CUDAICA: GPU Optimization of Infomax-ICA EEG Analysis”
(2012), DOI `10.1155/2012/206972`.
