import streamlit as st
import os
import urllib.request
from pathlib import Path
import time

# Indichiamo a rembg dove salvare/cercare il modello AI
os.environ["U2NET_HOME"] = "/home/pyodide/.u2net"

def run_actual_app():
    # Importiamo ed eseguiamo l'app originale
    import bg_remover
    bg_remover.main()

def download_and_setup():
    model_path = Path("/home/pyodide/.u2net/u2net/u2net.onnx")
    
    if not model_path.exists():
        st.set_page_config(page_title="AI Model Setup", page_icon="✂️")
        st.markdown("## 🚀 Initializing AI Environment")
        st.info("The background removal model (175MB) is being downloaded to your browser cache. This happens only once.")
        
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # UI per il caricamento
        progress_bar = st.progress(0)
        status_text = st.empty()
        console_box = st.empty()
        
        url = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
        
        def download_report(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(int(downloaded * 100 / total_size), 100)
                progress_bar.progress(percent)
                status_text.markdown(f"**Status: Downloading... {percent}%**")
                # Simulazione console
                console_box.code(
                    f"[SYSTEM] Downloading u2net.onnx\n"
                    f"[INFO]   Received: {downloaded // (1024*1024)}MB / {total_size // (1024*1024)}MB\n"
                    f"[TARGET] {model_path}"
                )

        try:
            urllib.request.urlretrieve(url, str(model_path), reporthook=download_report)
            st.success("✅ Download complete! Starting the app...")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"Setup Error: {e}")
            st.stop()
    else:
        # Se il modello esiste già, avviamo l'app
        run_actual_app()

if __name__ == "__main__":
    download_and_setup()
