# storage_consultant.py
from storage import get_connection

def get_business_summary() -> str:
    """
    Mengambil ringkasan data dari database WarungVision 
    (Pengeluaran, Hutang, Stok) untuk konteks AI.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    summary_parts = []

    # 1. Cek Pengeluaran Terakhir (Expense)
    try:
        cur.execute("SELECT total_amount, merchant_name, transaction_date FROM expense_logs ORDER BY id DESC LIMIT 5")
        rows = cur.fetchall()
        if rows:
            summary_parts.append("--- RIWAYAT BELANJA TERAKHIR ---")
            for r in rows:
                rp = "Rp {:,.0f}".format(r['total_amount']).replace(',', '.')
                summary_parts.append(f"- {r['transaction_date']}: Belanja di {r['merchant_name']} senilai {rp}")
        else:
            summary_parts.append("Belum ada data belanja.")
    except Exception:
        pass

    # 2. Cek Total Hutang Pelanggan (Debt)
    try:
        cur.execute("SELECT customer_name, total_amount, due_date_note FROM debt_logs ORDER BY id DESC LIMIT 5")
        rows = cur.fetchall()
        if rows:
            summary_parts.append("\n--- CATATAN HUTANG PELANGGAN ---")
            total_debt = 0
            for r in rows:
                total_debt += r['total_amount']
                rp = "Rp {:,.0f}".format(r['total_amount']).replace(',', '.')
                summary_parts.append(f"- {r['customer_name']}: Hutang {rp} (Tempo: {r['due_date_note']})")
            
            # Hitung total kasar (dari 5 terakhir saja sebagai sampel konteks)
            summary_parts.append(f"Catatan: Ini adalah 5 hutang terbaru.")
        else:
            summary_parts.append("\nBelum ada catatan hutang.")
    except Exception:
        pass

    # 3. Cek Isu Stok (Inventory)
    try:
        # Kita ambil log stok terakhir saja
        cur.execute("SELECT result_text, created_at FROM inventory_logs ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        if row:
            summary_parts.append(f"\n--- LAPORAN STOK TERAKHIR ({row['created_at'][:10]}) ---")
            # result_text berisi JSON, tapi untuk konteks AI kita berikan raw textnya saja
            # agar AI membacanya sebagai "catatan historis"
            summary_parts.append(f"Data Raw: {row['result_text'][:500]}...") # Potong biar gak kepanjangan
        else:
            summary_parts.append("\nBelum ada laporan stok.")
    except Exception:
        pass
    
    conn.close()
    return "\n".join(summary_parts)