import streamlit as st
import pandas as pd
from database import get_connection


# =========================
# CẤU HÌNH TRANG
# =========================

st.set_page_config(
    page_title="Quản lý khách hàng tiềm năng",
    page_icon="👥",
    layout="centered"
)

st.title("👥 QUẢN LÝ KHÁCH HÀNG TIỀM NĂNG")
st.write("Hệ thống tự động nhận diện khách hàng mới và khách hàng quay lại.")


# =========================
# KHỞI TẠO SESSION
# =========================

if "thong_tin_khach" not in st.session_state:
    st.session_state.thong_tin_khach = None


# =========================
# NHẬP SỐ ĐIỆN THOẠI
# =========================

st.subheader("🔎 Kiểm tra khách hàng")

so_dien_thoai_tim = st.text_input(
    "Nhập số điện thoại khách hàng"
)

kiem_tra = st.button("🔎 Kiểm tra thông tin")


# =========================
# KIỂM TRA KHÁCH HÀNG
# =========================

if kiem_tra:

    if not so_dien_thoai_tim:

        st.warning("Vui lòng nhập số điện thoại.")

    else:

        try:

            conn = get_connection()
            cursor = conn.cursor()

            sql = """
            SELECT
                ma_khach_hang,
                ho_ten,
                so_dien_thoai,
                khu_vuc,
                loai_khach_hang,
                nhu_cau,
                ghi_chu
            FROM khach_hang_tiem_nang
            WHERE so_dien_thoai = %s
            """

            cursor.execute(
                sql,
                (so_dien_thoai_tim,)
            )

            khach_hang = cursor.fetchone()

            cursor.close()
            conn.close()


            # =========================
            # KHÁCH HÀNG ĐÃ TỒN TẠI
            # =========================

            if khach_hang:

                st.session_state.thong_tin_khach = khach_hang

                st.success(
                    "🎯 Đã tìm thấy khách hàng! Đây là khách hàng quay lại."
                )

            # =========================
            # KHÁCH HÀNG MỚI
            # =========================

            else:

                st.session_state.thong_tin_khach = None

                st.info(
                    "✨ Đây là khách hàng mới. Vui lòng nhập thông tin khách hàng."
                )

        except Exception as e:

            st.error(f"Lỗi: {e}")


# =====================================================
# NẾU LÀ KHÁCH HÀNG CŨ / QUAY LẠI
# =====================================================

if st.session_state.thong_tin_khach:

    khach = st.session_state.thong_tin_khach

    ma_khach_hang = khach[0]
    ho_ten_cu = khach[1]
    so_dien_thoai_cu = khach[2]
    khu_vuc_cu = khach[3]
    loai_cu = khach[4]
    nhu_cau_cu = khach[5]
    ghi_chu_cu = khach[6]

    st.divider()

    st.subheader("👤 Thông tin khách hàng")

    st.write(f"**Họ tên:** {ho_ten_cu}")
    st.write(f"**Số điện thoại:** {so_dien_thoai_cu}")
    st.write(f"**Khu vực:** {khu_vuc_cu}")
    st.write(f"**Nhu cầu:** {nhu_cau_cu}")

    st.success(
        "⭐ Khách hàng đã quay lại. Hệ thống xác định là KHÁCH HÀNG TIỀM NĂNG."
    )


    # =========================
    # CẬP NHẬT THÀNH KHÁCH TIỀM NĂNG
    # =========================

    try:

        conn = get_connection()
        cursor = conn.cursor()

        sql_update = """
        UPDATE khach_hang_tiem_nang
        SET loai_khach_hang = 'Khách hàng cũ'
        WHERE ma_khach_hang = %s
        """

        cursor.execute(
            sql_update,
            (ma_khach_hang,)
        )

        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:

        st.error(f"Lỗi cập nhật: {e}")


    # =========================
    # TẠO LỊCH CHĂM SÓC
    # =========================

    st.divider()

    st.subheader("📅 Lịch chăm sóc / tái tư vấn")

    with st.form("form_lich_cham_soc"):

        ngay_hen = st.date_input(
            "Ngày hẹn"
        )

        gio_hen = st.time_input(
            "Giờ hẹn"
        )

        noi_dung_tu_van = st.text_input(
            "Nội dung tư vấn"
        )

        hinh_thuc_lien_he = st.selectbox(
            "Hình thức liên hệ",
            [
                "Gọi điện",
                "Gặp trực tiếp",
                "Tin nhắn",
                "Email"
            ]
        )

        trang_thai = st.selectbox(
            "Trạng thái",
            [
                "Chưa liên hệ",
                "Đã liên hệ",
                "Đã tư vấn",
                "Hẹn lại",
                "Hoàn thành"
            ]
        )

        ghi_chu_lich = st.text_area(
            "Ghi chú"
        )

        submit_lich = st.form_submit_button(
            "📅 Lưu lịch chăm sóc"
        )


    if submit_lich:

        try:

            conn = get_connection()
            cursor = conn.cursor()

            sql = """
            INSERT INTO lich_cham_soc
            (
                ma_khach_hang,
                ngay_hen,
                gio_hen,
                noi_dung_tu_van,
                hinh_thuc_lien_he,
                trang_thai,
                ghi_chu
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (
                    ma_khach_hang,
                    ngay_hen,
                    gio_hen,
                    noi_dung_tu_van,
                    hinh_thuc_lien_he,
                    trang_thai,
                    ghi_chu_lich
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            st.success("🎉 Đã lưu lịch chăm sóc!")

        except Exception as e:

            st.error(f"Lỗi: {e}")


# =====================================================
# KHÁCH HÀNG MỚI
# =====================================================

elif kiem_tra and not st.session_state.thong_tin_khach:

    st.divider()

    st.subheader("🆕 Đăng ký khách hàng mới")

    with st.form("form_khach_hang_moi"):

        ho_ten = st.text_input("Họ và tên")

        khu_vuc = st.text_input("Khu vực")

        nhu_cau = st.text_input(
            "Nhu cầu khách hàng",
            placeholder="Ví dụ: Vay vốn, gửi tiết kiệm..."
        )

        ghi_chu = st.text_area("Ghi chú")

        submit_khach_moi = st.form_submit_button(
            "💾 Lưu khách hàng"
        )


    if submit_khach_moi:

        if not ho_ten:

            st.warning("Vui lòng nhập họ tên.")

        else:

            try:

                conn = get_connection()
                cursor = conn.cursor()

                sql = """
                INSERT INTO khach_hang_tiem_nang
                (
                    ho_ten,
                    so_dien_thoai,
                    khu_vuc,
                    loai_khach_hang,
                    nhu_cau,
                    ghi_chu
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """

                cursor.execute(
                    sql,
                    (
                        ho_ten,
                        so_dien_thoai_tim,
                        khu_vuc,
                        "Khách hàng mới",
                        nhu_cau,
                        ghi_chu
                    )
                )

                conn.commit()

                cursor.close()
                conn.close()

                st.success(
                    "🎉 Đã lưu khách hàng mới thành công!"
                )

            except Exception as e:

                st.error(f"Lỗi: {e}")
