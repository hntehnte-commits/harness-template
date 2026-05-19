#include "wdt.h"

/* Dummy Traveo II (CYT2/CYT3/CYT4) WDT Registers */
#define SRSS_WDT_BASE_ADDR (0x40020000UL)
#define WDT_CTRL           (*(volatile uint32_t*)(SRSS_WDT_BASE_ADDR + 0x00))
#define WDT_MATCH          (*(volatile uint32_t*)(SRSS_WDT_BASE_ADDR + 0x08))
#define WDT_FEED           (*(volatile uint32_t*)(SRSS_WDT_BASE_ADDR + 0x0C))

#define WDT_CTRL_ENABLE_Msk (0x80000000UL)
#define WDT_FEED_PATTERN    (0x1ACCE551UL)

void WDT_Init(void) {
    /* Set match value for timeout (e.g. 1 second depending on clk_lf) */
    WDT_MATCH = 0x0FFF;
    
    /* Enable Watchdog */
    WDT_CTRL |= WDT_CTRL_ENABLE_Msk;
}

void WDT_Feed(void) {
    /* Feed the watchdog to prevent system reset */
    WDT_FEED = WDT_FEED_PATTERN;
}
