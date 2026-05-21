# Skill: AUTOSAR Software Architecture

## Purpose
Provide technical guidelines and architectural constraints for developing software components (SWCs) compliant with the AUTOSAR Classic platform, ensuring correct integration with the RTE and BSW layers.

---

## 1. Software Component (SWC) Design Protocol
1. **Ports Configuration**: Define distinct communication ports strictly adhering to the SWC description:
   * **Sender-Receiver (S/R) Ports**: Used for data-oriented communication. Ensure data elements match AUTOSAR base types.
   * **Client-Server (C/S) Ports**: Used for operation/service invocation. Define synchronous or asynchronous execution contexts carefully.
2. **Runnable Entities**: Declare runnables with explicit activation triggers (e.g., TimingEvent for periodic execution, DataReceivedEvent for reactive flows).
3. **BSW Layer Abstraction**: Under no circumstance should an Application SWC access hardware registers directly. All hardware interactions must go through the **MCAL** (Microcontroller Abstraction Layer) and **ECUAL** (ECU Abstraction Layer) via standard BSW APIs or service ports.

---

## 2. RTE (Run-Time Environment) Integration
1. **RTE APIs**: Interface with other SWCs or BSW modules exclusively using generated RTE APIs:
   * `Rte_Read_<Port>_<Data>` / `Rte_Write_<Port>_<Data>` for Sender-Receiver ports.
   * `Rte_Call_<Port>_<Operation>` for Client-Server ports.
2. **Return Codes**: Always check and handle RTE status returns (`RTE_E_OK`, `RTE_E_NO_DATA`, `RTE_E_LIMIT`, `RTE_E_TIMEOUT`) to handle bus failures or unresolved data sources gracefully.
3. **AUTOSAR Data Types**: Enforce the use of standard AUTOSAR Platform Types (`boolean`, `uint8`, `sint16`, `uint32`, `float32`) instead of native C types (`char`, `short`, `int`, `float`) to guarantee portability across compilers.

---

## 3. Memory Mapping & Calibration
1. **MemMap Compiler Abstraction**: Wrap variable declarations, constant definitions, and executable code blocks in specific MemMap macros:
   ```c
   #define SWC_START_SEC_CODE
   #include "SWC_MemMap.h"
   
   FUNC(void, SWC_CODE) SWC_RunnableFunc(void) {
       /* Runnable Logic */
   }
   
   #define SWC_STOP_SEC_CODE
   #include "SWC_MemMap.h"
   ```
2. **Calibration Parameters**: Isolate calibratable constants (e.g., maps, curves, thresholds) under calibration memory sections (`CALPRM`) to allow online tuning by calibration tools (e.g., ETAS INCA, Vector CANape) without rebuilding the binary.
