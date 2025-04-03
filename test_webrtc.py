import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import numpy as np
import matplotlib.pyplot as plt

class AudioProcessor:
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.frames.append(frame.to_ndarray().flatten())
        return frame

st.title("🧪 WebRTC テスト画面")
st.write("マイクをONにして、Stop後に波形が見えたら録音成功です！")

ctx = webrtc_streamer(
    key="mic-test",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=256,
    media_stream_constraints={"video": False, "audio": True},
    audio_processor_factory=AudioProcessor,
    async_processing=True,
)

if ctx.audio_processor and len(ctx.audio_processor.frames) > 0:
    st.success(f"✅ フレーム取得中: {len(ctx.audio_processor.frames)} 個")

    data = np.concatenate(ctx.audio_processor.frames)
    fig, ax = plt.subplots()
    ax.plot(data[-1000:])
    st.pyplot(fig)
else:
    st.warning("⚠️ フレームが取得できていません。マイクが動いていない可能性があります。")
