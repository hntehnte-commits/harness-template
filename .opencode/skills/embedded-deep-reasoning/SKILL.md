---
name: embedded-deep-reasoning
description: Enforce a rigorous, hardware-aware reasoning loop to analyze and solve complex embedded software failures, utilizing MCU hardware specifications, registers, and memory maps.
---

# Skill: Embedded Deep Reasoning

## Purpose
Enforce a rigorous, hardware-aware reasoning loop to analyze and solve complex embedded software failures, utilizing MCU hardware specifications, registers, and memory maps.

---

## 1. Hardware-Aware Context Analysis
When encountering an anomalous behavior, hardware fault, or unexpected code execution path, execute the following hardware-level audit:
1. **Identify Hardware Targets**: Inspect the specific Microcontroller (MCU) family (e.g. Infineon Traveo II, Aurix TriCore, ARM Cortex-M7) and open its Technical Reference Manual (TRM) or register map.
2. **Review Memory Allocations**: Verify the absolute address boundaries involved:
   * **RAM Sections**: DTCM (Data TCM), SRAM, Peripheral Memory Spaces.
   * **Flash / Code Sections**: ITCM (Instruction TCM), internal Code Flash, external SPI Flash.
3. **Register Map Audit**: Look up peripheral memory-mapped registers. Ensure all hardware registers are declared using the `volatile` qualifier and const pointer syntax:
   * *Correct*: `volatile uint32_t * const peripheral_reg = (volatile uint32_t *)0x40020100UL;`

---

## 2. Exception and Fault Debugging Loop
When a crash, hang, or exception (e.g., ARM Cortex HardFault, UsageFault, Aurix Trap) occurs:
1. **CPU State Recovery**: Read the core debugger registers from TRACE32 or GDB:
   * **PC (Program Counter)**: Pinpoint the exact instruction that failed.
   * **LR (Link Register)**: Determine the caller function.
   * **SP (Stack Pointer)**: Inspect the stack frame contents.
2. **System Control Block (SCB) Investigation**: For ARM Cortex cores, inspect fault status registers:
   * **HFSR (HardFault Status Register)** & **CFSR (Configurable Fault Status Register)**.
   * Check for `UNALIGNED` (unaligned access), `DIVBYZERO` (division by zero), `IBUSERR` (instruction bus error), or `PRECISERR` (precise data bus error).
3. **Concurrency Auditing**: Analyze Interrupt Service Routines (ISRs) and RTOS contexts:
   * Verify priority levels (prevent priority inversion or nested execution faults).
   * Confirm that critical sections (`taskENTER_CRITICAL()`) are correctly paired and short.

---

## 3. Systematic Hypothesis Formulation
1. **Develop Hardware Hypotheses**: Formulate three independent, distinct failure hypotheses covering both hardware and software interactions:
   * *Hypothesis A (Clock/Power)*: Clock configuration mismatch or low power mode transition state.
   * *Hypothesis B (Memory/Boundary)*: Memory alignment violation, stack overflow, or MPU (Memory Protection Unit) access violation.
   * *Hypothesis C (Concurrency)*: Race condition in shared global variables lacking `volatile` or mutex protection.
2. **Verification Plan**: Detail a precise verification plan (e.g., setting a memory watchpoint, reading active peripheral register flags, checking assembly instructions in Trace32) before modifying any production C code.
