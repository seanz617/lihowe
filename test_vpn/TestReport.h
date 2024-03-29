#pragma once

#include "HttpHandler.h"
#include "ShellHandler.h"

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
	CBrush m_brush;
	CListCtrl report;
	virtual BOOL OnInitDialog();
	
	CString city;
	CString isp;
	CString ip;
	float latency;
	float download_bandwidth;
	float upload_bandwidth;
	float packet_loss;
	CString isVpn;

	ShellHandler sh_speed_test;
	ShellHandler sh_upload_report;
	BOOL uploading;
protected:
	afx_msg LRESULT OnUpdateCityIsp(WPARAM wParam, LPARAM lParam);
	afx_msg LRESULT OnUpdateSpeedTest(WPARAM wParam, LPARAM lParam);
	afx_msg LRESULT OnChildWndResize(WPARAM wParam, LPARAM lParam);
public:
	afx_msg HBRUSH OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor);
	afx_msg void OnSize(UINT nType, int cx, int cy);
	CComboBox play_result;
	CComboBox play_result_screen;
	CComboBox play_result_finish;
protected:
	afx_msg LRESULT OnSetPlayFirstFrame(WPARAM wParam, LPARAM lParam);
public:
	afx_msg void OnBnClickedButton1();
protected:
	afx_msg LRESULT OnUploadReportFinish(WPARAM wParam, LPARAM lParam);
};
