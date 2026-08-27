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
st.write("Quản lý thông tin khách hàng và lịch chăm sóc, tái tư vấn.")


# =========================
# PHẦN 1: THÊM KHÁCH HÀNG
# =========================

st.subheader("📝 Thông tin khách hàng")

with st.form("form_khach_hang"):

    loai_khach_hang = st.radio(
        "Loại khách hàng",
        ["Khách hàng mới", "Khách hàng cũ"]
    )

    ho_ten = st.text_input("Họ và tên")

    so_dien_thoai = st.text_input("Số điện thoại")

    khu_vuc = st.text_input("Khu vực")

    nhu_cau = st.text_input(
        "Nhu cầu khách hàng",
        placeholder="Ví dụ: Vay vốn, gửi tiết kiệm, mở thẻ..."
    )

    ghi_chu = st.text_area("Ghi chú")

    submit_khach_hang = st.form_submit_button(
        "💾 Lưu khách hàng"
    )


if submit_khach_hang:

    if not ho_ten or not so_dien_thoai:
        st.warning("Vui lòng nhập họ tên và số điện thoại.")

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
                    so_dien_thoai,
                    khu_vuc,
                    loai_khach_hang,
                    nhu_cau,
                    ghi_chu
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            st.success("🎉 Đã lưu khách hàng thành công!")

        except Exception as e:

            st.error(f"Lỗi: {e}")


# =========================
# PHẦN 2: DANH SÁCH KHÁCH HÀNG
# =========================

st.divider()

st.subheader("📋 Danh sách khách hàng")

try:

    conn = get_connection()

    sql = """
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

    df_khach_hang = pd.read_sql(sql, conn)

    conn.close()

    if len(df_khach_hang) > 0:

        st.dataframe(
            df_khach_hang,
            use_container_width=True
        )

    else:

        st.info("Chưa có khách hàng nào.")

except Exception as e:

    st.error(f"Lỗi khi tải danh sách khách hàng: {e}")


# =========================
# PHẦN 3: TẠO LỊCH CHĂM SÓC
# =========================

st.divider()

st.subheader("📅 Tạo lịch chăm sóc / tái tư vấn")

try:

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ma_khach_hang, ho_ten, so_dien_thoai
        FROM khach_hang_tiem_nang
        ORDER BY ho_ten
    """)

    danh_sach_khach_hang = cursor.fetchall()

    cursor.close()
    conn.close()

except Exception as e:

    danh_sach_khach_hang = []

    st.error(f"Lỗi khi tải khách hàng: {e}")


if danh_sach_khach_hang:

    khach_hang_options = {
        f"{row[1]} - {row[2]}": row[0]
        for row in danh_sach_khach_hang
    }

    with st.form("form_lich_cham_soc"):

        khach_hang_chon = st.selectbox(
            "Khách hàng",
            list(khach_hang_options.keys())
        )

        ngay_hen = st.date_input(
            "Ngày hẹn"
        )

        gio_hen = st.time_input(
            "Giờ hẹn"
        )

        noi_dung_tu_van = st.text_input(
            "Nội dung tư vấn",
            placeholder="Ví dụ: Tư vấn khoản vay..."
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
            "Ghi chú lịch chăm sóc"
        )

        submit_lich = st.form_submit_button(
            "📅 Lưu lịch chăm sóc"
        )


    if submit_lich:

        try:

            ma_khach_hang = khach_hang_options[
                khach_hang_chon
            ]

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

            st.success("🎉 Đã tạo lịch chăm sóc thành công!")

        except Exception as e:

            st.error(f"Lỗi: {e}")


else:

    st.info("Bạn cần thêm ít nhất một khách hàng trước khi tạo lịch chăm sóc."
    )


# =========================
# PHẦN 4: XEM LỊCH CHĂM SÓC
# =========================

st.divider()

st.subheader("📆 Lịch chăm sóc khách hàng")

try:

    conn = get_connection()

    sql = """
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
    ORDER BY l.ngay_hen ASC, l.gio_hen ASC
    """

    df_lich = pd.read_sql(sql, conn)

    conn.close()

    if len(df_lich) > 0:

        st.dataframe(
            df_lich,
            use_container_width=True
        )

    else:

        st.info("Chưa có lịch chăm sóc nào.")

except Exception as e:

    st.error(f"Lỗi khi tải lịch chăm sóc: {e}")
