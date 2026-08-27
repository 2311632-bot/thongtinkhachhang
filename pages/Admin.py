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
st.write("Quản lý khách hàng tiềm năng và lịch chăm sóc khách hàng.")


# =========================
# TÀI KHOẢN QUẢN TRỊ
# =========================

USERNAME = "admin"
PASSWORD = "123456"


# =========================
# ĐĂNG NHẬP
# =========================

username = st.text_input("Tên đăng nhập")

password = st.text_input(
    "Mật khẩu",
    type="password"
)

login = st.button("Đăng nhập")


# =========================
# KIỂM TRA ĐĂNG NHẬP
# =========================

if login:

    if username == USERNAME and password == PASSWORD:

        st.success("✅ Đăng nhập thành công!")

        # =========================
        # KẾT NỐI DATABASE
        # =========================

        try:

            conn = get_connection()

            # =========================
            # DANH SÁCH KHÁCH HÀNG
            # =========================

            st.subheader("👥 Danh sách khách hàng tiềm năng")

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

            df_khach_hang = pd.read_sql(
                sql_khach_hang,
                conn
            )

            st.dataframe(
                df_khach_hang,
                use_container_width=True
            )


            # =========================
            # LỊCH CHĂM SÓC
            # =========================

            st.divider()

            st.subheader("📅 Lịch chăm sóc / tái tư vấn")

            sql_lich = """
            SELECT
                l.ma_lich,
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
            ORDER BY
                l.ngay_hen ASC,
                l.gio_hen ASC
            """

            df_lich = pd.read_sql(
                sql_lich,
                conn
            )

            st.dataframe(
                df_lich,
                use_container_width=True
            )


            # =========================
            # THỐNG KÊ
            # =========================

            st.divider()
          st.subheader("📊 Thống kê")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Tổng khách hàng",
                    len(df_khach_hang)
                )

            with col2:
                st.metric(
                    "Khách hàng mới",
                    len(
                        df_khach_hang[
                            df_khach_hang["loai_khach_hang"]
                            == "Khách hàng mới"
                        ]
                    )
                )

            with col3:
                st.metric(
                    "Lịch chăm sóc",
                    len(df_lich)
                )

            conn.close()

        except Exception as e:

            st.error(
                f"Lỗi khi lấy dữ liệu: {e}"
            )

    else:

        st.error(
            "❌ Sai tên đăng nhập hoặc mật khẩu."
        )
