#include "wdt.h"

int main(void) {
    /* System Core Initialization (Dummy) */
    
    /* Initialize Watchdog for Traveo II */
    WDT_Init();
    
    while(1) {
        /* Main Application Loop */
        
        /* Clear Watchdog Timer */
        WDT_Feed();
    }
    
    return 0;
}
