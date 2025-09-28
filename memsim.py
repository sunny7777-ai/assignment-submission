#!/usr/bin/env python3
"""
memsim.py â€" demand-paging memory simulator with LRU and CLOCK

Usage:
    python3 memsim.py <tracefile> <numframes> <algorithm> <mode>
    python3 memsim.py peek <tracefile> [N]

The "peek" mode is for debugging only: it prints the first N lines of a trace file
so you can inspect the format. This will not be used by the autograder.
"""
from __future__ import annotations
import sys
from collections import OrderedDict
from typing import Optional, Tuple
import re

# In the course traces, addresses are byte addresses; use 4KiB pages.
PAGE_SIZE = 4096  # bytes

# -------------------------- Common utilities ---------------------------
class Frame:
    __slots__ = ("page", "dirty")
    def __init__(self, page: int, dirty: bool = False):
        self.page = page
        self.dirty = dirty


def parse_line(line: str) -> Optional[Tuple[str, int]]:
    """Parse a single trace line in very tolerant fashion.
    Supports formats like:
    - R 0x1A2B, W 0x1000 (operation first)
    - 0041f7a0 R, 13f5e2c0 W (address first) 
    - Hex addresses with or without 0x prefix
    Returns (op, address_int) or None for comments/blank/unparsable lines.
    """
    s = line.strip()
    if not s or s.startswith('#') or s.startswith('//'):
        return None

    # Split into tokens
    parts = s.split()
    if len(parts) < 2:
        return None

    # Operation keywords
    OP_READ = {"R", "L", "READ", "LOAD"}
    OP_WRITE = {"W", "S", "WRITE", "STORE", "M", "MODIFY"}
    
    def is_hex_addr(token: str) -> bool:
        """Check if token looks like a hex address"""
        token = token.strip().lower()
        # Remove 0x prefix if present
        if token.startswith('0x'):
            token = token[2:]
        # Check if remaining chars are hex digits
        return len(token) >= 4 and all(c in '0123456789abcdef' for c in token)
    
    def parse_hex_addr(token: str) -> Optional[int]:
        """Parse hex address with or without 0x prefix"""
        token = token.strip().lower()
        if token.startswith('0x'):
            token = token[2:]
        try:
            return int(token, 16)
        except ValueError:
            return None
    
    op = None
    addr = None
    
    # Try different parsing strategies
    for i in range(len(parts)):
        token_upper = parts[i].upper().strip(',;:')
        
        # Check if this token is an operation
        if token_upper in OP_READ:
            op = 'R'
            # Look for address in remaining tokens
            for j in range(len(parts)):
                if j != i and is_hex_addr(parts[j]):
                    addr = parse_hex_addr(parts[j])
                    break
            break
        elif token_upper in OP_WRITE:
            op = 'W'
            # Look for address in remaining tokens  
            for j in range(len(parts)):
                if j != i and is_hex_addr(parts[j]):
                    addr = parse_hex_addr(parts[j])
                    break
            break
    
    # If no operation found, try common formats
    if op is None:
        # Try: address operation (like "0041f7a0 R")
        if len(parts) >= 2:
            if is_hex_addr(parts[0]):
                addr = parse_hex_addr(parts[0])
                token_upper = parts[1].upper().strip(',;:')
                if token_upper in OP_READ:
                    op = 'R'
                elif token_upper in OP_WRITE:
                    op = 'W'
            # Try: operation address (like "R 0041f7a0")  
            elif is_hex_addr(parts[1]):
                addr = parse_hex_addr(parts[1])
                token_upper = parts[0].upper().strip(',;:')
                if token_upper in OP_READ:
                    op = 'R'
                elif token_upper in OP_WRITE:
                    op = 'W'
    
    if op is None or addr is None:
        return None
    
    return op, addr

# ------------------------------ LRU -----------------------------------
class LRUSim:
    def __init__(self, capacity: int, debug: bool = False):
        if capacity <= 0:
            raise ValueError("numframes must be positive")
        self.capacity = capacity
        self.frames: "OrderedDict[int, Frame]" = OrderedDict()
        self.debug = debug
        self.events = 0
        self.disk_reads = 0
        self.disk_writes = 0

    def _touch(self, page: int):
        self.frames.move_to_end(page, last=True)

    def access(self, op: str, addr: int):
        self.events += 1
        page = addr // PAGE_SIZE
        if page in self.frames:
            fr = self.frames[page]
            if op == 'W':
                fr.dirty = True
            self._touch(page)
            if self.debug:
                print(f"hit  {op} {addr:#x} -> page {page}")
            return
        self.disk_reads += 1
        if len(self.frames) >= self.capacity:
            evict_page, evict_fr = self.frames.popitem(last=False)
            if evict_fr.dirty:
                self.disk_writes += 1
                if self.debug:
                    print(f"evict dirty {evict_page}")
        self.frames[page] = Frame(page, dirty=(op == 'W'))
        # REMOVED: self._touch(page) - new pages are already in MRU position
        if self.debug:
            print(f"MISS {op} {addr:#x} -> page {page}")

# ------------------------------ CLOCK ---------------------------------
class ClockSim:
    def __init__(self, capacity: int, debug: bool = False):
        if capacity <= 0:
            raise ValueError("numframes must be positive")
        self.capacity = capacity
        self.pages = [-1] * capacity
        self.refbit = [0] * capacity
        self.dirty = [0] * capacity
        self.hand = 0
        self.loc = {}
        self.debug = debug
        self.events = 0
        self.disk_reads = 0
        self.disk_writes = 0

    def _advance(self):
        self.hand = (self.hand + 1) % self.capacity

    def access(self, op: str, addr: int):
        self.events += 1
        page = addr // PAGE_SIZE
        idx = self.loc.get(page, -1)
        if idx != -1:
            self.refbit[idx] = 1
            if op == 'W':
                self.dirty[idx] = 1
            if self.debug:
                print(f"hit  {op} {addr:#x} -> page {page} at {idx}")
            return
        self.disk_reads += 1
        empty_idx = -1
        for i in range(self.capacity):
            if self.pages[i] == -1:
                empty_idx = i
                break
        if empty_idx != -1:
            victim = empty_idx
        else:
            while True:
                if self.refbit[self.hand] == 0:
                    victim = self.hand
                    break
                if self.debug:
                    print(f" second chance to page {self.pages[self.hand]} at {self.hand}")
                self.refbit[self.hand] = 0
                self._advance()
        old_page = self.pages[victim]
        if old_page != -1:
            if self.dirty[victim]:
                self.disk_writes += 1
            del self.loc[old_page]
        self.pages[victim] = page
        self.refbit[victim] = 1
        self.dirty[victim] = 1 if op == 'W' else 0
        self.loc[page] = victim
        self.hand = (victim + 1) % self.capacity
        if self.debug:
            print(f"MISS {op} {addr:#x} -> page {page} placed at {victim}")

# ---------------------------- Runner ----------------------------------

def _dump_trace_preview(trace_path: str, max_lines: int = 40):
    try:
        with open(trace_path, 'r') as f:
            raw = f.readlines()
    except Exception as e:
        sys.stderr.write(f"[memsim] could not read trace for preview: {e}\n")
        return
    sys.stderr.write("[memsim] ===== TRACE RAW PREVIEW =====\n")
    for i, line in enumerate(raw[:max_lines], 1):
        sys.stderr.write(f"[memsim] {i:4d}: {line.rstrip()}\n")
    sys.stderr.write("[memsim] ============================\n")


def simulate(trace_path: str, numframes: int, algorithm: str, mode: str):
    algo = (algorithm or "").strip().lower()
    debug = ((mode or "").strip().lower() == "debug")

    if algo == "lru":
        sim = LRUSim(numframes, debug=debug)
    elif algo == "clock":
        sim = ClockSim(numframes, debug=debug)
    else:
        raise NotImplementedError("Supported algorithms: lru, clock")

    with open(trace_path, 'r') as f:
        for line in f:
            parsed = parse_line(line)
            if not parsed:
                continue
            op, addr = parsed
            sim.access(op, addr)

    if sim.events == 0:
        _dump_trace_preview(trace_path, max_lines=50)

    page_fault_rate = (sim.disk_reads / sim.events) if sim.events else 0.0

    # Remove ">" prefix to match expected format
    print(f"total memory frames:  {numframes}")
    print(f"events in trace:      {sim.events}")
    print(f"total disk reads:     {sim.disk_reads}")
    print(f"total disk writes:    {sim.disk_writes}")
    print(f"page fault rate:      {page_fault_rate:.4f}")


def peek_trace(path: str, N: int = 20):
    try:
        with open(path, 'r') as f:
            for i, line in enumerate(f, 1):
                print(f"{i:4d}: {line.rstrip()}")
                if i >= N:
                    break
    except FileNotFoundError:
        print(f"could not open trace file: {path}")


def main(argv):
    if len(argv) >= 2 and argv[1] == "peek":
        if len(argv) < 3:
            print("Usage: python3 memsim.py peek <tracefile> [N]")
            return 2
        path = argv[2]
        N = int(argv[3]) if len(argv) > 3 else 20
        peek_trace(path, N)
        return 0

    if len(argv) != 5:
        sys.stderr.write("Usage: python3 memsim.py <tracefile> <numframes> <algorithm> <mode>\n")
        return 2
    _, tracefile, numframes_s, algorithm, mode = argv
    try:
        numframes = int(numframes_s)
    except ValueError:
        sys.stderr.write("numframes must be an integer\n")
        return 2
    try:
        simulate(tracefile, numframes, algorithm, mode)
    except FileNotFoundError:
        sys.stderr.write(f"could not open trace file: {tracefile}\n")
        return 2
    except NotImplementedError as e:
        sys.stderr.write(str(e) + "\n")
        return 2
    except ValueError as e:
        sys.stderr.write(str(e) + "\n")
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
