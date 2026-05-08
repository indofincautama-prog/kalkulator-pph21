import streamlit as st

st.set_page_config(page_title="Kalkulator PPh 21", page_icon="🧮", layout="centered")

st.title("🧮 Kalkulator PPh 21 Pekerjaan Bebas")
st.caption("Berdasarkan PMK No. 101/PMK.010/2016 | Tarif UU HPP 2021")

# Gate: cek omzet
st.subheader("Cek kelayakan")
omzet_ok = st.radio(
    "Apakah penghasilan bruto ≤ Rp4.800.000.000 per tahun?",
    ["Pilih jawaban...", "Ya, ≤ Rp4,8 miliar", "Tidak, di atas itu"]
)

if omzet_ok == "Tidak, di atas itu":
    st.error("""
    ❌ Kalkulator ini tidak dapat digunakan.
    
    Penghasilan bruto di atas Rp4,8 miliar tidak memenuhi syarat 
    menggunakan NPPN. Wajib pajak wajib menyelenggarakan pembukuan 
    sesuai Pasal 28 UU KUP.
    """)

elif omzet_ok == "Ya, ≤ Rp4,8 miliar":
    st.divider()

    # Data wajib pajak
    st.subheader("Data wajib pajak")
    nama = st.text_input("Nama wajib pajak")
    bruto = st.number_input("Penghasilan bruto per tahun (Rp)", min_value=0, step=1000000)

    st.divider()

    # Status PTKP
    st.subheader("Status PTKP")
    col1, col2 = st.columns(2)
    with col1:
        status = st.selectbox("Status perkawinan", ["Tidak Kawin (TK)", "Kawin (K)", "Kawin, istri bekerja (K/I)"])
    with col2:
        tanggungan = st.selectbox("Jumlah tanggungan", [0, 1, 2, 3])

    # Hitung PTKP
    ptkp_dasar = 54_000_000
    ptkp_kawin = 4_500_000
    ptkp_tanggungan = 4_500_000

    if "TK" in status and "K/I" not in status:
        ptkp = ptkp_dasar + tanggungan * ptkp_tanggungan
        label_status = f"TK/{tanggungan}"
    elif "K/I" in status:
        ptkp = ptkp_dasar * 2 + ptkp_kawin + tanggungan * ptkp_tanggungan
        label_status = f"K/I/{tanggungan}"
    else:
        ptkp = ptkp_dasar + ptkp_kawin + tanggungan * ptkp_tanggungan
        label_status = f"K/{tanggungan}"

    st.divider()

    # Metode NPPN
    st.subheader("Metode perhitungan")
    pakai_nppn = st.toggle("Gunakan NPPN (Norma Perhitungan Penghasilan Netto)")
    norma = 0
    if pakai_nppn:
        norma = st.number_input("Persentase norma (%)", min_value=1, max_value=100, value=50)
        metode = f"NPPN {norma}%"
    else:
        metode = "Penghasilan netto penuh"

    st.divider()

    # Hitung
    if st.button("🧮 Hitung PPh 21", use_container_width=True):
        if bruto <= 0:
            st.warning("Masukkan penghasilan bruto terlebih dahulu.")
        else:
            netto_raw = bruto * (norma / 100) if pakai_nppn else bruto
            netto = round(netto_raw)
            pkp_raw = max(netto - ptkp, 0)
            pkp = (pkp_raw // 1000) * 1000

            if pkp <= 60_000_000:
                pajak = pkp * 0.05
                layer = "5%"
            elif pkp <= 250_000_000:
                pajak = 60_000_000 * 0.05 + (pkp - 60_000_000) * 0.15
                layer = "5% + 15%"
            elif pkp <= 500_000_000:
                pajak = 60_000_000 * 0.05 + 190_000_000 * 0.15 + (pkp - 250_000_000) * 0.25
                layer = "5% + 15% + 25%"
            else:
                pajak = 60_000_000 * 0.05 + 190_000_000 * 0.15 + 250_000_000 * 0.25 + (pkp - 500_000_000) * 0.30
                layer = "5% + 15% + 25% + 30%"

            # Tampilkan hasil
            st.subheader(f"Hasil — {nama} ({label_status})")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Penghasilan bruto", f"Rp {bruto:,.0f}")
                st.metric("PTKP", f"Rp {ptkp:,.0f}")
                st.metric("PPh 21 / tahun", f"Rp {pajak:,.0f}")
            with col2:
                st.metric("Penghasilan netto", f"Rp {netto:,.0f}")
                st.metric("PKP", f"Rp {pkp:,.0f}")
                st.metric("PPh 21 / bulan", f"Rp {pajak/12:,.0f}")

            st.info(f"Metode: {metode} | Tarif: {layer}")
            st.caption("* Pembulatan sesuai Pasal 17 UU PPh | PMK No. 101/PMK.010/2016")
