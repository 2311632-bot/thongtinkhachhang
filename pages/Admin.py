import streamlit as st
import pandas as pd
from database import get_connection


# =========================
# CẤU HÌNH TRANG
# =========================

st.set_page_config(
    page_title="Trang quản trị SmartCare CRM",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 SMARTCARE CRM - TRANG QUẢN TRỊ")

st.write(
    "Quản lý khách hàng tiềm năng và theo dõi lịch chăm sóc / tái tư vấn."
)


# =========================
# TÀI KHOẢN ADMIN
# =========================

USERNAME = "admin"
PASSWORD = "123456"


# =========================
# SESSION ĐĂNG NHẬP
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =====================================================
# FORM ĐĂNG NHẬP
# =====================================================

if not st.session_state.logged_in:

    st.subheader("🔑 Đăng nhập quản trị")

    username = st.text_input(
        "Tên đăng nhập"
    )

    password = st.text_input(
        "Mật khẩu",
        type="password"
    )

    if st.button("🔐 Đăng nhập"):

        if username == USERNAME and password == PASSWORD:

            st.session_state.logged_in = True

            st.success(
                "✅ Đăng nhập thành công!"
            )

            st.rerun()

        else:

            st.error(
                "❌ Sai tên đăng nhập hoặc mật khẩu."
            )


# =====================================================
# TRANG QUẢN TRỊ
# =====================================================

else:

    # =========================
    # ĐĂNG XUẤT
    # =========================

    col_logout, col_space = st.columns([1, 6])

    with col_logout:

        if st.button("🚪 Đăng xuất"):

            st.session_state.logged_in = False
            st.rerun()


    # =====================================================
    # LẤY DỮ LIỆU DATABASE
    # =====================================================

    try:

        conn = get_connection()
        cursor = conn.cursor()


        # =========================
        # LẤY KHÁCH HÀNG
        # =========================

        sql_khach_hang = """
        SELECT
            ma_khach_hang,
            ho_ten,
            so_dien_thoai,
            khu_vuc,
            loai_khach_hang,
            nhu_cau,
            ghi_chu,
            ngay_tao
        FROM khach_hang_tiem_nang
        ORDER BY ma_khach_hang DESC
        """

        cursor.execute(sql_khach_hang)

        data_khach_hang = cursor.fetchall()


        columns_khach_hang = [
            "Mã khách hàng",
            "Họ tên",
            "Số điện thoại",
            "Khu vực",
            "Loại khách hàng",
            "Nhu cầu",
            "Ghi chú",
            "Ngày tạo"
        ]


        df_khach_hang = pd.DataFrame(
            data_khach_hang,
            columns=columns_khach_hang
        )


        # =========================
        # LẤY LỊCH HẸN
        # =========================

        sql_lich = """
        SELECT
            l.ma_lich,
            l.ma_khach_hang,
            k.ho_ten,
            k.so_dien_thoai,
            l.ngay_hen,
            l.gio_hen,
            l.noi_dung_tu_van,
            l.hinh_thuc_lien_he,
            l.trang_thai,
            l.ghi_chu
        FROM lich_cham_soc l
        INNER JOIN khach_hang_tiem_nang k
        ON l.ma_khach_hang = k.ma_khach_hang
        ORDER BY l.ngay_hen DESC, l.gio_hen DESC
        """

        cursor.execute(sql_lich)

        data_lich = cursor.fetchall()


        columns_lich = [
            "Mã lịch",
            "Mã khách hàng",
            "Họ tên",
            "Số điện thoại",
            "Ngày hẹn",
            "Giờ hẹn",
            "Nội dung tư vấn",
            "Hình thức liên hệ",
            "Trạng thái",
            "Ghi chú"
        ]


        df_lich = pd.DataFrame(
            data_lich,
            columns=columns_lich
        )


        cursor.close()
        conn.close()


        # =====================================================
        # THỐNG KÊ
        # =====================================================

        st.divider()

        st.subheader("📊 Thống kê tổng quan")

        col1, col2, col3, col4 = st.columns(4)


        # Tổng khách hàng
        col1.metric(
            "👥 Tổng khách hàng",
            len(df_khach_hang)
        )


        # Khách hàng mới
        if not df_khach_hang.empty:

            so_khach_moi = len(
                df_khach_hang[
                    df_khach_hang[
                        "Loại khách hàng"
                    ] == "Khách hàng mới"
                ]
            )

        else:

            so_khach_moi = 0


        col2.metric(
            "🆕 Khách hàng mới",
            so_khach_moi
        )


        # Khách hàng cũ
        if not df_khach_hang.empty:

            so_khach_cu = len(
                df_khach_hang[
                    df_khach_hang[
                        "Loại khách hàng"
                    ] == "Khách hàng cũ"
                ]
            )

        else:

            so_khach_cu = 0


        col3.metric(
            "🔄 Khách hàng quay lại",
            so_khach_cu
        )


        # Tổng lịch
        col4.metric(
            "📅 Tổng lịch hẹn",
            len(df_lich)
        )


        # =====================================================
        # DANH SÁCH KHÁCH HÀNG
        # =====================================================

        st.divider()

        st.subheader(
            "👥 Danh sách khách hàng tiềm năng"
        )


        # Tìm kiếm
        tim_kiem = st.text_input(
            "🔎 Tìm kiếm khách hàng",
            placeholder="Nhập tên hoặc số điện thoại..."
        )


        df_hien_thi = df_khach_hang.copy()


        if tim_kiem:

            df_hien_thi = df_hien_thi[
                df_hien_thi["Họ tên"]
                .astype(str)
                .str.contains(
                    tim_kiem,
                    case=False,
                    na=False
                )
                |
                df_hien_thi["Số điện thoại"]
                .astype(str)
                .str.contains(
                    tim_kiem,
                    case=False,
                    na=False
                )
            ]


        if not df_hien_thi.empty:

            st.dataframe(
                df_hien_thi,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Chưa tìm thấy khách hàng."
            )


        # =====================================================
        # DANH SÁCH LỊCH HẸN
        # =====================================================

        st.divider()

        st.subheader(
            "📅 Lịch chăm sóc / tái tư vấn"
        )


        # Lọc trạng thái
        trang_thai_loc = st.selectbox(
            "Lọc theo trạng thái",
            [
                "Tất cả",
                "Chưa liên hệ",
                "Đã liên hệ",
                "Đã tư vấn",
                "Hẹn lại",
                "Hoàn thành"
            ]
        )


        df_lich_hien_thi = df_lich.copy()


        if trang_thai_loc != "Tất cả":

            df_lich_hien_thi = df_lich_hien_thi[
                df_lich_hien_thi[
                    "Trạng thái"
                ] == trang_thai_loc
            ]


        # Hiển thị lịch
        if not df_lich_hien_thi.empty:

            st.dataframe(
                df_lich_hien_thi,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Chưa có lịch phù hợp."
            )


        # =====================================================
        # CẬP NHẬT TRẠNG THÁI LỊCH
        # =====================================================

        st.divider()

        st.subheader(
            "✏️ Cập nhật trạng thái lịch hẹn"
        )


        if not df_lich.empty:

            danh_sach_ma_lich = (
                df_lich["Mã lịch"]
                .tolist()
            )


            ma_lich_chon = st.selectbox(
                "Chọn mã lịch cần cập nhật",
                danh_sach_ma_lich
            )


            thong_tin_lich = df_lich[
                df_lich["Mã lịch"]
                == ma_lich_chon
            ].iloc[0]


            st.write(
                f"**Khách hàng:** {thong_tin_lich['Họ tên']}"
            )

            st.write(
                f"**Ngày hẹn:** {thong_tin_lich['Ngày hẹn']}"
            )


            trang_thai_moi = st.selectbox(
                "Trạng thái mới",
                [
                    "Chưa liên hệ",
                    "Đã liên hệ",
                    "Đã tư vấn",
                    "Hẹn lại",
                    "Hoàn thành"
                ]
            )


            if st.button(
                "💾 Cập nhật trạng thái"
            ):

                try:

                    conn = get_connection()
                    cursor = conn.cursor()


                    sql_update = """
                    UPDATE lich_cham_soc
                    SET trang_thai = %s
                    WHERE ma_lich = %s
                    """


                    cursor.execute(
                        sql_update,
                        (
                            trang_thai_moi,
                            ma_lich_chon
                        )
                    )


                    conn.commit()

                    cursor.close()
                    conn.close()


                    st.success(
                        "🎉 Cập nhật trạng thái thành công!"
                    )

                    st.rerun()


                except Exception as e:

                    st.error(
                        f"❌ Lỗi khi cập nhật: {e}"
                    )


        else:

            st.info(
                "Chưa có lịch hẹn để cập nhật."
            )


    except Exception as e:

        st.error(
            f"❌ Lỗi hệ thống: {e}"
        )
