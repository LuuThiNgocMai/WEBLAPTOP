import streamlit as st
import time
import os
import pandas as pd
import json
import io
from pathlib import Path
from parsers import parse_excel, parse_csv
from utils.normalizer import normalize_testcase
from ai import enrich_test_data
from core.test_runner import run_test_case
from core.driver_factory import create_driver

# --- Configuration & Paths ---
UPLOAD_DIR = Path("Testing/uploads")
DATA_DIR = Path("Testing/data")
REPORT_DIR = Path("Testing/reports")
EXPORT_DIR = Path("Testing/exports")
SCREENSHOT_DIR = Path("Testing/screenshots")

for d in [UPLOAD_DIR, DATA_DIR, REPORT_DIR, EXPORT_DIR, SCREENSHOT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

STANDARDIZED_PATH = DATA_DIR / "testcase_chuan_hoa.json"
AI_DATA_PATH = DATA_DIR / "testcase_ai.json"
REVIEWED_PATH = DATA_DIR / "testcase_review.json"
GLOBAL_REPORT_CSV = REPORT_DIR / "ket_qua_chay_test.csv"

# --- Utility Functions ---
def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(path):
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# --- Custom Styling ---
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .status-box { padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .success-box { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .warning-box { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
    .error-box { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; }
    .metric-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; }
</style>
""", unsafe_allow_html=True)

def render_execution_report(results):
    if not results:
        return

    st.header("Báo cáo Thực thi Loạt Test Case")
    
    # Summary Metrics
    total_tcs = len(results)
    passed_tcs = sum(1 for r in results if r['trang_thai_cuoi'] == 'THÀNH CÔNG')
    failed_tcs = total_tcs - passed_tcs
    
    # Calculate total duration sum (strings like '1.23s')
    try:
        total_duration = sum(float(r['tong_thoi_gian_chay'].replace('s', '')) for r in results)
    except:
        total_duration = 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Tổng số Test Case", total_tcs)
    with m2:
        st.metric("Thành công", passed_tcs, delta=f"{(passed_tcs/total_tcs*100):.1f}%" if total_tcs > 0 else None)
    with m3:
        st.metric("Thất bại", failed_tcs, delta=f"-{failed_tcs}" if failed_tcs > 0 else None, delta_color="inverse")
    with m4:
        st.metric("Tổng thời gian", f"{total_duration:.2f}s")

    st.markdown("### Chi tiết Kết quả")
    
    for res in results:
        status_text = "[PASS]" if res['trang_thai_cuoi'] == "THÀNH CÔNG" else "[FAIL]"
        with st.expander(f"{status_text} {res['ma_tc']} - {res['ten_test_case']}"):
            # TC Header Info
            c1, c2, c3 = st.columns([1, 1, 1])
            c1.write(f"**Trạng thái:** {res['trang_thai_cuoi']}")
            c2.write(f"**Số bước Đạt/Tổng:** {res['so_buoc_pass']}/{res['tong_so_buoc']}")
            c3.write(f"**Thời gian chạy:** {res['tong_thoi_gian_chay']}")
            
            if res['trang_thai_cuoi'] == "THẤT BẠI":
                st.error(f"**Lỗi:** {res['thong_bao_loi_cuoi_cung']}")
                if res['screenshot_loi_cuoi_cung'] and os.path.exists(res['screenshot_loi_cuoi_cung']):
                    st.image(res['screenshot_loi_cuoi_cung'], caption=f"Failure Screenshot for {res['ma_tc']}", use_container_width=True)
            
            # Step Table
            if res.get('chi_tiet_buoc'):
                st.markdown("**Chi tiết các bước:**")
                step_df = pd.DataFrame(res['chi_tiet_buoc'])
                # Select and rename columns for display
                display_cols = {
                    'so_buoc': 'Bước',
                    'noi_dung_buoc': 'Nội dung',
                    'trang_thai': 'Trạng thái',
                    'thong_bao_loi': 'Thông báo lỗi'
                }
                # Only keep existing columns
                cols_to_show = [c for c in display_cols.keys() if c in step_df.columns]
                st.table(step_df[cols_to_show].rename(columns=display_cols))

    # --- New: Unsupported Action Warning ---
    has_unsupported = any("not supported in" in str(res.get('thong_bao_loi_cuoi_cung', '')).lower() for res in results)
    if has_unsupported:
        st.markdown("---")
        st.info("""
        ### Phát hiện hành động chưa được hỗ trợ!
        Dường như có một số bước trong Test Case của bạn chưa được viết code logic (Action not supported). Để hoàn thiện kịch bản, bạn hãy làm theo các bước sau:
        1. **Mở Katalon Recorder** (tiện ích mở rộng trên Chrome/Edge).
        2. Nhấn **Record** và thực hiện thủ công các bước cho Test Case đầu tiên trên trình duyệt.
        3. Dựa trên script mà Katalon đã lưu lại (các lệnh `click`, `type`, `select`...), bạn có thể xác định chính xác các selector và hành động cần thiết.
        4. Sau đó, hãy cung cấp thông tin/script này cho tôi để tôi bổ sung các Action còn thiếu vào code và chạy tự động cho các case còn lại.
        """)

    if st.button("Xóa kết quả thực hiện"):
        if 'final_results' in st.session_state:
            del st.session_state['final_results']
        st.rerun()

def main():
    st.set_page_config(page_title="Hệ thống Automation Toàn diện", layout="wide")
    
    # --- Sidebar Header & Project Status ---
    with st.sidebar:
        st.title("Điều khiển Hệ thống")
        st.markdown("---")
        
        # Simple State Indicator
        norm_data = load_json(STANDARDIZED_PATH)
        ai_data = load_json(AI_DATA_PATH)
        rev_data = load_json(REVIEWED_PATH)
        
        st.info(f"Nguồn: {len(norm_data)} TC")
        st.success(f"AI Xong: {len(ai_data)} TC")
        st.warning(f"Đã Duyệt: {len(rev_data)} TC")
        
        st.markdown("---")
        if st.button("Reset Toàn bộ Dữ liệu"):
            for f in [STANDARDIZED_PATH, AI_DATA_PATH, REVIEWED_PATH]:
                if f.exists(): f.unlink()
            st.rerun()

    st.title("Hệ thống Quản lý & Automation Đồng nhất")
    st.caption("Khung làm việc toàn diện cho Web Automation: từ Excel đến Báo cáo Thực thi")
    st.markdown("---")

    # --- Main Tabs Layout ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "Dự án & Chuẩn hóa", 
        "Trí tuệ Nhân tạo AI", 
        "Automation Studio", 
        "Báo cáo Analytics"
    ])

    # --- TAB 1: Dự án & Chuẩn hóa ---
    with tab1:
        st.header("Bước 1: Tải lên & Chuẩn hóa Dữ liệu")
        
        uploaded_file = st.file_uploader("Tải lên tệp Excel/CSV Test Case", type=["xlsx", "csv"])
        if uploaded_file:
            if st.button("Thực hiện Chuẩn hóa", use_container_width=True):
                fp = UPLOAD_DIR / uploaded_file.name
                with open(fp, "wb") as f: f.write(uploaded_file.getbuffer())
                ext = fp.suffix.lower()
                raw = parse_excel(str(fp)) if ext == ".xlsx" else parse_csv(str(fp))
                normalized = [normalize_testcase(r, i) for i, r in enumerate(raw)]
                save_json(STANDARDIZED_PATH, normalized)
                st.success(f"Đã chuẩn hóa {len(normalized)} test case!")
                st.rerun()

        st.markdown("---")
        if norm_data:
            st.subheader("Dữ liệu hiện tại")
            df = pd.DataFrame([{ 
                "STT": t['stt'], 
                "Mã TC": t['ma_tc'], 
                "Tên Test Case": t['ten_test_case'],
                "Mô tả": t['mo_ta'],
                "ĐK Tiên quyết": t['dieu_kien_tien_quyet'],
                "Dữ liệu gốc": t['du_lieu_test_goc'],
                "KQ Mong đợi": t['ket_qua_mong_doi'],
                "Ghi chú": t['ghi_chu_tu_dong_hoa']
            } for t in norm_data])
            
            # Tự động tính chiều cao để hạn chế scroll dọc nếu ít dữ liệu
            calc_height = min(len(df) * 35 + 100, 800)
            st.dataframe(df, use_container_width=True, hide_index=True, height=calc_height)
            
            with st.expander("Xem chi tiết bước của toàn bộ Test Case"):
                for tc in norm_data:
                    st.markdown(f"**{tc['ma_tc']} - {tc['ten_test_case']}**")
                    steps_text = "\n".join([f"{s['so_buoc']}. {s['noi_dung']}" for s in tc.get('danh_sach_buoc', [])])
                    st.code(steps_text)
        else:
            st.info("Chưa có dữ liệu. Vui lòng upload file để bắt đầu.")

    # --- TAB 2: Trí tuệ Nhân tạo AI ---
    with tab2:
        st.header("Bước 2: AI Làm giàu Dữ liệu Test")
        if not norm_data:
            st.warning("Vui lòng hoàn thành Bước 1 trước.")
        else:
            # --- AI State Management ---
            if 'ai_progress' not in st.session_state:
                st.session_state.ai_progress = {"index": 0, "processed": [], "is_running": False, "engine": "Google Gemini"}

            # --- Dialog for Fallback ---
            @st.dialog("Phát hiện sự cố AI")
            def confirm_fallback():
                st.write("Đã có sự cố xảy ra với Google Gemini. Bạn có muốn chuyển sang **Mock AI** để tiếp tục hoàn thành các test case còn lại không?")
                c1, c2 = st.columns(2)
                if c1.button("Sử dụng Mock AI", use_container_width=True):
                    st.session_state.ai_progress["engine"] = "Mock AI"
                    st.rerun()
                if c2.button("Dừng lại", use_container_width=True):
                    st.session_state.ai_progress["is_running"] = False
                    st.rerun()

            st.subheader("Cấu hình xử lý AI")
            c_ai_op1, c_ai_op2 = st.columns([1, 1])
            with c_ai_op1:
                ai_mode = st.radio("Chế độ xử lý:", ["Tất cả (Batch)", "Từng Test Case (Single)"])
                selected_engine = st.radio("Công cụ AI:", ["Mock AI", "Google Gemini"], 
                                         index=1 if st.session_state.ai_progress["engine"] == "Google Gemini" else 0)
            
            with c_ai_op2:
                # Update engine in session state if user manually changes it
                st.session_state.ai_progress["engine"] = selected_engine
                
                if st.button("Bắt đầu/Tiếp tục xử lý AI", type="primary", use_container_width=True):
                    st.session_state.ai_progress["is_running"] = True
                    st.rerun()

            # --- Running Logic ---
            if st.session_state.ai_progress["is_running"]:
                current_engine = st.session_state.ai_progress["engine"]
                with st.spinner(f"Đang xử lý bằng {current_engine}... (TC {st.session_state.ai_progress['index']+1}/{len(norm_data)})"):
                    for i in range(st.session_state.ai_progress["index"], len(norm_data)):
                        tc = norm_data[i]
                        try:
                            result = enrich_test_data(tc, engine=current_engine)
                            tc.update(result)
                            st.session_state.ai_progress["processed"].append(tc)
                            st.session_state.ai_progress["index"] = i + 1
                        except Exception as e:
                            confirm_fallback()
                            st.stop()
                    
                    # Finalize
                    save_json(AI_DATA_PATH, st.session_state.ai_progress["processed"])
                    st.session_state.ai_progress["is_running"] = False
                    st.session_state.ai_progress["index"] = 0
                    st.session_state.ai_progress["processed"] = []
                    st.success(f"Đã làm giàu hoàn tất bằng {current_engine}!")
                    st.balloons()
                    st.rerun()

            st.markdown("---")
            st.subheader("Dữ liệu đã AI-fied")
            if ai_data:
                # Chuẩn bị dữ liệu hiển thị kèm theo Data AI
                display_list = []
                for t in ai_data:
                    ai_payload = t.get('du_lieu_test_ai', {})
                    ai_data_str = json.dumps(ai_payload, ensure_ascii=False) if ai_payload else "Chưa có"
                    
                    display_list.append({
                        "Mã TC": t['ma_tc'],
                        "Tên Test Case": t['ten_test_case'],
                        "Dữ liệu AI (JSON)": ai_data_str,
                        "Trạng thái AI": "Sẵn sàng" if ai_payload else "Chờ xử lý",
                        "Mô tả": t['mo_ta'],
                        "KQ Mong đợi": t['ket_qua_mong_doi']
                    })
                
                ai_df = pd.DataFrame(display_list)
                st.dataframe(ai_df, use_container_width=True, hide_index=True, height=500)
                
                if st.button("Duyệt tất cả (Review & Approve)", use_container_width=True):
                    save_json(REVIEWED_PATH, ai_data)
                    st.success("Đã chuyển toàn bộ Test Case sang hàng chờ Automation!")
                    st.balloons()
                    time.sleep(1) # Đợi một chút để hiệu ứng hiện ra
                    st.rerun()
            else:
                st.info("Chưa có dữ liệu AI. Hãy click 'Bắt đầu xử lý AI'.")

    # --- TAB 3: Automation Studio ---
    with tab3:
        st.header("Bước 3: Điều khiển Thực thi")
        if not rev_data:
            st.error("Chưa có Test Case nào được duyệt. Hãy quay lại Tab AI.")
        else:
            c_env1, c_env2 = st.columns([1, 1])
            with c_env1:
                st.subheader("URL & Xác thực")
                target_url = st.text_input("URL mục tiêu:", value="https://localhost:44396")
                use_auth = st.checkbox("Sử dụng Basic Auth?")
                auth_info = {"use_auth": use_auth}
                if use_auth:
                    auth_info['username'] = st.text_input("Username:")
                    auth_info['password'] = st.text_input("Password:", type="password")
            
            with c_env2:
                st.subheader("Hàng chờ Test Case")
                tc_options = [f"{t['ma_tc']} - {t['ten_test_case']}" for t in rev_data]
                to_run = st.multiselect("Chọn TC để chạy:", tc_options, default=tc_options)
                show_browser = st.checkbox("Quan sát quá trình chạy (Mở trình duyệt)", value=True)
                headless = not show_browser
                keep_open = st.checkbox("Giữ trình duyệt mở sau khi chạy", value=False)
                
                st.markdown("---")
                single_browser = st.checkbox("Sử dụng 1 trình duyệt duy nhất (Single Browser)", value=True, help="Tất cả test case sẽ chạy trong một cửa sổ duy nhất để tăng tốc độ.")
                if single_browser:
                    clear_cookies = st.checkbox("Xóa cookie giữa các test case", value=True)
                else:
                    clear_cookies = False
            
            if st.button("EXECUTE AUTOMATION", type="primary", use_container_width=True):
                if not to_run:
                    st.warning("Vui lòng chọn ít nhất 1 test case!")
                else:
                    # Clear previous results before starting
                    if 'final_results' in st.session_state:
                        del st.session_state['final_results']
                    
                    status_area = st.empty()
                    main_bar = st.progress(0)
                    results = []
                    
                    env_config = {"target_url": target_url, "auth": auth_info}
                    
                    batch_driver = None
                    try:
                        if single_browser:
                            status_area.info("Đang khởi tạo trình duyệt dùng chung...")
                            batch_driver = create_driver(headless=headless)
                            
                        for i, selection in enumerate(to_run):
                            sm = selection.split(" - ")[0]
                            tc_node = next(it for it in rev_data if it['ma_tc'] == sm)
                            status_area.info(f"Đang chạy {sm}: {tc_node['ten_test_case']}")
                            
                            # Điều hướng chỉ cho TC đầu tiên (nếu dùng single browser)
                            # Hoặc cho mọi TC nếu dùng nhiều trình duyệt
                            should_nav = (i == 0) if single_browser else True
                            
                            # Xóa cookie nếu được yêu cầu (trừ TC đầu tiên vì nó vừa mở)
                            should_clear = clear_cookies if (single_browser and i > 0) else False

                            # EXECUTE
                            res = run_test_case(
                                tc_node, 
                                headless=headless, 
                                env_config=env_config, 
                                keep_open=keep_open if not single_browser else True, # Giữ mở để TC sau chạy tiếp
                                existing_driver=batch_driver,
                                should_navigate=should_nav,
                                clear_cookies=should_clear
                            )
                            results.append(res)
                            
                            main_bar.progress((i + 1) / len(to_run))
                            
                    except Exception as e:
                        st.error(f"Lỗi trong quá trình thực thi: {str(e)}")
                    finally:
                        # Đóng trình duyệt sau khi xong batch nếu dùng single browser
                        if single_browser and batch_driver and not keep_open:
                            batch_driver.quit()
                    
                    status_area.success(f"Đã hoàn thành {len(results)} Test Case!")
                    st.session_state['final_results'] = results

            if 'final_results' in st.session_state:
                render_execution_report(st.session_state['final_results'])

    # --- TAB 4: Báo cáo Analytics ---
    with tab4:
        st.header("Bước 4: Bảng Điều khiển Thông minh")
        if not GLOBAL_REPORT_CSV.exists():
            st.info("Chưa có dữ liệu báo cáo lịch sử.")
        else:
            df_rep = pd.read_csv(GLOBAL_REPORT_CSV)
            
            # Metrics
            met1, met2, met3 = st.columns(3)
            met1.metric("Tổng lần chạy", len(df_rep))
            pass_count = len(df_rep[df_rep['Trạng thái'] == 'PASSED'])
            met2.metric("Tỷ lệ thành công", f"{(pass_count/len(df_rep)*100):.1f}%")
            met3.metric("Tổng số bước", int(df_rep['Tổng Bước'].sum()))

            st.markdown("---")
            st.subheader("Lịch sử thực thi")
            st.dataframe(df_rep, use_container_width=True)
            
            # Export Centre
            st.subheader("Export Center")
            e_c1, e_c2 = st.columns(2)
            with e_c1:
                csv_bytes = df_rep.to_csv(index=False).encode('utf-8-sig')
                st.download_button("Tải Báo cáo CSV", csv_bytes, "report.csv", "text/csv")
            with e_c2:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_rep.to_excel(writer, index=False, sheet_name='Tổng hợp')
                st.download_button("Tải Báo cáo Excel", output.getvalue(), "report.xlsx", "application/vnd.ms-excel")

if __name__ == "__main__":
    main()
