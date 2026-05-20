---
name: c-memory-analyzer-profile-specific
description: Ensure C code is safe for resource-constrained, high-reliability embedded systems (Infineon Traveo II or equivalent), enforcing memory safety and style guidelines.
---

# Skill: C Memory Analyzer (Profile Specific)

## Purpose
Ensure C code is safe for resource-constrained, high-reliability embedded systems (Infineon Traveo II or equivalent), enforcing memory safety and style guidelines.

---

## 1. Static Allocation Audit
- Verify that **NO** dynamic memory allocation functions (`malloc`, `calloc`, `realloc`, `free`) are used in the source code.
- Verify that arrays have fixed, constant bounds known at compile-time.

---

## 2. Pointer Safety Checks
Before writing or modifying pointer arithmetic:
1. **NULL Checking**: Ensure pointers are checked against `NULL` before dereferencing.
2. **Buffer Overrun Prevention**: Validate bounds before reading/writing inside a buffer array.
3. **Volatile Peripheral Mapping**: Check that any peripheral register addresses (e.g. at `0x40000000`) utilize the `volatile` modifier.
   * Example: `volatile uint32_t * const reg = (volatile uint32_t *)0x40020000UL;`

---

## 3. Compliance Guidelines (MISRA C)
1. Do not use nested comments.
2. All functions must have explicit return types.
3. Avoid casting pointers to integer types unless mapping hardware registers.
