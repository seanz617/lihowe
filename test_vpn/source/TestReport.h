#pragma once

#include "HttpHandler.h"

class TestReport : public CDialogEx
{
	DECLARE_DYNAMIC(TestReport)

public:
	TestReport(CWnd* pParent = nullptr);   // 标准构造函数
	virtual ~TestReport();

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_DIALOG1 };
#endif

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持
	DECLARE_MESSAGE_MAP()
	afx_msg LRESULT OnUpdateReport(WPARAM wParam, LPARAM lParam);
public:
	HttpHandler httpHandler;

	CListCtrl report;
	virtual BOOL OnInitDialog();
};
