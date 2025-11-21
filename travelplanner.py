import os
import json
from datetime import datetime

DATA_FILE = "travel_data.json"

# ============================
#   UTILITIES
# ============================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header():
    print("=" * 60)
    print("🌍  TRAVEL PLANNER - SISTEM MANAJEMEN RENCANA LIBURAN 🌍".center(60))
    print("=" * 60)

def pause():
    input("\nTekan ENTER untuk melanjutkan...")

# ============================
#   LOAD & SAVE DATA JSON
# ============================

def load_data():
    if not os.path.exists(DATA_FILE):
        return [], 1

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            return data.get("travel_list", []), data.get("next_id", 1)
    except:
        return [], 1

def save_data(travel_list, next_id):
    with open(DATA_FILE, "w") as file:
        json.dump({
            "travel_list": travel_list,
            "next_id": next_id
        }, file, indent=4)

# ============================
#   FORMAT TANGGAL
# ============================

def convert_to_display(date_str):
    return date_str  # sudah dd-mm-yyyy

# ============================
#   HELPER
# ============================

def find_by_id(travel_list, ID):
    for d in travel_list:
        if d["id"] == ID:
            return d
    return None

# ============================
#   CRUD FUNCTIONS
# ============================

def tambah_destinasi(travel_list, next_id):
    while True:
        clear()
        header()
        print("➕ TAMBAH DESTINASI")
        print("0. Kembali\n")

        lanjut = input("Tekan ENTER untuk mulai atau 0 untuk kembali: ").strip()
        if lanjut == "0":
            return next_id

        nama = input("Nama Tempat          : ").strip()
        lokasi = input("Lokasi (Kota/Negara) : ").strip()
        durasi = input("Durasi Kunjungan     : ").strip()
        transportasi = input("Transportasi         : ").strip()
        tanggal = input("Tanggal (DD-MM-YYYY) : ").strip()
        biaya = input("Estimasi Biaya (Rp)  : ").strip()
        catatan = input("Catatan Tambahan     : ").strip()

        if not (nama and lokasi and durasi and transportasi and tanggal and biaya):
            print("\n❌ Semua field wajib diisi!")
            pause()
            continue

        try:
            datetime.strptime(tanggal, "%d-%m-%Y")
        except ValueError:
            print("\n❌ Format tanggal salah!")
            pause()
            continue

        biaya_clean = biaya.replace(".", "").replace(",", "")
        if not biaya_clean.isdigit():
            print("\n❌ Biaya harus angka!")
            pause()
            continue

        travel_list.append({
            "id": next_id,
            "nama": nama,
            "lokasi": lokasi,
            "durasi": durasi,
            "transportasi": transportasi,
            "tanggal": tanggal,
            "biaya": int(biaya_clean),
            "catatan": catatan
        })

        save_data(travel_list, next_id + 1)
        print("\n✅ Destinasi berhasil ditambahkan!")
        pause()
        return next_id + 1


def tampilkan_destinasi(travel_list, pause_after=True):
    clear()
    header()
    print("📜 DAFTAR RENCANA PERJALANAN\n")

    if not travel_list:
        print("Belum ada destinasi.")
        if pause_after:
            pause()
        return

    sorted_list = sorted(
        travel_list,
        key=lambda x: datetime.strptime(x["tanggal"], "%d-%m-%Y")
    )

    for d in sorted_list:
        print(f"""
ID            : {d['id']}
Nama          : {d['nama']}
Lokasi        : {d['lokasi']}
Durasi        : {d['durasi']}
Transportasi  : {d['transportasi']}
Tanggal       : {d['tanggal']}
Biaya         : Rp{d['biaya']:,}
Catatan       : {d['catatan']}
-----------------------------------------------
""")

    if pause_after:
        pause()


def edit_destinasi(travel_list, next_id):
    clear()
    header()
    print("✏ UBAH DESTINASI")
    print("0. Kembali\n")

    tampilkan_destinasi(travel_list, pause_after=False)

    pilih = input("Masukkan ID (0 untuk kembali): ").strip()
    if pilih == "0":
        return next_id

    if not pilih.isdigit():
        print("❌ ID tidak valid!")
        pause()
        return next_id

    pilih = int(pilih)
    d = find_by_id(travel_list, pilih)

    if not d:
        print("❌ ID tidak ditemukan!")
        pause()
        return next_id

    print("\nKosongkan input jika tidak ingin mengubah.")

    d['nama'] = input(f"Nama ({d['nama']}): ") or d['nama']
    d['lokasi'] = input(f"Lokasi ({d['lokasi']}): ") or d['lokasi']
    d['durasi'] = input(f"Durasi ({d['durasi']}): ") or d['durasi']
    d['transportasi'] = input(f"Transportasi ({d['transportasi']}): ") or d['transportasi']

    tanggal_baru = input(f"Tanggal [{d['tanggal']}] (DD-MM-YYYY): ")
    if tanggal_baru.strip():
        try:
            datetime.strptime(tanggal_baru, "%d-%m-%Y")
            d['tanggal'] = tanggal_baru
        except ValueError:
            print("❌ Format tanggal salah!")

    biaya_baru = input(f"Biaya ({d['biaya']}): ")
    if biaya_baru.strip():
        biaya_clean = biaya_baru.replace(".", "").replace(",", "")
        if biaya_clean.isdigit():
            d['biaya'] = int(biaya_clean)
        else:
            print("❌ Biaya harus angka!")

    d['catatan'] = input(f"Catatan ({d['catatan']}): ") or d['catatan']

    save_data(travel_list, next_id)
    print("\n✅ Destinasi berhasil diperbarui!")
    pause()
    return next_id


def hapus_destinasi(travel_list, next_id):
    clear()
    header()
    print("🗑 HAPUS DESTINASI")
    print("0. Kembali\n")

    tampilkan_destinasi(travel_list, pause_after=False)

    pilih = input("Masukkan ID (0 untuk kembali): ").strip()
    if pilih == "0":
        return next_id

    if not pilih.isdigit():
        print("❌ ID tidak valid!")
        pause()
        return next_id

    pilih = int(pilih)
    d = find_by_id(travel_list, pilih)

    if not d:
        print("❌ ID tidak ditemukan!")
        pause()
        return next_id

    travel_list.remove(d)
    save_data(travel_list, next_id)

    print("\n🗑 Destinasi berhasil dihapus!")
    pause()
    return next_id


def ringkasan(travel_list):
    clear()
    header()
    print("📊 RINGKASAN PERJALANAN\n")

    if not travel_list:
        print("Belum ada data.")
        pause()
        return

    total_biaya = sum(d["biaya"] for d in travel_list)
    total_tempat = len(travel_list)

    print(f"Total Destinasi        : {total_tempat}")
    print(f"Total Estimasi Biaya   : Rp{total_biaya:,}")

    print("\n📅 Jadwal Berdasarkan Tanggal")
    print("-" * 60)

    sorted_list = sorted(
        travel_list,
        key=lambda x: datetime.strptime(x["tanggal"], "%d-%m-%Y")
    )

    for d in sorted_list:
        print(f"{d['tanggal']} — {d['nama']} ({d['lokasi']})")

    pause()

# ============================
#   MENU UTAMA
# ============================

def menu():
    travel_list, next_id = load_data()

    while True:
        clear()
        header()
        print("1. Lihat Rencana")
        print("2. Tambah Destinasi")
        print("3. Ubah Destinasi")
        print("4. Hapus Destinasi")
        print("5. Ringkasan")
        print("6. Keluar")
        print("=" * 60)

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tampilkan_destinasi(travel_list)
        elif pilih == "2":
            next_id = tambah_destinasi(travel_list, next_id)
        elif pilih == "3":
            next_id = edit_destinasi(travel_list, next_id)
        elif pilih == "4":
            next_id = hapus_destinasi(travel_list, next_id)
        elif pilih == "5":
            ringkasan(travel_list)
        elif pilih == "6":
            clear()
            print("👋 Terima kasih telah menggunakan Travel Planner!")
            break
        else:
            print("❌ Input tidak valid!")
            pause()

menu()
