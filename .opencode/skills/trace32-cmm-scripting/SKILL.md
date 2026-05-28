---
name: trace32-cmm-scripting
description: Enable the generation and debugging of Lauterbach TRACE32 PRACTICE (.
---

# Skill: TRACE32 CMM Scripting

## Purpose
Enable the generation and debugging of Lauterbach TRACE32 PRACTICE (.cmm) scripts to configure, initialize, and debug various target microcontrollers (e.g., Infineon Traveo II, Aurix, STM32).

---

## 1. Target Connection and Setup
1. **Initialize State**: Always start a CMM script by resetting the debugger state to prevent conflicting configurations:
   ```practice
   RESet
   ```
2. **CPU and Debug Interface**: Specify the microcontroller architecture and JTAG/SWD debug port configuration:
   ```practice
   SYStem.CPU CYT2B7         ; Set the specific micro family (e.g. Infineon Traveo II)
   SYStem.CONFIG.DEBUGPORTTYPE SWD ; Select SWD or JTAG
   SYStem.CONFIG.Connector MIPI20  ; Select debug header connector
   ```
3. **Multi-core Initialization**: For multi-core microcontrollers (e.g., Cortex-M0+ and Cortex-M4/M7 in Traveo II), configure the multi-core debug session (master/slave instances) and trigger CPU startup:
   ```practice
   SYStem.Up                 ; Start the debugger connection and halt the CPU
   ```

---

## 2. Flashing & Debugging Sequences
1. **ELF Symbols Loading**: Load the compiled application symbols to allow structured source code mapping:
   ```practice
   Data.LOAD.Elf "build/app.elf" /NoCODE ; Loads symbol map without copying raw bytes
   ```
2. **Flash Programming Sequence**: Automate the flashing process using target-specific flash drivers:
   ```practice
   FLASH.RESet
   FLASH.Create 1. 0x10000000--0x100FFFFF 0x10000 Target ; Define flash sector
   FLASH.ReProgram.ALL /Erase                           ; Enable reprogram mode with sector erase
   Data.LOAD.Elf "build/app.elf"                         ; Flash the compiled binary
   FLASH.ReProgram.OFF                                  ; Close reprogram mode
   ```
3. **Execution Control**: Program basic register controls and execute:
   ```practice
   Register.Set PC 0x10000000  ; Point Program Counter to entry address
   Break.Set main             ; Set a breakpoint at main()
   Go                         ; Start target execution
   ```

---

## 3. CMM Scripting Best Practices
1. **Dialogue and Visual Feedback**: Create custom dialog areas to present messages or allow interactive input:
   ```practice
   AREA.Create DebugInfo 80. 20.
   AREA.Select DebugInfo
   PRINT "=== Starting Flash Script ==="
   ```
2. **Timing and Verification**: Insert appropriate delays (`WAIT 100.ms`) to let the PLL settle or complete flash erase operations. Always verify the connection state before executing operations:
   ```practice
   IF !SYStem.UP()
   (
       PRINT "Error: Connection failed!"
       ENDDO
   )
   ```
3. **Script Termination**: Always close active sessions and clean up variables at the end of the script using `ENDDO`.
