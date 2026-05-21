# Skill: Python Performance Optimization

## Purpose
Provide concrete diagnostic protocols and performance tuning patterns for high-throughput or memory-constrained Python applications, optimizing loops, data structures, and I/O execution.

---

## 1. Diagnostics and Profiling Protocol
1. **Locate Bottlenecks**: Before optimizing any code, execute a precise CPU or memory audit. Never optimize based on assumptions:
   * **CPU Profiling**: Run the `cProfile` module to identify slow functions:
     `python -m cProfile -s tottime my_script.py`
   * **Memory Profiling**: Use `memory_profiler` (`@profile` decorator) to trace line-by-line RAM allocation.
2. **Micro-benchmarking**: Use the `timeit` module to test alternative code implementations for high-frequency loops or data parsing.

---

## 2. Memory & Data Structure Tuning
1. **Class Footprint Reduction**: Use `__slots__` in data-heavy classes (instantiated thousands of times) to prevent dynamic dictionary allocation and cut RAM usage by up to 60%:
   ```python
   class DataPoint:
       __slots__ = ('x', 'y', 'timestamp')
       def __init__(self, x, y, ts):
           self.x = x
           self.y = y
           self.timestamp = ts
   ```
2. **Generators for Large Data Sets**: Never load massive query results or files completely into RAM. Implement generator expressions or custom iterable structures using `yield` for memory-efficient lazy evaluation.
3. **Optimized Built-ins**: Utilize collections like `deque` for O(1) double-ended operations, and set/dictionary operations for O(1) membership lookups instead of list iteration.

---

## 3. Concurrency & I/O Abstraction
1. **I/O Bound Workloads**: Use `asyncio` or `concurrent.futures.ThreadPoolExecutor` to handle parallel API requests, database queries, and file transactions without blocking the primary event loop.
2. **CPU Bound Workloads**: Evade the GIL (Global Interpreter Lock) for heavy computations (e.g. image processing, data analysis) by utilizing `multiprocessing` or delegating the core logic to highly optimized C-extensions (like NumPy).
