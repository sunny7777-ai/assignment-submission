# Test Report – memsim.py

**Generated:** 2025-09-12T14:58:05

**Platform:** macOS-15.6.1-arm64-arm-64bit

**Python:** 3.12.7 | packaged by Anaconda, Inc. | (main, Oct  4 2024, 08:22:19) [Clang 14.0.6 ]

**Python Executable:** /opt/anaconda3/bin/python3

**memsim.py:** `/Users/huangjie/Documents/2025s2/OS_pace/Assignment2/prac2/memsim.py`

**SHA256(memsim.py):** `2b82b81916ec585593614984b6b214fb68771a951affc059b868d43fce7aca88`

---

## Case: trace_sanity.txt

**Command:** `python3 memsim.py < trace_sanity.txt`

**Trace (`traces/trace_sanity.txt`)**

```
1
2
3
2
4
1
```

**Observed Output**

```
=== memsim results ===
policy:     FIFO
frames:     3
references: 6
hits:       1
misses:     5
evictions:  2
hit_rate:   16.67%
```

---

## Case: trace_hits.txt

**Command:** `python3 memsim.py < trace_hits.txt`

**Trace (`traces/trace_hits.txt`)**

```
1
2
3
1
2
3
```

**Observed Output**

```
=== memsim results ===
policy:     FIFO
frames:     3
references: 6
hits:       3
misses:     3
evictions:  0
hit_rate:   50.00%
```

---

## Case: trace_evictions.txt

**Command:** `python3 memsim.py < trace_evictions.txt`

**Trace (`traces/trace_evictions.txt`)**

```
1
2
3
4
5
6
```

**Observed Output**

```
=== memsim results ===
policy:     FIFO
frames:     3
references: 6
hits:       0
misses:     6
evictions:  3
hit_rate:   0.00%
```

---

## Case: trace_repeat.txt

**Command:** `python3 memsim.py < trace_repeat.txt`

**Trace (`traces/trace_repeat.txt`)**

```
1
1
1
2
2
3
3
```

**Observed Output**

```
=== memsim results ===
policy:     FIFO
frames:     3
references: 7
hits:       4
misses:     3
evictions:  0
hit_rate:   57.14%
```

---

## Case: trace_comments.txt

**Command:** `python3 memsim.py < trace_comments.txt`

**Trace (`traces/trace_comments.txt`)**

```
# this is a comment
1

2
# another comment
3
2
```

**Observed Output**

```
=== memsim results ===
policy:     FIFO
frames:     3
references: 4
hits:       1
misses:     3
evictions:  0
hit_rate:   25.00%
```

---

## Case: trace_single_frame.txt

**Command:** `python3 memsim.py < trace_single_frame.txt`

**Trace (`traces/trace_single_frame.txt`)**

```
1
2
1
2
1
```

**Observed Output**

```
=== memsim results ===
policy:     FIFO
frames:     3
references: 5
hits:       3
misses:     2
evictions:  0
hit_rate:   60.00%
```

---

