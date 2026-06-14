import streamlit as st
import os
import urllib.request
from pathlib import Path
import time

# Cartella per il modello AI
os.environ["U2NET_HOME"] = "/home/pyodide/.u2net"

def download_and_run():
    model_path = Path("/home/pyodide/.u2net/u2net/u2net.onnx")
    
    if not model_path.exists():
        st.set_page_config(page_title="AI Setup", page_icon="⚙️")
        st.markdown("### 🚀 Phase 2: Downloading AI Model")
        st.info("Downloading u2net.onnx (175MB). This happens only once.")
        
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        bar = st.progress(0)
        status = st.empty()
        console = st.empty()
        
        start_time = time.time()
        url = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
        
        def report(block_num, block_size, total_size):
            downloaded = block_num * block_size
            elapsed = time.time() - start_time
            if total_size > 0:
                percent = min(int(downloaded * 100 / total_size), 100)
                speed = downloaded / elapsed if elapsed > 0 else 0
                remaining = total_size - downloaded
                eta = remaining / speed if speed > 0 else 0
                
                bar.progress(percent)
                status.markdown(f"**{percent}%** | Speed: {speed/1024/1024:.2f} MB/s | ETA: {int(eta)}s")
                console.code(f"[RECV] {downloaded//1024//1024}MB / {total_size//1024//1024}MB")

        try:
            urllib.request.urlretrieve(url, str(model_path), reporthook=report)
            st.success("✅ Ready! Launching...")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"Download Error: {e}")
            st.stop()
    else:
        import bg_remover
        bg_remover.main()

if __name__ == "__main__":
    download_and_run()
