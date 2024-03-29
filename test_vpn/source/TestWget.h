#pragma once

#include <TlHelp32.h>
#include "ShellHandler.h"

class TestWget : public CDialogEx
{
	DECLARE_DYNAMIC(TestWget)

public:
	TestWget(CWnd* pParent = nullptr);   // 标准构造函数
	virtual ~TestWget();

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_DIALOG3 };
#endif

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

	DECLARE_MESSAGE_MAP()
	afx_msg LRESULT OnChildWndResize(WPARAM wParam, LPARAM lParam);
public:
	CBrush m_brush;
	ShellHandler sh;
	virtual BOOL OnInitDialog();
	afx_msg void OnBnClickedButton1();
	BOOL CheckWget();
	DWORD wget_pid;
	DWORD wget_parent_pid;
protected:
	afx_msg LRESULT OnWgetStatus(WPARAM wParam, LPARAM lParam);
public:
	CProgressCtrl progress;
	afx_msg void OnBnClickedButton2();
	CButton info_text;
	CEdit wget_result;
	CString current_address;
	afx_msg HBRUSH OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor);
	CComboBox connect_type;
};
