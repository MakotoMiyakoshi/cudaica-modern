#!/bin/sh
set -eu

binary=${CUDAICA_BINARY:-./cudaica}
mkl_path=${CUDAICA_MKL_PATH:-}

if [ ! -x "$binary" ]; then
    echo "error: CUDAICA executable is not executable: $binary" >&2
    exit 2
fi

if [ -n "$mkl_path" ]; then
    if [ ! -f "$mkl_path" ] || [ ! -r "$mkl_path" ]; then
        echo "error: CUDAICA_MKL_PATH is not a readable file: $mkl_path" >&2
        exit 2
    fi
else
    if command -v ldconfig >/dev/null 2>&1; then
        mkl_path=$(ldconfig -p 2>/dev/null | awk '/libmkl_rt\.so/{print $NF; exit}')
    fi
    if [ -z "$mkl_path" ]; then
        for candidate in \
            /opt/intel/oneapi/mkl/latest/lib/intel64/libmkl_rt.so \
            /usr/local/lib/libmkl_rt.so \
            /usr/lib/x86_64-linux-gnu/libmkl_rt.so
        do
            if [ -f "$candidate" ] && [ -r "$candidate" ]; then
                mkl_path=$candidate
                break
            fi
        done
    fi
fi

if [ -n "$mkl_path" ]; then
    echo "Using local oneMKL runtime: $mkl_path" >&2
    if [ -z "${MKL_NUM_THREADS:-}" ]; then
        echo "MKL_NUM_THREADS is unset; the benchmark used 64, but no default is imposed." >&2
    fi
    LD_PRELOAD="$mkl_path${LD_PRELOAD:+:$LD_PRELOAD}"
    export LD_PRELOAD
else
    echo "oneMKL runtime not found; using the build-time BLAS/LAPACK selection." >&2
fi

exec "$binary" "$@"
