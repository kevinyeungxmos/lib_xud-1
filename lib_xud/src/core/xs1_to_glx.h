// Copyright (c) 2017, XMOS Ltd, All rights reserved

#ifndef _XS1_TO_GLX_H_
#define _XS1_TO_GLX_H_
/* Workaround for tools issue #17048 */

#define XS1_SU_PER_UIFM_CHANEND_NUM                     XS1_GLX_PER_UIFM_CHANEND_NUM
#define XS1_SU_PER_UIFM_CONTROL_NUM                     XS1_GLX_PER_UIFM_CONTROL_NUM

#define XS1_SU_CFG_RST_MISC_NUM                         XS1_GLX_CFG_RST_MISC_NUM
#define XS1_SU_CFG_USB_CLK_EN_SHIFT                     XS1_GLX_CFG_USB_CLK_EN_SHIFT

#define XS1_SU_CFG_USB_CLK_EN_SHIFT                     XS1_GLX_CFG_USB_CLK_EN_SHIFT

#define XS1_SU_CFG_USB_EN_SHIFT                         XS1_GLX_CFG_USB_EN_SHIFT

#define XS1_SU_PER_UIFM_OTG_CONTROL_NUM                 XS1_GLX_PER_UIFM_OTG_CONTROL_NUM
#define XS1_SU_UIFM_IFM_CONTROL_DECODELINESTATE_SHIFT   XS1_UIFM_IFM_CONTROL_DECODELINESTATE_SHIFT

#define XS1_SU_PER_UIFM_FUNC_CONTROL_NUM                XS1_GLX_PER_UIFM_FUNC_CONTROL_NUM

#define XS1_SU_UIFM_FUNC_CONTROL_XCVRSELECT_SHIFT       XS1_UIFM_FUNC_CONTROL_XCVRSELECT_SHIFT
#define XS1_SU_UIFM_FUNC_CONTROL_TERMSELECT_SHIFT       XS1_UIFM_FUNC_CONTROL_TERMSELECT_SHIFT

#define XS1_SU_PER_UIFM_DEVICE_ADDRESS_NUM              XS1_GLX_PER_UIFM_DEVICE_ADDRESS_NUM


#define XS1_SU_UIFM_IFM_CONTROL_DOTOKENS_SHIFT          XS1_UIFM_IFM_CONTROL_DOTOKENS_SHIFT
#define XS1_SU_UIFM_IFM_CONTROL_CHECKTOKENS_SHIFT       XS1_UIFM_IFM_CONTROL_CHECKTOKENS_SHIFT
#define XS1_SU_UIFM_IFM_CONTROL_DECODELINESTATE_SHIFT   XS1_UIFM_IFM_CONTROL_DECODELINESTATE_SHIFT
#define XS1_SU_UIFM_IFM_CONTROL_SOFISTOKEN_SHIFT        XS1_UIFM_IFM_CONTROL_SOFISTOKEN_SHIFT

#define XS1_SU_PER_UIFM_MASK_NUM                        XS1_GLX_PER_UIFM_MASK_NUM

#define XS1_SU_UIFM_IFM_FLAGS_NEWTOKEN_SHIFT            XS1_UIFM_IFM_FLAGS_NEWTOKEN_SHIFT
#define XS1_SU_UIFM_IFM_FLAGS_RXACTIVE_SHIFT            XS1_UIFM_IFM_FLAGS_RXACTIVE_SHIFT
#define XS1_SU_UIFM_IFM_FLAGS_RXERROR_SHIFT             XS1_UIFM_IFM_FLAGS_RXERROR_SHIFT

#define XS1_SU_PER_UIFM_OTG_FLAGS_NUM                   XS1_GLX_PER_UIFM_OTG_FLAGS_NUM
#define XS1_SU_UIFM_OTG_FLAGS_SESSVLDB_SHIFT            XS1_UIFM_OTG_FLAGS_SESSVLDB_SHIFT

#endif
