# Optimization notes

This release intentionally contains exactly two retained production source
changes relative to upstream commit `7631813`.

## Stage 1: CUDA memory discovery

`src/device.cu` now obtains current free and total device memory directly with
`cudaMemGetInfo()`. It removes the former `cudaMallocPitch()` binary-search
probe, which repeatedly allocated and freed memory to estimate availability.
The existing reserved-memory margin remains applied by `getFreeMem()`.

Exact change: [patches/stage1_memory_probe.patch](patches/stage1_memory_probe.patch).

## Stage 3: `varsort()` redundant work removal

In `src/postprocess.cu`, the sum of squared inverse-weight elements for one
component does not depend on sample index. The release computes that value
once as `backproj_power`, then multiplies it by each squared activation. This
is algebraically equivalent to the prior inner-loop calculation.

Exact change: [patches/stage3_varsort.patch](patches/stage3_varsort.patch).

## Explicitly unchanged or excluded

- `MAX_MULTIPROCESSORS` remains `32`.
- `gpu.nthreads` remains `8` for devices outside the legacy compute-2 branch.
- `DEFAULT_POSACT` remains `1`.
- The rejected 108-SM retuning is excluded.
- Experimental `geproj_gpu` work and profiling instrumentation are excluded.
- Later Stage 5B/5C source changes are excluded.
- oneMKL use is optional runtime configuration, not a source optimization.

No further CUDAICA optimization was performed for this release.
