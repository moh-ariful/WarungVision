# ui_templates.py
from typing import List, Any, Dict

# --- CSS Styling ---
CSS = """
<style>
body, .gradio-container { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important; }
.gradio-container { max-width: 800px !important; margin: 0 auto !important; padding-top: 20px !important; }
h1 { color: #d35400; font-weight: 800 !important; text-align: center; margin-bottom: 0.5rem !important; font-size: 2.2rem !important; }
.description { text-align: center; font-size: 1.2rem; color: #555; margin-bottom: 1.5rem; }

.result-box { background-color: #fff; border: 2px solid #eee; border-radius: 12px; padding: 1.5rem; margin-top: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
.section-title { font-size: 1.25rem; font-weight: 700; margin-top: 1.2rem; margin-bottom: 0.8rem; color: #444; border-bottom: 2px solid #eee; padding-bottom: 5px; }
.result-list { padding-left: 0; list-style-type: none; margin: 0; }
.result-list li { font-size: 1.15rem; line-height: 1.5; margin-bottom: 0.8rem; padding: 10px; background-color: #f9f9f9; border-radius: 6px; border-left: 5px solid #ddd; }
.recommendations li { background-color: #e3f2fd; border-left: 5px solid #2196f3; color: #0d47a1; font-weight: 600; }
.sub-note { font-size: 0.95rem; color: #666; font-style: italic; }
.simple-text { font-size: 1.15rem; line-height: 1.5; }
.footer-info { text-align: center; font-size: 0.9rem; color: #888; margin-top: 2rem; }
button.primary { font-size: 1.2rem !important; padding: 12px 20px !important; font-weight: bold !important; }
.history-list li { font-size: 1rem !important; margin-bottom: 0.5rem !important; background-color: #fff !important; border: 1px solid #eee !important; border-left: 4px solid #ef5350 !important; }

/* Styles Khusus Kasbon */
.kasbon-header { background-color: #e8eaf6; color: #1a237e; border: 2px solid #3949ab; }
.kasbon-history li { border-left: 4px solid #3f51b5 !important; }

/* Styles Khusus Konsultan */
.consultant-box { background-color: #f3e5f5; border: 2px solid #ab47bc; border-radius: 12px; padding: 20px; margin-top: 1rem; }
.consultant-header { font-size: 1.3rem; font-weight: bold; color: #6a1b9a; margin-bottom: 10px; border-bottom: 1px solid #ce93d8; padding-bottom: 5px; display: flex; align-items: center; }
.consultant-content { font-size: 1.1rem; line-height: 1.6; color: #333; white-space: pre-wrap; }

.status-header { font-size: 1.5rem; font-weight: 900; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 1.5rem; color: #333; }
.status-header.DIDUGA-PALSU { background-color: #ffebee; color: #c62828; border: 2px solid #ef5350; }
.status-header.ASLI { background-color: #e8f5e9; color: #2e7d32; border: 2px solid #66bb6a; }
.status-header.PERLU-DICEK-LAGI { background-color: #fff8e1; color: #f57f17; border: 2px solid #ffca28; }

.status-header.SCAM-SAFE { background-color: #e0f7fa; color: #006064; border: 2px solid #00acc1; }
.status-header.SCAM-DANGER { background-color: #ffebee; color: #b71c1c; border: 2px solid #d32f2f; animation: pulse 2s infinite; }

@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(211, 47, 47, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(211, 47, 47, 0); } 100% { box-shadow: 0 0 0 0 rgba(211, 47, 47, 0); } }

@media (max-width: 600px) {
    .gradio-container { padding: 10px !important; }
    .status-header { font-size: 1.3rem; padding: 10px; }
    .result-list li { font-size: 1.05rem; }
    h1 { font-size: 1.8rem !important; }
}
</style>
"""

FOOTER = "<div class='footer-info'><strong>Dibuat untuk UMKM Indonesia 🇮🇩 | Powered by Kolosal AI, OpenAI, Gemini & Fonnte</strong></div>"
HEADER = "<div class='description'>Asisten pintar warung: Konsultan Warung, Cek Stok, Cegah Penipuan, Promosi WA dll</div>"

# --- HTML Generators ---

def format_expense_history(expenses: List[Dict[str, Any]]) -> str:
    """Render daftar riwayat belanja"""
    if not expenses:
        return "<div style='text-align:center; color:#999; padding:20px; font-style:italic;'>Belum ada riwayat belanja.</div>"
    
    html = '<div class="history-container"><div class="section-title" style="margin-top:0;">🕒 Riwayat Kulakan Terakhir</div><ul class="result-list history-list">'
    for item in expenses:
        rp = "Rp {:,.0f}".format(item['total']).replace(',', '.')
        html += f"""
        <li>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:700; color:#444;">{item['merchant']}</span>
                <span style="font-weight:700; color:#d32f2f;">{rp}</span>
            </div>
            <div style="font-size:0.9rem; color:#666; margin-top:4px; display:flex; justify-content:space-between;">
                <span>📅 {item['date']}</span>
                <span style="max-width:60%; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; text-align:right;">🛒 {item['items']}</span>
            </div>
        </li>
        """
    html += '</ul></div>'
    return html

def format_transfer_result(result: Any) -> str:
    """Render hasil cek transfer"""
    status_map = {
        "ASLI": ("✅", "UANG MASUK / ASLI"),
        "PERLU DICEK LAGI": ("🟡", "RAGU-RAGU / CEK LAGI"),
        "MENCURIGAKAN": ("🟠", "MENCURIGAKAN"),
        "DIDUGA PALSU": ("🔴", "AWAS! KEMUNGKINAN PALSU"),
    }
    icon, status_text = status_map.get(result.status, ("⚠️", result.status))
    
    md = f"""
    <div class="result-box">
        <div class="status-header {result.status.replace(' ', '-')}">
            <span class="icon">{icon}</span> {status_text}
        </div>
    """
    if result.findings:
        md += '<div class="section-title">Apa yang ditemukan di foto:</div><ul class="result-list">'
        for f in result.findings[:5]:
            clean_f = f.replace('"', '')
            md += f"<li>{clean_f}</li>"
        md += "</ul>"
    if result.recommendations:
        md += '<div class="section-title">Saran untuk Anda:</div><ul class="result-list recommendations">'
        for r in result.recommendations[:3]:
            clean_r = r.replace('"', '')
            md += f"<li>👉 {clean_r}</li>"
        md += "</ul></div>"
    return md

def format_inventory_result(result: Any) -> str:
    """Render hasil cek stok"""
    cat_icon = {"AMAN": "✅", "MULAI MENIPIS": "⚠️", "HAMPIR HABIS": "🔴"}
    md = '<div class="result-box"><div class="section-title" style="margin-top:0;">📦 Laporan Stok Barang</div><ul class="result-list">'
    
    for cat in result.categories:
        icon = cat_icon.get(cat.status, "⚠️")
        status_indo = cat.status
        if cat.status == "MULAI MENIPIS": status_indo = "Mulai Sedikit"
        if cat.status == "HAMPIR HABIS": status_indo = "Hampir Habis!"
        
        note_text = f" — {cat.notes}" if cat.notes else ""
        md += f"<li><strong>{icon} {cat.name}</strong>: {status_indo} <br><span class='sub-note'>{note_text}</span></li>"
        
    md += f"</ul><div class=\"section-title\">Ringkasan:</div><p class=\"simple-text\">{result.summary}</p></div>"
    return md

def format_scam_result(verdict_json: Dict, tech_details: List[str]) -> str:
    """Render hasil tangkal tipu"""
    status = verdict_json.get("status", "PERLU WASPADA").upper()
    reason = verdict_json.get("reason", "Tidak ada alasan spesifik.")
    action = verdict_json.get("action", "Hati-hati.")
    
    status_style = "SCAM-SAFE" if status == "AMAN" else "SCAM-DANGER"
    icon = "🛡️" if status == "AMAN" else "🚨"

    md = f"""
    <div class="result-box">
        <div class="status-header {status_style}">
            <span class="icon">{icon}</span> {status}
        </div>
        <div class="section-title">🔍 Analisis Kolosal AI:</div>
        <p class="simple-text">"{reason}"</p>
        <div class="section-title">💡 Saran Tindakan:</div>
        <div class="recommendations" style="padding:10px; background:#eef; border-radius:5px;">
            <strong>{action}</strong>
        </div>
        <div class="section-title" style="margin-top:20px; font-size:1rem; color:#666;">🛠️ Investigasi Teknis:</div>
        <ul class="result-list" style="font-size:0.9rem;">
    """
    for tech in tech_details:
        style = "color:red; font-weight:bold;" if any(x in tech for x in ["BERBAHAYA", "RED FLAG", "Ditemukan form"]) else ""
        md += f"<li style='{style}'>{tech}</li>"
    md += "</ul></div>"
    return md

def format_expense_result(result: Any) -> str:
    """Render hasil catat pengeluaran"""
    rp_formatted = "Rp {:,.0f}".format(result.numeric_total).replace(',', '.')
    return f"""
    <div class="result-box">
        <div class="status-header" style="background-color:#ffebee; color:#b71c1c; border:2px solid #ef5350;">
            <span class="icon">💸</span> PENGELUARAN TERCATAT
        </div>
        <div style="text-align:center; margin: 20px 0;">
            <div style="font-size:1.2rem; color:#666;">Total Belanja</div>
            <div style="font-size:2.5rem; font-weight:bold; color:#d32f2f;">{rp_formatted}</div>
        </div>
        <div class="section-title">📝 Detail Transaksi:</div>
        <ul class="result-list">
            <li>🏪 <strong>Toko:</strong> {result.merchant}</li>
            <li>📅 <strong>Tanggal:</strong> {result.date}</li>
            <li>🛒 <strong>Item:</strong> {result.items_summary}</li>
        </ul>
        <p class="sub-note" style="text-align:center; margin-top:15px;">Info: {result.confidence_note}</p>
    </div>
    """

def format_salesman_preview(caption: str) -> str:
    """Render preview caption salesman"""
    return f"""
    <div class="result-box">
        <div class="status-header ASLI">
            <span class="icon">✍️</span> CAPTION TERBENTUK (EDIT SEBELUM KIRIM)
        </div>
        <div style="padding:12px; font-size:1.05rem; white-space:pre-wrap;">{caption}</div>
        <div class="sub-note" style="margin-top:8px;">Silakan edit caption jika perlu: tambahkan harga, alamat, atau catatan penting sebelum mengirim.</div>
    </div>
    """

def format_salesman_result(status: str, result_text: str) -> str:
    """Render status pengiriman salesman"""
    header_class = "ASLI" if status == "SUCCESS" else "DIDUGA-PALSU"
    icon = "🚀" if status == "SUCCESS" else "💥"
    header_text = "PROMOSI TERKIRIM" if status == "SUCCESS" else "GAGAL KIRIM"

    return f"""
    <div class="result-box">
        <div class="status-header {header_class}">
            <span class="icon">{icon}</span> {header_text}
        </div>
        <div style="padding:15px; font-size:1.05rem; white-space: pre-wrap;">{result_text}</div>
        <div class="footer-info" style="margin-top:10px;">Powered by Fonnte & Gemini</div>
    </div>
    """

def format_kasbon_result(result: Any) -> str:
    """Render hasil pencatatan kasbon suara"""
    if result.status != "SUCCESS":
        return f"""
        <div class="result-box">
             <div class="status-header DIDUGA-PALSU">
                <span class="icon">❌</span> GAGAL PROSES
            </div>
            <p>Maaf, audio tidak jelas atau sistem gagal membaca.</p>
        </div>
        """

    rp_formatted = "Rp {:,.0f}".format(result.numeric_amount).replace(',', '.')
    return f"""
    <div class="result-box">
        <div class="status-header kasbon-header">
            <span class="icon">🎙️</span> KASBON TERCATAT
        </div>
        <div style="text-align:center; margin: 20px 0;">
            <div style="font-size:1.2rem; color:#666;">Total Hutang</div>
            <div style="font-size:2.5rem; font-weight:bold; color:#1a237e;">{rp_formatted}</div>
        </div>
        <div class="section-title">👤 Detail Pelanggan:</div>
        <ul class="result-list">
            <li><strong>Nama:</strong> {result.customer_name}</li>
            <li><strong>Barang:</strong> {result.items_summary}</li>
            <li><strong>Jatuh Tempo:</strong> {result.due_date}</li>
        </ul>
    </div>
    """

def format_kasbon_history(debts: List[Dict[str, Any]]) -> str:
    """Render riwayat kasbon"""
    if not debts:
        return "<div style='text-align:center; color:#999; padding:20px; font-style:italic;'>Belum ada data kasbon.</div>"
    
    html = '<div class="history-container"><div class="section-title" style="margin-top:0;">📒 Buku Hutang Terbaru</div><ul class="result-list history-list kasbon-history">'
    for item in debts:
        rp = "Rp {:,.0f}".format(item['amount']).replace(',', '.')
        # Format tanggal created_at biar rapi
        date_display = item['created_at'].split("T")[0]
        
        html += f"""
        <li>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:700; color:#303f9f;">{item['customer_name']}</span>
                <span style="font-weight:700; color:#c62828;">{rp}</span>
            </div>
            <div style="font-size:0.9rem; color:#666; margin-top:4px;">
               🛒 {item['items']}
            </div>
            <div style="font-size:0.85rem; color:#888; margin-top:4px; font-style:italic;">
               🕒 Tgl Catat: {date_display} | Tempo: {item['due_date']}
            </div>
        </li>
        """
    html += '</ul></div>'
    return html

def format_consultation_result(answer: str) -> str:
    """Render hasil jawaban konsultan AI (NEW)"""
    return f"""
    <div class="consultant-box">
        <div class="consultant-header">
            <span style="margin-right:8px;">💡</span> Jawaban Konsultan:
        </div>
        <div class="consultant-content">{answer}</div>
        <div class="sub-note" style="margin-top:15px; font-size:0.85rem;">*Jawaban berdasarkan data warung Anda yang tersedia.</div>
    </div>
    """