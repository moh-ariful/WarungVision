# app.py 
import os
import gradio as gr
from PIL import Image
from config import settings
from models import WarungVisionAI
from analyzers import TransferVerifier, InventoryAnalyzer
from storage import init_db, log_transfer, log_inventory
from analyzers_tangkal_tipu import ScamAnalyzer
from storage_tangkal_tipu import init_db_scam, log_scam_check
from analyzers_expense import ExpenseAnalyzer
from storage_expense import init_db_expense, log_expense, get_recent_expenses
from analyzers_salesman import SalesmanAnalyzer
from storage_salesman import init_db_salesman
from analyzers_kasbon import KasbonAnalyzer
from storage_kasbon import init_db_kasbon, log_debt, get_recent_debts
# --- Import Modul Konsultan (NEW) ---
from analyzers_consultant import ConsultantAnalyzer
# ------------------------------------
import ui_templates as ui  # Import template modul

def build_interface() -> gr.Blocks:
    # --- Init DB & AI ---
    init_db(); init_db_scam(); init_db_expense(); init_db_salesman(); init_db_kasbon()
    
    try:
        ai = WarungVisionAI()
        transfer_verifier = TransferVerifier(ai)
        inv_analyzer = InventoryAnalyzer(ai)
        scam_analyzer = ScamAnalyzer(vision_ai=ai)
        exp_analyzer = ExpenseAnalyzer(ai)
        sales_analyzer = SalesmanAnalyzer(ai)
        kasbon_analyzer = KasbonAnalyzer(ai)
        # Init Consultant Analyzer
        consult_analyzer = ConsultantAnalyzer()
        ai_ready = True
    except Exception as e:
        ai_ready = False
        print(f"Error init AI: {e}")

    # --- Helpers ---
    def validate_image(file_path):
        """Validasi ukuran dan format file gambar"""
        if not file_path: return None, "⚠️ File tidak ditemukan."
        if os.path.getsize(file_path) > 11 * 1024 * 1024: return None, "⚠️ File max 11MB."
        try: return Image.open(file_path), None
        except: return None, "⚠️ File rusak."

    def get_history_html():
        """Ambil data belanja dan render HTML"""
        return ui.format_expense_history(get_recent_expenses(5))

    def get_kasbon_history_html():
        """Ambil data kasbon dan render HTML"""
        return ui.format_kasbon_history(get_recent_debts(5))

    # --- Handlers ---
    def handle_transfer(file_path, notes, progress=gr.Progress()):
        if not ai_ready: return "⚠️ Error: API Key bermasalah."
        img, err = validate_image(file_path)
        if err: return err
        
        progress(0.2, desc="Sedang melihat foto...")
        try:
            # Notes dijamin string kosong jika None agar logic model tetap jalan
            safe_notes = notes if notes else ""
            res = transfer_verifier.verify(safe_notes, img)
            
            progress(0.8, desc="Menulis laporan...")
            log_transfer(safe_notes, res.raw_text)
            return ui.format_transfer_result(res)
        except Exception as e: return f"⚠️ Gangguan: {str(e)}"

    def handle_inventory(file_path, notes, progress=gr.Progress()):
        if not ai_ready: return "⚠️ API Key bermasalah."
        img, err = validate_image(file_path)
        if err: return err

        progress(0.2, desc="Analisa stok...")
        try:
            safe_notes = notes if notes else ""
            res = inv_analyzer.analyze(safe_notes, img)
            
            progress(0.8, desc="Menyusun laporan...")
            log_inventory(safe_notes, res.raw_text)
            return ui.format_inventory_result(res)
        except Exception as e: return f"⚠️ Gangguan: {str(e)}"

    def handle_scam(file_path, progress=gr.Progress()):
        if not ai_ready: return "⚠️ API Key bermasalah."
        img, err = validate_image(file_path)
        if err: return err

        progress(0.2, desc="🕵️‍♀️ Membaca pesan...")
        try:
            data = scam_analyzer.analyze(img)
            verdict = data["final_verdict"]
            progress(0.8, desc="🤖 Kolosal AI berpikir...")
            log_scam_check(data['text'], data['url'], verdict.get('status','UNKNOWN'), str(verdict))
            return ui.format_scam_result(verdict, data["tech_data"])
        except Exception as e: return f"⚠️ Error: {str(e)}"

    def handle_expense(file_path, progress=gr.Progress()):
        if not ai_ready: return "⚠️ API Key Error.", get_history_html()
        img, err = validate_image(file_path)
        if err: return err, get_history_html()

        progress(0.2, desc="🔎 Baca struk...")
        try:
            res = exp_analyzer.analyze(img)
            progress(0.8, desc="💾 Simpan...")
            log_expense(res.merchant, res.date, res.numeric_total, res.items_summary, res.raw_text)
            return ui.format_expense_result(res), get_history_html()
        except Exception as e: return f"⚠️ Gagal: {str(e)}", get_history_html()

    def handle_sales_gen(file_path, style, progress=gr.Progress()):
        if not ai_ready: return None, "⚠️ API Key Error."
        img, err = validate_image(file_path)
        if err: return None, err

        progress(0.2, desc="🧠 AI menulis...")
        try:
            cap, err_msg = sales_analyzer.generate_caption(style, img)
            if err_msg: return None, err_msg
            return cap, ui.format_salesman_preview(cap)
        except Exception as e: return None, f"⚠️ Error: {str(e)}"

    def handle_sales_send(file_path, phone, caption, progress=gr.Progress()):
        if not ai_ready: return "⚠️ API Key Error."
        img, err = validate_image(file_path)
        if err: return err
        if not phone or not caption: return "⚠️ Data tidak lengkap."

        progress(0.2, desc="📤 Mengirim...")
        try:
            res_txt, status = sales_analyzer.send_promotion(file_path, phone, caption)
            return ui.format_salesman_result(status, res_txt)
        except Exception as e: return f"⚠️ Error: {str(e)}"

    def handle_kasbon(audio_path, progress=gr.Progress()):
        if not ai_ready: return "⚠️ API Key Error.", get_kasbon_history_html()
        if not audio_path: return "⚠️ Belum ada suara direkam.", get_kasbon_history_html()

        progress(0.2, desc="👂 Mendengarkan & Uploading...")
        try:
            # Analyze audio using Gemini Multimodal
            res = kasbon_analyzer.analyze(audio_path)
            
            if res.status == "SUCCESS":
                progress(0.8, desc="💾 Mencatat di buku hutang...")
                log_debt(res.customer_name, res.items_summary, res.numeric_amount, res.due_date, res.raw_text)
            
            return ui.format_kasbon_result(res), get_kasbon_history_html()
        except Exception as e:
            return f"⚠️ Error System: {str(e)}", get_kasbon_history_html()

    # --- Handler Konsultan Warung (NEW) ---
    def handle_consult(question, progress=gr.Progress()):
        if not question: return "⚠️ Pertanyaan kosong."
        
        progress(0.2, desc="🕵️ Mengambil data warung...")
        try:
            progress(0.5, desc="🤖 AI Hibrida berpikir...")
            answer = consult_analyzer.consult(question)
            return ui.format_consultation_result(answer)
        except Exception as e:
            return f"⚠️ Error Konsultan: {str(e)}"

    # --- UI Builder ---
    with gr.Blocks(title=settings.GRADIO_TITLE) as demo:
        # Inject CSS melalui komponen HTML di dalam body
        gr.HTML(ui.CSS)
        
        gr.Markdown("# 🏪 WarungVision")
        gr.HTML(ui.HEADER)

        with gr.Tab("💳 Cek Transfer"):
            with gr.Row():
                with gr.Column():
                    tf_img = gr.Image(label="Bukti Transfer", type="filepath", height=350)
                    tf_note = gr.Textbox(label="Catatan", placeholder="Misal: Cek nominalnya sudah benar belum?")
                    btn_tf = gr.Button("✅ Periksa", variant="primary")
                with gr.Column():
                    tf_out = gr.HTML("<div class='result-box' style='text-align:center; color:#ccc'>Hasil disini...</div>")
            btn_tf.click(handle_transfer, inputs=[tf_img, tf_note], outputs=[tf_out])

        with gr.Tab("📦 Stok & Rak"):
            with gr.Row():
                with gr.Column():
                    inv_img = gr.Image(label="Foto Rak", type="filepath", height=350)
                    inv_note = gr.Textbox(label="Catatan", placeholder="Misal: Cek apakah stok minyak goreng menipis?")
                    btn_inv = gr.Button("🔎 Analisa Stok", variant="primary")
                with gr.Column():
                    inv_out = gr.HTML("<div class='result-box' style='text-align:center; color:#ccc'>Hasil disini...</div>")
            btn_inv.click(handle_inventory, inputs=[inv_img, inv_note], outputs=[inv_out])

        with gr.Tab("🛡️ Tangkal Tipu"):
            with gr.Row():
                with gr.Column():
                    scam_img = gr.Image(label="Screenshot Chat", type="filepath", height=350)
                    btn_scam = gr.Button("🔍 Analisa", variant="primary")
                with gr.Column():
                    scam_out = gr.HTML("<div class='result-box' style='text-align:center; color:#ccc'>Hasil disini...</div>")
            btn_scam.click(handle_scam, inputs=[scam_img], outputs=[scam_out])

        with gr.Tab("💸 Catat Pengeluaran"):
            with gr.Row():
                with gr.Column():
                    exp_img = gr.Image(label="Foto Struk", type="filepath", height=350)
                    btn_exp = gr.Button("💾 Catat", variant="primary")
                with gr.Column():
                    exp_out = gr.HTML("<div class='result-box' style='text-align:center; color:#ccc'>Hasil disini...</div>")
                    exp_hist = gr.HTML(get_history_html()) 
            btn_exp.click(handle_expense, inputs=[exp_img], outputs=[exp_out, exp_hist])

        with gr.Tab("📢 Salesman WA"):
            with gr.Row():
                with gr.Column():
                    sale_img = gr.Image(label="Produk", type="filepath", height=350)
                    sale_phone = gr.Textbox(label="No WA Tujuan")
                    sale_style = gr.Dropdown(["Gaya Emak-emak (Heboh)", "Gaya Formal", "Gaya Gaul"], label="Gaya", value="Gaya Emak-emak (Heboh)")
                    btn_gen = gr.Button("📝 Buat Caption", variant="primary")
                    btn_send = gr.Button("📨 Kirim", variant="secondary")
                with gr.Column():
                    sale_stat = gr.HTML("<div class='result-box' style='text-align:center; color:#ccc'>Status kirim...</div>")
                    sale_cap = gr.Textbox(label="Caption (Edit)", lines=4)
                    sale_prev = gr.HTML("")
            btn_gen.click(handle_sales_gen, inputs=[sale_img, sale_style], outputs=[sale_cap, sale_prev])
            btn_send.click(handle_sales_send, inputs=[sale_img, sale_phone, sale_cap], outputs=[sale_stat])
        
        with gr.Tab("🎙️ Juragan Kasbon"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 🗣️ Rekam Transaksi Hutang")
                    gr.Markdown("Tekan ikon mic untuk bicara, atau upload file audio (MP3/WAV).")
                    kasbon_audio = gr.Audio(sources=["microphone", "upload"], type="filepath", label="Suara Pemilik Warung")
                    btn_kasbon = gr.Button("📝 Catat Suara", variant="primary")
                with gr.Column():
                    kasbon_out = gr.HTML("<div class='result-box' style='text-align:center; color:#ccc'>Hasil pencatatan suara...</div>")
                    kasbon_hist = gr.HTML(get_kasbon_history_html())
            btn_kasbon.click(handle_kasbon, inputs=[kasbon_audio], outputs=[kasbon_out, kasbon_hist])
            
        # --- TAB BARU: KONSULTAN WARUNG ---
        with gr.Tab("🤝 Konsultan Warung"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 🤖 Asisten Bisnis Pintar (Hybrid AI)")
                    gr.Markdown("Tanyakan apa saja tentang kondisi warungmu. AI akan menjawab berdasarkan data belanja, hutang, dan stok.")
                    consult_input = gr.Textbox(label="Pertanyaan Anda", placeholder="Misal: 'Keuanganku sehat gak?', 'Siapa yang hutangnya paling banyak?'")
                    btn_consult = gr.Button("Tanya Konsultan", variant="primary")
                with gr.Column():
                    consult_out = gr.HTML("<div class='result-box' style='text-align:center; color:#ccc'>Jawaban akan muncul di sini...</div>")
            btn_consult.click(handle_consult, inputs=[consult_input], outputs=[consult_out])

        gr.HTML(ui.FOOTER)

        # --- EVENT LISTENERS FOR ON-LOAD REFRESH ---
        demo.load(fn=get_kasbon_history_html, inputs=None, outputs=[kasbon_hist])
        demo.load(fn=get_history_html, inputs=None, outputs=[exp_hist])

    return demo

if __name__ == "__main__":
    demo = build_interface()
    demo.queue().launch(server_name=settings.GRADIO_SERVER_NAME, server_port=settings.GRADIO_SERVER_PORT)