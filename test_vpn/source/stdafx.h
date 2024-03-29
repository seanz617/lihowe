
// stdafx.h : 标准系统包含文件的包含文件，
// 或是经常使用但不常更改的
// 特定于项目的包含文件

#pragma once

#ifndef VC_EXTRALEAN
#define VC_EXTRALEAN            // 从 Windows 头中排除极少使用的资料
#endif

#include "targetver.h"

#define _ATL_CSTRING_EXPLICIT_CONSTRUCTORS      // 某些 CString 构造函数将是显式的

// 关闭 MFC 对某些常见但经常可放心忽略的警告消息的隐藏
#define _AFX_ALL_WARNINGS

#include <afxwin.h>         // MFC 核心组件和标准组件
#include <afxext.h>         // MFC 扩展

#include <afxdisp.h>        // MFC 自动化类

#ifndef _AFX_NO_OLE_SUPPORT
#include <afxdtctl.h>           // MFC 对 Internet Explorer 4 公共控件的支持
#endif
#ifndef _AFX_NO_AFXCMN_SUPPORT
#include <afxcmn.h>             // MFC 对 Windows 公共控件的支持
#endif // _AFX_NO_AFXCMN_SUPPORT

#include <afxcontrolbars.h>     // 功能区和控件条的 MFC 支持

#ifdef _UNICODE
#if defined _M_IX86
#pragma comment(linker,"/manifestdependency:\"type='win32' name='Microsoft.Windows.Common-Controls' version='6.0.0.0' processorArchitecture='x86' publicKeyToken='6595b64144ccf1df' language='*'\"")
#elif defined _M_X64
#pragma comment(linker,"/manifestdependency:\"type='win32' name='Microsoft.Windows.Common-Controls' version='6.0.0.0' processorArchitecture='amd64' publicKeyToken='6595b64144ccf1df' language='*'\"")
#else
#pragma comment(linker,"/manifestdependency:\"type='win32' name='Microsoft.Windows.Common-Controls' version='6.0.0.0' processorArchitecture='*' publicKeyToken='6595b64144ccf1df' language='*'\"")
#endif
#endif

#include "vlc/vlc.h" 
#include <afxcontrolbars.h>
#include <afxcontrolbars.h>
#include <afxcontrolbars.h>
#pragma comment(lib,"libvlc.lib")
#pragma comment(lib,"libvlccore.lib")

#define WM_PLAY_POS_CHANGED (WM_USER + 1)
#define WM_CHANGE_PLAY_POS (WM_USER + 2)
#define WM_USER_CHANGE_POS (WM_USER + 3)
#define WM_UPDATE_REPORT (WM_USER + 4)
#define WM_CHECK_PVPN_PROC (WM_USER + 5)
#define WM_CHILD_WND_RESIZE (WM_USER + 6)
#define WM_LOAD_PVPN_CONFIG (WM_USER + 7)
#define WM_UPDATE_CITY_ISP (WM_USER + 8)
#define WM_UPDATE_PROXY_STUN (WM_USER + 9)
#define WM_UPDATE_SPEED_TEST (WM_USER + 10)
#define WM_PLAY_STOPED (WM_USER + 11)
#define WM_WGET_STATUS (WM_USER + 12)
#define WM_PLAY_FIRST_FRAME (WM_USER + 13)
#define WM_SET_PLAY_FIRST_FRAME (WM_USER + 14)

struct report_data {
	int video_length = 0;
	int play_length = 0;
};

struct ProxyInfo
{
	CString ProxyServer;
	CString ProxyServerStun;
};

struct StunInfo
{
	CString StunName;
	CString StunAddress;
};

struct VideoInfo
{
	CString VideoName;
	CString VideoAddress;
};

struct TestConfig
{
	int ProxyCount = 0;
	int VideoCount = 0;
	int StunCount = 0;
	struct ProxyInfo ProxyInfos[16];
	struct StunInfo StunInfos[16];
	struct VideoInfo VideoInfos[16];
};