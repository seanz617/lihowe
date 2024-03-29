
// MFCApplication1Dlg.h: 头文件
//

#pragma once

#include "PlaySlider.h"
#include "TestReport.h"
#include "TestSettings.h"
#include "TestWget.h"

class CMFCApplication1Dlg : public CDialogEx
{
public:
	CMFCApplication1Dlg(CWnd* pParent = nullptr);	// 标准构造函数

#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_MFCAPPLICATION1_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 支持

protected:
	HICON m_hIcon;

	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()

public:
	struct TestConfig tc;
	BOOL LoadConfig();

	CString m_VideoPath;
	libvlc_instance_t*     p_instance;
	libvlc_media_player_t* p_media_player;
	libvlc_media_t*        p_media;
	HANDLE p_player_mutex;

	afx_msg void OnStnClickedSurface();
	afx_msg void OnBnClickedOk();
	afx_msg void OnBnClickedCancel();
	afx_msg void OnDestroy();
	afx_msg void OnBnClickedButton2();
	afx_msg void OnBnClickedButton4();
	afx_msg void OnBnClickedButton3();
	afx_msg void OnNMCustomdrawSlider1(NMHDR *pNMHDR, LRESULT *pResult);
	afx_msg void OnTimer(UINT_PTR nIDEvent);
	afx_msg HBRUSH OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor);
	afx_msg void OnSize(UINT nType, int cx, int cy);
	afx_msg void OnTcnSelchangeTab1(NMHDR *pNMHDR, LRESULT *pResult);
	afx_msg LRESULT OnUserChangePos(WPARAM wParam, LPARAM lParam);

	void update_play_progress();
	void OnEndReached(const libvlc_event_t* p_event, void* p_data);
	void ReSize(int nID,float ban);
	void ReSizeChild(float ban);

	CComboBox play_list;
	PlaySlider play_progress;
	CBrush m_brush;
	CBrush m_black_brush;
	BOOL change_flag;
	LONG start_btn_width;
	LONG pause_btn_width;
	LONG play_start_time;
	LONG play_end_time;

	CTabCtrl info_tab;
	CDialogEx* tabs[2];
	TestReport dlg_test_report;
	TestSettings dlg_test_settings;
	TestWget dlg_test_wget;
	BOOL stop_timer = FALSE;
protected:
	afx_msg LRESULT OnPlayStoped(WPARAM wParam, LPARAM lParam);
public:
	afx_msg void OnCbnSelchangeCombo1();
protected:
	afx_msg LRESULT OnPlayFirstFrame(WPARAM wParam, LPARAM lParam);
};
