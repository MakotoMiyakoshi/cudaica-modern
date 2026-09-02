# Regression test

`input_16x40000.fdt` is a deterministic synthetic, headerless float32 fixture:
16 channels × 40,000 frames (2,560,000 bytes). It contains no human-subject
data. Its SHA256 is
`a76487004b105ea612707aadffbd070b0037a21be1b7b872ae803582791365c7`.

Run the full test on a CUDA-capable Linux build host:

```sh
python3 tests/run_regression.py --binary ./cudaica
```

The harness performs two isolated executions, requires successful exit,
requires 16×16 float32 weights and sphere outputs, checks every value is
finite, checks exact known-good SHA256 digests, and confirms both runs are
bitwise deterministic.

On a host without a CUDA build/runtime:

```sh
python3 tests/run_regression.py --verify-fixture-only
```
