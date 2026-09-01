# Benchmark protocol

Run:

```bash
python -m resolutive_routing.benchmark
```

The microbenchmark compares deterministic selection overhead for:

- resolutive score;
- first available;
- lowest latency;
- highest advertised hardware;
- seeded random routing;
- broadcast candidate selection.

The included `demo_v1` scenario is intentionally small. Timing results depend on the machine and Python runtime. They are diagnostic measurements, not performance claims. The more important first comparison is the selected destination and whether every strategy respects the same policy filter.

Future experiments should use recorded node-state fixtures, explicit expected utility and enough scenarios to compare route quality—not only execution time.

