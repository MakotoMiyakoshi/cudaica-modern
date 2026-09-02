# Benchmark report

## Scope and method

The recorded production benchmark used a deterministic 64-channel × 180,000-
sample workload in double precision on an NVIDIA A100 80GB PCIe GPU. Reference
BLAS/LAPACK and runtime-oneMKL variants were alternated for 20 measured runs
each. The oneMKL runs used `MKL_NUM_THREADS=64`.

Captured build evidence identifies CUDA Toolkit 11.6, NVIDIA driver 550.54.14,
GCC/G++/GFortran 9.4.0, GNU Make 4.2.1, and `sm_80`. The CPU model was not
captured. The exact oneMKL version was not independently preserved in the
immutable snapshot, so no version claim is made here.

## Results

| Measurement | Reference | oneMKL runtime | Change |
| --- | ---: | ---: | ---: |
| DGEMM mean | 0.662447 s | 0.011072 s | 59.8× faster |
| Scan mean | 0.149678 s | 0.162254 s | 0.92× (slower) |
| Inversion mean | 0.028867 s | 0.041097 s | 0.70× (slower) |
| Timed region mean | 0.841071 s | 0.214512 s | 3.92× faster |
| Wall time mean | 7.150500 s | 6.055100 s | 15.3% lower (1.18×) |

The retained Stage 3 `varsort()` change reduced its separately measured region
from 7.508 s to 6.870 s, an 8.5% reduction.

Weights SHA256 was
`ed8868049452898e51572433925e29e9dedcc8462509f4ec55a0f84dbfa26e7a` and
sphere SHA256 was
`bfb99483cb6d7e775800458d6d9936218d48b0d1d5d97d7b81063825142e1c14`
for both compared variants. This establishes bitwise equality for this
workload and configuration only; it is not a universal numerical-equivalence
claim.

The large input and generated outputs are deliberately excluded from the
source release. Machine-readable summary values are in
`benchmarks/a100_64ch_180k_results.txt`.
