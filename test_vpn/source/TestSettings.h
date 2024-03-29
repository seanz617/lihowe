#pragma once

#include <TlHelp32.h>
#include "ShellHandler.h"
// TestSettings 对话框

class TestSettings : public CDialogEx
{
	DECLARE_DYNAMIC(TestSettings)

public:
	TestSettings(CWnd* pParent = nullptr);   // 标准构造函数
	virtual ~TestSettings();

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_DIALOG2 };
#endif

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

	DECLARE_MESSAGE_MAP()
public:
	CBrush m_brush;
	PROCESS_INFORMATION ProcessInfo;
	STARTUPINFO StartupInfo;
	DWORD pvpn_pid;
	DWORD pvpn_parent_pid;
	struct TestConfig* ptc;

	ShellHandler sh_update_proxy_stun;

	void StartPvpn();
	void StopPvpn();
	BOOL CheckPvpn();

	afx_msg HBRUSH OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor);
	virtual BOOL OnInitDialog();
	afx_msg void OnBnClickedButton1();
	afx_msg void OnBnClickedButton5();
	afx_msg void OnDestroy();
	afx_msg void OnBnClickedButton2();
	afx_msg void OnTimer(UINT_PTR nIDEvent);
	afx_msg void OnSize(UINT nType, int cx, int cy);
protected:
	afx_msg LRESULT OnChildWndResize(WPARAM wParam, LPARAM lParam);
	afx_msg LRESULT OnLoadPvpnConfig(WPARAM wParam, LPARAM lParam);
public:
	CComboBox proxy_list;
	CComboBox stun_list;
protected:
	afx_msg LRESULT OnUpdateProxyStun(WPARAM wParam, LPARAM lParam);
};
