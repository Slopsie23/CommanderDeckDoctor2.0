# ------------------ Mana Spinner helper ------------------
st.markdown("""
<style>
@keyframes mana-spin { 
    from { transform: rotate(0deg); } 
    to { transform: rotate(360deg); } 
}
@keyframes mana-counter { 
    from { transform: rotate(0deg); } 
    to { transform: rotate(-360deg); } 
}

.mana-spinner-wrap { 
    display:flex; 
    flex-direction:column; 
    align-items:center; 
    justify-content:center; 
    margin: 12px 0 18px; 
}
.mana-spinner { 
    position: relative; 
    width: 120px; 
    height: 120px; 
    border-radius: 50%; 
    animation: mana-spin 3s linear infinite; 
}
.mana { 
    position: absolute; 
    top: 50%; 
    left: 50%; 
    width: 36px; 
    height: 36px; 
    margin: -18px 0 0 -18px; 
    transform: rotate(calc(var(--i) * 72deg)) translate(50px); 
    transform-origin: center center; 
}
.mana .face { 
    width: 100%; 
    height: 100%; 
    animation: mana-counter 3s linear infinite; 
    transition: animation-play-state 0.2s ease; 
}
.mana-spinner:hover .face { 
    animation-play-state: paused; 
}
.mana img { 
    width: 100%; 
    height: 100%; 
    display:block; 
}
.mana-msg { 
    margin-top: 6px; 
    font-size: 14px; 
    opacity: 0.9; 
    text-align:center; 
}
</style>
""", unsafe_allow_html=True)

def show_mana_spinner(message="Bezig met laden..."):
    ph = st.empty()
    html = f"""
    <div class="mana-spinner-wrap">
        <div class="mana-spinner">
            <div class="mana" style="--i:0"><div class="face"><img src="https://svgs.scryfall.io/card-symbols/W.svg" /></div></div>
            <div class="mana" style="--i:1"><div class="face"><img src="https://svgs.scryfall.io/card-symbols/U.svg" /></div></div>
            <div class="mana" style="--i:2"><div class="face"><img src="https://svgs.scryfall.io/card-symbols/B.svg" /></div></div>
            <div class="mana" style="--i:3"><div class="face"><img src="https://svgs.scryfall.io/card-symbols/R.svg" /></div></div>
            <div class="mana" style="--i:4"><div class="face"><img src="https://svgs.scryfall.io/card-symbols/G.svg" /></div></div>
        </div>
        <div class="mana-msg">{message}</div>
    </div>
    """
    ph.markdown(html, unsafe_allow_html=True)
    return ph
