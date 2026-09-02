# CUDAICA Modernization License and Provenance Audit

Audit date: 2026-08-28; permission update: 2026-09-02  
Release candidate: `v0.1.0` (source only)  
Audit result: **PASS — NO UNRESOLVED BLOCKING ISSUE**

This audit applies to the verified production snapshot whose archive SHA256 is
`8d8054db374051a8a8c1aa4f90d6f254f3158887c53bc776a3ea48bfe0d313df`.
The archive contains Git commit
`763181395f0a4bfa79bfab3974f38eb82b1140bb` plus uncommitted production
changes and build/test artifacts. All 181 regular files extracted on the audit
host matched `production-tree.before.sha256`; the before and after manifests
were byte-identical.

This document records source and license evidence. It is not a substitute for
legal advice.

## CONFIRMED

### Upstream identity and history

- The snapshot's `.git/config` identifies
  <https://github.com/fraimondo/cudaica> as `origin`.
- `HEAD`, local `master`, `origin/master`, and `origin/HEAD` all resolve in the
  snapshot to commit
  [`763181395f0a4bfa79bfab3974f38eb82b1140bb`](https://github.com/fraimondo/cudaica/commit/763181395f0a4bfa79bfab3974f38eb82b1140bb),
  authored by Fede Raimondo. There are no tags in the captured repository.
- The captured history begins with an initial commit followed by commit
  `73829e557bed4084b3f35898572a6bb8b806ada8`, whose message is `Import from SVN`.
  The snapshot does not contain the prior SVN metadata or an SVN source URL.
- The upstream README identifies the work as CUDAICA, an implementation of
  Infomax ICA on CUDA, and cites Raimondo, Kamienkowski, Sigman, and Fernandez
  Slezak, “CUDAICA: GPU Optimization of Infomax-ICA EEG Analysis” (2012).

### Main CUDAICA license

- The repository-root `LICENSE` is the unmodified GNU General Public License,
  version 3. The authoritative license text is published by the
  [Free Software Foundation](https://www.gnu.org/licenses/gpl-3.0.html).
- `cudaica.c`, the principal `src/*.cu` implementation files, and the principal
  `include/*.h` headers carry Federico Raimondo's 2011 copyright notice and an
  explicit grant under **GPL version 3 or any later version**.
- The retained Stage 1 and Stage 3 changes are modifications of those
  GPL-3.0-or-later files. A redistributable version would have to preserve the
  notices, remain GPL-3.0-or-later, provide complete corresponding source, and
  prominently identify modified files as required by GPLv3.
- `matlab/cudaica.m` carries Scott Makeig's 2000 copyright notice and an
  explicit **GPL version 2 or any later version** grant. That option permits its
  distribution under GPLv3 with the rest of this work.
- The bundled Autoconf Archive `AX_BLAS` and `AX_LAPACK` macros include their
  own GPLv3-or-later notices and the standard generated-configure-script
  exception.

### Exact production source changes relative to captured upstream Git

Ignoring Windows line-ending and executable-mode presentation, the production
source differs from commit `7631813` in two implementation files:

- `src/device.cu`: Stage 1 replaces allocation-based free-memory probing with
  `cudaMemGetInfo()`-based reporting.
- `src/postprocess.cu`: Stage 3 precomputes `backproj_power` in `varsort()`.

The captured production source retains `DEFAULT_POSACT=1`, the legacy
`MAX_MULTIPROCESSORS` behavior, and `gpu.nthreads=8` for non-compute-capability-2
devices. Rejected Stage 2, `geproj_gpu`, Stage 4 profiling, and later experiment
files exist only as untracked production artifacts; they are not part of the
two retained production source changes.

### Carter/Taygeta R250 C implementation — resolved

**Author:** Everett F. “Skip” Carter Jr.

**Covered files:**

- `lib/r250/r250.c`
- `lib/r250/randlcg.c`
- `lib/include/r250.h`
- `lib/include/randlcg.h`

Phase 1B recovered both original Carter/Taygeta distribution formats directly
from the exact FTP links on Taygeta's official R250 page. Three CUDAICA files
are byte-identical to that payload. `randlcg.c` differs only by renaming the
private identifier `remainder` to `remain` at its declaration and one use.
The forensic comparison is recorded in the private release working record.

Written permission was obtained directly from Carter on 2026-09-01 and
clarified on 2026-09-02 in direct response to a request covering modification,
redistribution of modified versions, GPL-3.0-or-later inclusion, and retained
attribution. The combined permission covers:

- use;
- distribution;
- modification;
- redistribution of modified versions; and
- inclusion in GPL-3.0-or-later software.

Carter attribution and the original EFC/source comments must be retained. The
private permission transcript is stored outside the proposed public tree at
`cudaica-release-private-provenance-20260902/efc-r250-permission/` and has
SHA256 `f3c7dc9282a22ac25d14b9de0c66f072748e13c7c5bcc01418caac4f2e366adc`.
No original `.eml` or `.msg` files were available locally, so the preserved
record is explicitly identified as a recipient-supplied transcript rather
than an original message with transport headers.

### BLAS and LAPACK build evidence

- Captured `config.log`, `config.status`, and `Makefile` show the production
  build selected `BLAS_LIBS='-lblas'` and `LAPACK_LIBS='-llapack'` dynamically.
- The captured configuration does not embed or copy BLAS/LAPACK source or
  binaries into CUDAICA.
- Netlib states that its reference LAPACK distribution uses the modified BSD
  license; see the authoritative
  [Netlib LAPACK licensing page](https://www.netlib.org/lapack/).
- The exact shared-library provider selected by the production machine's
  generic `libblas.so`/`liblapack.so` links is not recorded in the snapshot.
  Therefore this audit does not authorize redistributing a linked executable.

### NVIDIA CUDA relationship

- Captured build records show CUDA Toolkit 11.6, `nvcc`, compute capability
  `sm_80`, and includes/libraries referenced from `/usr/local/cuda`.
- No NVIDIA header, CUDA library, driver, or other CUDA Toolkit file is needed
  in a source-only repository; users would obtain the toolkit separately.
- NVIDIA's authoritative
  [CUDA 11.6 documentation](https://docs.nvidia.com/cuda/archive/11.6.1/)
  and
  [CUDA 11.6 EULA](https://docs.nvidia.com/cuda/archive/11.6.1/pdf/EULA.pdf)
  govern the separately installed toolkit and any CUDA component
  redistribution. This audit intentionally authorizes **no CUDA component
  redistribution**.
- The FSF explains that GPL obligations for static and dynamic linking are the
  same and discusses the System Library exception and GPL-incompatible
  libraries in its authoritative
  [GNU license FAQ](https://www.gnu.org/licenses/gpl-faq.html).

### Intel oneMKL relationship

- Stage 5A is runtime configuration through `LD_PRELOAD`; it is not a CUDAICA
  source optimization.
- No oneMKL header, object, static library, shared library, or copied runtime is
  required in the source-only repository.
- Intel states that oneMKL is licensed under the
  [Intel Simplified Software License](https://www.intel.com/content/www/us/en/content-details/749362/intel-simplified-software-license-version-october-2022.html);
  Intel's
  [oneMKL license FAQ](https://www.intel.com/content/www/us/en/developer/articles/tool/onemkl-license-faq.html)
  also directs users to that license for controlling terms.
- Even though Intel documents redistribution rights, this release plan does
  not rely on them: users must supply their own oneMKL installation and set a
  runtime path locally.

## NOT APPLICABLE

- Redistribution of `/opt/anaconda3/lib/libmkl_rt.so.2` or any other Intel
  binary: **not applicable; explicitly excluded**.
- Redistribution of CUDA Toolkit or NVIDIA driver files: **not applicable;
  explicitly excluded**.
- Redistribution of the captured `cudaica`, `a.out`, static archives, object
  files, or experimental binaries: **not applicable; the planned release is
  source only**.
- Redistribution of the 64-channel × 180,000-sample input or other large
  benchmark fixtures: **not applicable; explicitly excluded**.
- A license conclusion for a conveyed dynamically linked CUDAICA executable:
  **not applicable to v0.1.0**, because no executable may be conveyed under
  this plan.

## UNCERTAIN

- The exact implementation selected by the production machine's generic
  `-lblas` and `-llapack` links is not preserved in the snapshot. The captured
  records are consistent with a system reference BLAS/LAPACK installation, but
  that identity cannot be established from this primary evidence alone.
  Source-only redistribution does not convey those libraries.
- `src/config.cu`, `python/bindings.c`, `python/setup.py`, and two local CUDA
  Autoconf macros lack per-file license headers. They have no separate
  third-party attribution marker and are contained in the upstream repository
  distributed with the root GPLv3 license, so the root grant is the best
  primary evidence for them. This is recorded as an uncertainty rather than a
  separate blocker.
- `lib/include/mt19937.h` lacks a license header and is not referenced by the
  captured build. It must be omitted from the source-only distribution unless
  separate primary license evidence is established.
- The 2026 modernization changes are attributed to Makoto Miyakoshi in release
  metadata without displacing original CUDAICA authorship.

## BLOCKING

None.

## Decision

Phase 1 **passes**. The Carter/Taygeta R250 issue is **CONFIRMED / RESOLVED**,
and the complete audit contains no other unresolved BLOCKING issue. Release
work may proceed to Phase 2 subject to the source-only exclusions and notice
requirements documented above.
