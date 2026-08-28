import streamlit as st
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

st.write(
    "Hệ thống tự động nhận diện khách hàng mới và khách hàng quay lại."
)


# =========================
# KHỞI TẠO SESSION
# =========================

if "ma_khach_hang" not in st.session_state:
    st.session_state.ma_khach_hang = None

if "khach_hang" not in st.session_state:
    st.session_state.khach_hang = None

if "da_kiem_tra" not in st.session_state:
    st.session_state.da_kiem_tra = False

if "khach_moi" not in st.session_state:
    st.session_state.khach_moi = False


# =========================
# HÀM KIỂM TRA KHÁCH HÀNG
# =========================

def tim_khach_hang(so_dien_thoai):

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

    cursor.execute(sql, (so_dien_thoai,))

    khach_hang = cursor.fetchone()

    cursor.close()
    conn.close()

    return khach_hang


# =========================
# KIỂM TRA SỐ ĐIỆN THOẠI
# =========================

st.subheader("🔎 Kiểm tra thông tin khách hàng")

so_dien_thoai = st.text_input(
    "Nhập số điện thoại khách hàng",
    key="so_dien_thoai_input"
)

if st.button("🔎 Kiểm tra khách hàng"):

    if not so_dien_thoai:

        st.warning("⚠️ Vui lòng nhập số điện thoại.")

    else:

        try:

            khach_hang = tim_khach_hang(so_dien_thoai)

            st.session_state.da_kiem_tra = True

            # -------------------------
            # KHÁCH HÀNG ĐÃ TỒN TẠI
            # -------------------------

            if khach_hang:

                st.session_state.khach_moi = False
                st.session_state.khach_hang = khach_hang
                st.session_state.ma_khach_hang = khach_hang[0]

                # Cập nhật thành khách hàng tiềm năng
                conn = get_connection()
                cursor = conn.cursor()

                sql_update = """
                UPDATE khach_hang_tiem_nang
                SET loai_khach_hang = 'Khách hàng cũ'
                WHERE ma_khach_hang = %s
                """

                cursor.execute(
                    sql_update,
                    (khach_hang[0],)
                )

                conn.commit()

                cursor.close()
                conn.close()

                st.success(
                    "🎯 Đã tìm thấy khách hàng! Khách hàng quay lại."
                )

            # -------------------------
            # KHÁCH HÀNG MỚI
            # -------------------------

            else:

                st.session_state.khach_moi = True
                st.session_state.khach_hang = None
                st.session_state.ma_khach_hang = None

                st.info(
                    "✨ Đây là khách hàng mới. Vui lòng nhập thông tin bên dưới."
                )

        except Exception as e:

            st.error(f"❌ Lỗi: {e}")


# =====================================================
# FORM KHÁCH HÀNG MỚI
# =====================================================

if (
    st.session_state.da_kiem_tra
    and st.session_state.khach_moi
    and st.session_state.ma_khach_hang is None
):

    st.divider()

    st.subheader("🆕 Thông tin khách hàng mới")

    with st.form("form_khach_hang_moi"):

        ho_ten = st.text_input("Họ và tên")

        khu_vuc = st.text_input("Khu vực")

        nhu_cau = st.text_input(
            "Nhu cầu khách hàng",
            placeholder="Ví dụ: Vay vốn, gửi tiết kiệm..."
        )

        ghi_chu = st.text_area("Ghi chú")

        submit_khach_moi = st.form_submit_button(
            "💾 Lưu thông tin khách hàng"
        )


    if submit_khach_moi:

        if not ho_ten:

            st.warning("⚠️ Vui lòng nhập họ tên.")

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
                        "Khách hàng mới",
                        nhu_cau,
                        ghi_chu
                    )
                )

                conn.commit()

                # Lấy mã khách hàng vừa tạo
                ma_khach_hang_moi = cursor.lastrowid

                cursor.close()
                conn.close()

                # LƯU VÀO SESSION
                st.session_state.ma_khach_hang = ma_khach_hang_moi

                st.session_state.khach_hang = (
                    ma_khach_hang_moi,
                    ho_ten,
                    so_dien_thoai,
                    khu_vuc,
                    "Khách hàng mới",
                    nhu_cau,
                    ghi_chu
                )

                st.session_state.khach_moi = False

                st.success(
                    "🎉 Đã lưu khách hàng thành công!"
                )

                st.rerun()

            except Exception as e:

                st.error(f"❌ Lỗi khi lưu khách hàng: {e}")


# =====================================================
# HIỂN THỊ KHÁCH HÀNG
# =====================================================

if st.session_state.ma_khach_hang is not None:

    st.divider()

    st.subheader("👤 Thông tin khách hàng")

    # Lấy thông tin mới nhất từ database
    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                ma_khach_hang,
                ho_ten,
                so_dien_thoai,
                khu_vuc,
                loai_khach_hang,
                nhu_cau,
                ghi_chu
            FROM khach_hang_tiem_nang
            WHERE ma_khach_hang = %s
            """,
            (st.session_state.ma_khach_hang,)
        )

        khach = cursor.fetchone()

        cursor.close()
        conn.close()

        if khach:

            st.write(f"**Họ tên:** {khach[1]}")
            st.write(f"**Số điện thoại:** {khach[2]}")
            st.write(f"**Khu vực:** {khach[3]}")
            st.write(f"**Loại khách hàng:** {khach[4]}")
            st.write(f"**Nhu cầu:** {khach[5]}")

    except Exception as e:

        st.error(f"❌ Lỗi: {e}")


# =====================================================
# LỊCH HẸN / TÁI TƯ VẤN
# =====================================================

if st.session_state.ma_khach_hang is not None:

    st.divider()

    st.subheader("📅 Lịch hẹn chăm sóc / tái tư vấn")

    with st.form("form_lich_cham_soc"):

        ngay_hen = st.date_input(
            "Ngày hẹn"
        )

        gio_hen = st.time_input(
            "Giờ hẹn"
        )

        noi_dung_tu_van = st.text_input(
            "Nội dung tư vấn",
            placeholder="Ví dụ: Tư vấn vay vốn, gửi tiết kiệm..."
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
            "Ghi chú lịch hẹn"
        )

        submit_lich = st.form_submit_button(
            "📅 Lưu lịch hẹn / tái tư vấn"
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
                    st.session_state.ma_khach_hang,
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

            st.success(
                "🎉 Đã lưu lịch chăm sóc / tái tư vấn thành công!"
            )

        except Exception as e:

            st.error(f"❌ Lỗi khi lưu lịch: {e}")
