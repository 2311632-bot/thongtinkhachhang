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

    col1, col2 = st.columns([6, 1])

    with col2:

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
        # DANH SÁCH KHÁCH HÀNG
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
        # HIỂN THỊ MÃ KHÁCH HÀNG KH001
        # =========================

        if not df_khach_hang.empty:

            df_khach_hang["Mã khách hàng"] = (
                df_khach_hang["Mã khách hàng"]
                .apply(lambda x: f"KH{int(x):03d}")
            )


        # =========================
        # DANH SÁCH LỊCH HẸN
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
        # MÃ KHÁCH HÀNG TRONG LỊCH
        # =========================

        if not df_lich.empty:

            df_lich["Mã khách hàng"] = (
                df_lich["Mã khách hàng"]
                .apply(lambda x: f"KH{int(x):03d}")
            )


        cursor.close()
        conn.close()


        # =========================
        # THỐNG KÊ
        # =========================

        st.divider()

        st.subheader("📊 Thống kê tổng quan")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "👥 Tổng khách hàng",
            len(df_khach_hang)
        )


        if not df_khach_hang.empty:

            so_khach_moi = len(
                df_khach_hang[
                    df_khach_hang["Loại khách hàng"]
                    == "Khách hàng mới"
                ]
            )

            so_khach_cu = len(
                df_khach_hang[
                    df_khach_hang["Loại khách hàng"]
                    == "Khách hàng cũ"
                ]
            )

        else:

            so_khach_moi = 0
            so_khach_cu = 0


        col2.metric(
            "🆕 Khách hàng mới",
            so_khach_moi
        )

        col3.metric(
            "🔄 Khách hàng quay lại",
            so_khach_cu
        )

        col4.metric(
            "📅 Tổng lịch hẹn",
            len(df_lich)
        )


        # =========================
        # DANH SÁCH KHÁCH HÀNG
        # =========================

        st.divider()

        st.subheader("👥 Danh sách khách hàng tiềm năng")


        if not df_khach_hang.empty:

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
                "📭 Chưa có khách hàng nào."
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


            # =========================
            # CẬP NHẬT TRẠNG THÁI
            # =========================

            st.divider()

            st.subheader(
                "✏️ Cập nhật trạng thái lịch hẹn"
            )

            # Danh sách mã lịch
            danh_sach_ma_lich = df_lich[
                "Mã lịch"
            ].tolist()

            ma_lich_chon = st.selectbox(
                "Chọn lịch hẹn cần cập nhật",
                danh_sach_ma_lich
            )


            # Tìm thông tin lịch được chọn
            lich_hien_tai = df_lich[
                df_lich["Mã lịch"] == ma_lich_chon
            ].iloc[0]


            st.info(
                f"👤 Khách hàng: {lich_hien_tai['Họ tên']} | "
                f"🆔 Mã khách hàng: {lich_hien_tai['Mã khách hàng']} | "
                f"📌 Trạng thái hiện tại: "
                f"{lich_hien_tai['Trạng thái']}"
            )


            danh_sach_trang_thai = [
                "Chưa liên hệ",
                "Đã liên hệ",
                "Đã tư vấn",
                "Hẹn lại",
                "Hoàn thành"
            ]


            # Xác định trạng thái hiện tại
            trang_thai_hien_tai = (
                lich_hien_tai["Trạng thái"]
            )

            if trang_thai_hien_tai in danh_sach_trang_thai:

                vi_tri_hien_tai = (
                    danh_sach_trang_thai.index(
                        trang_thai_hien_tai
                    )
                )

            else:

                vi_tri_hien_tai = 0


            trang_thai_moi = st.selectbox(
                "Chọn trạng thái mới",
                danh_sach_trang_thai,
                index=vi_tri_hien_tai
            )


            if st.button(
                "💾 Cập nhật trạng thái"
            ):

                try:

                    conn_update = get_connection()

                    cursor_update = (
                        conn_update.cursor()
                    )


                    sql_update = """
                    UPDATE lich_cham_soc
                    SET trang_thai = %s
                    WHERE ma_lich = %s
                    """


                    cursor_update.execute(
                        sql_update,
                        (
                            trang_thai_moi,
                            ma_lich_chon
                        )
                    )


                    conn_update.commit()

                    cursor_update.close()
                    conn_update.close()


                    st.success(
                        "🎉 Cập nhật trạng thái thành công!"
                    )

                    st.rerun()


                except Exception as e:

                    st.error(
                        f"❌ Lỗi cập nhật trạng thái: {e}"
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
