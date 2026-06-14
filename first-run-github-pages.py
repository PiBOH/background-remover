import streamlit as st
import os
import urllib.request
from pathlib import Path
import time

os.environ["U2NET_HOME"] = "/home/pyodide/.u2net"

def run_actual_app():
    import bg_remover
    bg_remover.main()

def download_and_setup():
    model_path = Path("/home/pyodide/.u2net/u2net/u2net.onnx")
    
    if not model_path.exists():
        st.set_page_config(page_title="AI Setup", page_icon="⚙️")
        st.markdown("### 🚀 Phase 2: AI Model Download")
        
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        console_box = st.empty()
        
        url = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
        
        start_time = time.time()
        
        def download_report(block_num, block_size, total_size):
            downloaded = block_num * block_size
            elapsed_time = time.time() - start_time
            
            if total_size > 0:
                percent = min(int(downloaded * 100 / total_size), 100)
                # Calcolo velocità e tempo stimato
                speed = downloaded / elapsed_time if elapsed_time > 0 else 0 # bytes/s
                remaining_bytes = total_size - downloaded
                eta = remaining_bytes / speed if speed > 0 else 0
                
                progress_bar.progress(percent)
                
                # Testo di stato con ETA
                status_text.markdown(f"""
                **Progress:** {percent}% | **Speed:** {speed/(1024*1024):.2f} MB/s
                **ETA:** {int(eta // 60)}m {int(eta % 60)}s remaining
                """)
                
                console_box.code(
                    f"[DOWNLOAD] u2net.onnx\n"
                    f"[STATS]    {downloaded // (1024*1024)}MB / {total_size // (1024*1024)}MB\n"
                    f"[TIME]     Elapsed: {int(elapsed_time)}s | Remaining: {int(eta)}s"
                )

        try:
            urllib.request.urlretrieve(url, str(model_path), reporthook=download_report)
            st.success("✅ Phase 2 Complete! Launching Background Remover...")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"Setup Error: {e}")
            st.stop()
    else:
        run_actual_app()

if __name__ == "__main__":
    download_and_setup()
