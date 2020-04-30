
#include "XUD_HAL.h"
#include <xs1.h>

#ifdef __XS2A__
#include "xs2_su_registers.h"
#include "XUD_USBTile_Support.h"

extern in port flag0_port;
extern in port flag1_port;
extern in port flag2_port;

extern unsigned get_tile_id(tileref ref);
extern tileref USB_TILE_REF;

#else

#include <xs3a_registers.h>
extern in port flag0_port; /* For XS3: RXA  or DP */
extern in port flag1_port; /* For XS3: RXE  or DM */

void XUD_SetCrcTableAddr(unsigned addr);

unsigned XtlSelFromMhz(unsigned m)
{
    switch(m)
    {
        case 10:
            return 0b000;
        case 12:
            return 0b001;
        case 25:
            return 0b010;
        case 30:
            return 0b011;
        case 19: /*.2*/
            return 0b100;
        case 24:
            return 0b101;
        case 27:
            return 0b110;
        case 40:
            return 0b111;
        default:
            /* Panic */
            while(1);
            break;
    }
}

void XUD_HAL_EnterMode_PeripheralFullSpeed()
{
#ifndef XUD_SIM_XSIM
    unsigned d = 0;
    d = XS1_USB_PHY_CFG0_UTMI_XCVRSELECT_SET(d, 1);
    d = XS1_USB_PHY_CFG0_UTMI_TERMSELECT_SET(d, 1);
    d = XS1_USB_PHY_CFG0_UTMI_OPMODE_SET(d, 0);
    d = XS1_USB_PHY_CFG0_DMPULLDOWN_SET(d, 0);
    d = XS1_USB_PHY_CFG0_DPPULLDOWN_SET(d, 0);
    
    d = XS1_USB_PHY_CFG0_UTMI_SUSPENDM_SET(d, 1);
    d = XS1_USB_PHY_CFG0_TXBITSTUFF_EN_SET(d, 1);
    d = XS1_USB_PHY_CFG0_PLL_EN_SET(d, 1);
    d = XS1_USB_PHY_CFG0_LPM_ALIVE_SET(d, 0);
    d = XS1_USB_PHY_CFG0_IDPAD_EN_SET(d, 0);

    unsigned xtlSelVal = XtlSelFromMhz(XUD_OSC_MHZ);
    d = XS1_USB_PHY_CFG0_XTLSEL_SET(d, xtlSelVal);
    
    write_sswitch_reg(get_local_tile_id(), XS1_SSWITCH_USB_PHY_CFG0_NUM, d); 
#endif
}

void XUD_HAL_EnterMode_PeripheralChirp()
{
#ifndef XUD_SIM_XSIM
    unsigned d = 0;
    d = XS1_USB_PHY_CFG0_UTMI_XCVRSELECT_SET(d, 0);
    d = XS1_USB_PHY_CFG0_UTMI_TERMSELECT_SET(d, 1);
    d = XS1_USB_PHY_CFG0_UTMI_OPMODE_SET(d, 0b10);
    d = XS1_USB_PHY_CFG0_DMPULLDOWN_SET(d, 0);
    d = XS1_USB_PHY_CFG0_DPPULLDOWN_SET(d, 0);
    
    d = XS1_USB_PHY_CFG0_UTMI_SUSPENDM_SET(d, 1);
    d = XS1_USB_PHY_CFG0_TXBITSTUFF_EN_SET(d, 1);
    d = XS1_USB_PHY_CFG0_PLL_EN_SET(d, 1);
    d = XS1_USB_PHY_CFG0_LPM_ALIVE_SET(d, 0);
    d = XS1_USB_PHY_CFG0_IDPAD_EN_SET(d, 0);

    unsigned xtlselVal = XtlSelFromMhz(XUD_OSC_MHZ);
    d = XS1_USB_PHY_CFG0_XTLSEL_SET(d, xtlselVal);
    write_sswitch_reg(get_local_tile_id(), XS1_SSWITCH_USB_PHY_CFG0_NUM, d); 
#endif
}

void XUD_HAL_EnterMode_PeripheralHighSpeed()
{
#ifndef XUD_SIM_XSIM
    unsigned d = 0;
    d = XS1_USB_PHY_CFG0_UTMI_XCVRSELECT_SET(d, 0); // HS
    d = XS1_USB_PHY_CFG0_UTMI_TERMSELECT_SET(d, 0); // HS
    d = XS1_USB_PHY_CFG0_UTMI_OPMODE_SET(d, 0b00);  // Normal operation
    d = XS1_USB_PHY_CFG0_DMPULLDOWN_SET(d, 0);
    d = XS1_USB_PHY_CFG0_DPPULLDOWN_SET(d, 0);
    
    d = XS1_USB_PHY_CFG0_UTMI_SUSPENDM_SET(d, 1);
    d = XS1_USB_PHY_CFG0_TXBITSTUFF_EN_SET(d, 1);
    d = XS1_USB_PHY_CFG0_PLL_EN_SET(d, 1);
    d = XS1_USB_PHY_CFG0_LPM_ALIVE_SET(d, 0);
    d = XS1_USB_PHY_CFG0_IDPAD_EN_SET(d, 0);

    unsigned xtlselVal = XtlSelFromMhz(XUD_OSC_MHZ);
    d = XS1_USB_PHY_CFG0_XTLSEL_SET(d, xtlselVal);
    write_sswitch_reg(get_local_tile_id(), XS1_SSWITCH_USB_PHY_CFG0_NUM, d); 
#endif
}

void XUD_HAL_EnterMode_PeripheralTestJTestK()
{
#ifndef XUD_SIM_XSIM
#ifdef __XS3A__

  /* From ULPI Specification Revsion 1.1, table 41 
     * XcvrSelect:  00b
     * TermSelect:  0b
     * OpMode:      10b
     * DpPullDown   0b
     * DmPullDown:  0b
     */
    unsigned d = 0;
    d = XS1_USB_PHY_CFG0_UTMI_XCVRSELECT_SET(d, 0);
    d = XS1_USB_PHY_CFG0_UTMI_TERMSELECT_SET(d, 0);
    d = XS1_USB_PHY_CFG0_UTMI_OPMODE_SET(d, 2);
    d = XS1_USB_PHY_CFG0_DMPULLDOWN_SET(d, 0);
    d = XS1_USB_PHY_CFG0_DPPULLDOWN_SET(d, 0);

    d = XS1_USB_PHY_CFG0_UTMI_SUSPENDM_SET(d, 1);
    d = XS1_USB_PHY_CFG0_TXBITSTUFF_EN_SET(d, 1);
    d = XS1_USB_PHY_CFG0_PLL_EN_SET(d, 1);
    d = XS1_USB_PHY_CFG0_LPM_ALIVE_SET(d, 0);
    d = XS1_USB_PHY_CFG0_IDPAD_EN_SET(d, 0);

    unsigned xtlSelVal = XtlSelFromMhz(XUD_OSC_MHZ);
    d = XS1_USB_PHY_CFG0_XTLSEL_SET(d, xtlSelVal);

    write_sswitch_reg(get_local_tile_id(), XS1_SSWITCH_USB_PHY_CFG0_NUM, d); 
#else
    write_periph_word(USB_TILE_REF, XS1_GLX_PER_UIFM_CHANEND_NUM, XS1_GLX_PER_UIFM_FUNC_CONTROL_NUM, 0b1000);
#endif
#endif
}

void XUD_HAL_Mode_PowerSig()
{
#ifndef XUD_SIM_XSIM
    unsigned d = 0;
    d = XS1_USB_SHIM_CFG_FLAG_MODE_SET(d, 1);
    write_sswitch_reg(get_local_tile_id(), XS1_SSWITCH_USB_SHIM_CFG_NUM, d); 
#endif
}

void XUD_HAL_Mode_DataTransfer()
{
#ifndef XUD_SIM_XSIM
    unsigned d = 0;
    d = XS1_USB_SHIM_CFG_FLAG_MODE_SET(d, 0);
    write_sswitch_reg(get_local_tile_id(), XS1_SSWITCH_USB_SHIM_CFG_NUM, d); 
#endif
}

#endif

/* In full-speed and low-speed mode, LineState(0) always reflects DP and LineState(1) reflects DM */
/* Note, this port ordering is the opposide of what might be expected - but linestate is swapped in the USB shim */
#define dp_port flag1_port      // DP: LINESTATE[0]
#define dm_port flag0_port      // DM: LINESTATE[1]

{unsigned, unsigned} LineStateToLines(XUD_LineState_t ls)
{
    return {ls & 1, (ls >> 1) & 1};
}

static inline XUD_LineState_t LinesToLineState(unsigned dp, unsigned dm)
{
    return (XUD_LineState_t) (dp & 1) | ((dm & 1)<< 1);
}

/* TODO pass structure  */
XUD_LineState_t XUD_HAL_GetLineState(/*XUD_HAL_t &xudHal*/)
{
#ifdef __XS3A__
    unsigned dp, dm;
    dp_port :> dp;
    dm_port :> dm;
    return LinesToLineState(dp, dm);
#else   
    unsigned j, k, se0;
    flag0_port :> j;
    flag1_port :> k;
    flag2_port :> se0;

    if(j) 
        return XUD_LINESTATE_J;
    if(k)
        return XUD_LINESTATE_K;
    if(se0)
        return XUD_LINESTATE_SE0;

#endif
}

unsigned XUD_HAL_WaitForLineStateChange(XUD_LineState_t &currentLs, unsigned timeout)
{
#ifdef __XS3A__
    unsigned dp, dm;
    timer t; 
    unsigned time;

    /* Look up line values from linestate */
    {dp, dm} = LineStateToLines(currentLs);

    if (timeout != null)
        t :> time;

    /* Wait for change */
    select 
    {
        case dp_port when pinsneq(dp) :> dp:
            break;
        case dm_port when pinsneq(dm) :> dm:
            break;
        case timeout != null => t when timerafter(time + timeout) :> int _:
            return 1;

    }

    /* Return new linestate */
    currentLs = LinesToLineState(dp, dm);
    return 0;

#else
    #error TODO
#endif
    
}

void XUD_HAL_SetDeviceAddress(unsigned char address)
{
#if defined(__XS2A__)
    write_periph_word(USB_TILE_REF, XS1_SU_PER_UIFM_CHANEND_NUM, XS1_SU_PER_UIFM_DEVICE_ADDRESS_NUM, address);
#elif defined(__XS3A__)
    XUD_SetCrcTableAddr(address);
#endif
}



