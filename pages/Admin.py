import streamlit as st
import pandas as pd
from database import get_connection


# =========================
# CẤU HÌNH TRANG
# =========================

st.set_page_config(
    page_title="Trang quản trị",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 TRANG QUẢN TRỊ")
st.write(
    "Quản lý khách hàng tiềm năng và lịch chăm sóc khách hàng."
)


# =========================
# TÀI KHOẢN ADMIN
# =========================

USERNAME = "admin"
PASSWORD = "123456"


# =========================
# KHỞI TẠO SESSION
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =========================
# FORM ĐĂNG NHẬP
# =========================

if not st.session_state.logged_in:

    st.subheader("🔑 Đăng nhập quản trị")

    username = st.text_input("Tên đăng nhập")

    password = st.text_input(
        "Mật khẩu",
        type="password"
    )

    if st.button("🔐 Đăng nhập"):

        if username == USERNAME and password == PASSWORD:

            st.session_state.logged_in = True

            st.success("✅ Đăng nhập thành công!")

            st.rerun()

        else:

            st.error(
                "❌ Sai tên đăng nhập hoặc mật khẩu."
            )


# =========================
# TRANG QUẢN TRỊ
# =========================

else:

    col_title, col_logout = st.columns([6, 1])

    with col_logout:

        if st.button("🚪 Đăng xuất"):

            st.session_state.logged_in = False

            st.rerun()


    # =========================
    # LẤY DỮ LIỆU
    # =========================

    try:

        conn = get_connection()
        cursor = conn.cursor()


        # =========================
        # LẤY DANH SÁCH KHÁCH HÀNG
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
        # HIỂN THỊ MÃ KHÁCH HÀNG
        # =========================

        if not df_khach_hang.empty:

            df_khach_hang["Mã khách hàng"] = (
                df_khach_hang["Mã khách hàng"]
                .apply(lambda x: f"KH{int(x):03d}")
            )


        # =========================
        # LẤY DANH SÁCH LỊCH
        # =========================

        sql_lich = """
        SELECT
            l.ma_lich,
            k.ma_khach_hang,
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
        ORDER BY l.ngay_hen ASC, l.gio_hen ASC
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


        # =========================
        # HIỂN THỊ MÃ KHÁCH HÀNG TRONG LỊCH
        # =========================

        if not df_lich.empty:

            df_lich["Mã khách hàng"] = (
                df_lich["Mã khách hàng"]
                .apply(lambda x: f"KH{int(x):03d}")
            )


        # =========================
        # ĐÓNG DATABASE
        # =========================

        cursor.close()
        conn.close()


        # =========================
        # THỐNG KÊ
        # =========================

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
                    df_khach_hang["Loại khách hàng"]
                    == "Khách hàng mới"
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
                    df_khach_hang["Loại khách hàng"]
                    == "Khách hàng cũ"
                ]
            )

        else:

            so_khach_cu = 0


        col3.metric(
            "🔄 Khách hàng quay lại",
            so_khach_cu
        )


        # Tổng lịch hẹn

        col4.metric(
            "📅 Lịch chăm sóc",
            len(df_lich)
        )


        # =========================
        # DANH SÁCH KHÁCH HÀNG
        # =========================

        st.divider()

        st.subheader(
            "👥 Danh sách khách hàng tiềm năng"
        )


        if not df_khach_hang.empty:

            # Tìm kiếm khách hàng
            tim_kiem = st.text_input(
                "🔎 Tìm kiếm theo tên hoặc số điện thoại"
            )


            df_hien_thi = df_khach_hang.copy()


            if tim_kiem:

                mask = (
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
                )

                df_hien_thi = df_hien_thi[mask]


            st.dataframe(
                df_hien_thi,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "📭 Chưa có khách hàng nào trong hệ thống."
            )


        # =========================
        # DANH SÁCH LỊCH HẸN
        # =========================

        st.divider()

        st.subheader(
            "📅 Danh sách lịch chăm sóc / tái tư vấn"
        )


        if not df_lich.empty:

            st.dataframe(
                df_lich,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "📭 Chưa có lịch chăm sóc nào."
            )


        # =========================
        # LÀM MỚI DỮ LIỆU
        # =========================

        st.divider()

        if st.button("🔄 Làm mới dữ liệu"):

            st.rerun()


    except Exception as e:

        st.error(
            f"❌ Lỗi hệ thống: {e}"
        )
