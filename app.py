import streamlit as st
from PIL import Image
import time
import os
import requests
import json
import random

# ==============================================
# 🔥 这里！把下面两个值改成你自己的！
# ==============================================
DEFAULT_API_KEY = "ark-9dc08183-212c-4c1a-a816-fb285f476a5f-a7d4c"  # 你的ark-开头的API密钥
DEFAULT_ENDPOINT_ID = "ep-20260526134725-dbn87"  # 你的ep-开头的接入点ID
DEFAULT_TEMPERATURE = 0.6

# ---------------------- 全局配置 ----------------------
st.set_page_config(
    page_title="艾草科普+小工坊平台",
    page_icon="🌿",
    layout="wide"
)

# ---------------------- 全局样式 ----------------------
hide_default_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stSlider > div > div > div > div {
    background-color: #2E7D32 !important;
}
.stProgress > div > div > div > div {
    background-color: #2E7D32 !important;
}

/* 聊天气泡样式 */
.user-message {
    background: linear-gradient(135deg, #43A047 0%, #2E7D32 100%);
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0;
    margin-left: auto;
    max-width: 75%;
    box-shadow: 0 2px 8px rgba(46, 125, 50, 0.2);
}

.assistant-message {
    background-color: #f8f9fa;
    color: #212529;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 0;
    max-width: 75%;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.chat-container {
    height: 65vh;
    overflow-y: auto;
    padding-right: 10px;
    margin-bottom: 20px;
}

/* 视频容器样式 */
.video-container {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    margin-bottom: 30px;
}

/* 隐藏所有视频的控制条 */
video::-webkit-media-controls {
    display: none !important;
}
video::-webkit-media-controls-panel {
    display: none !important;
}
video::-webkit-media-controls-play-button {
    display: none !important;
}
</style>
"""
st.markdown(hide_default_style, unsafe_allow_html=True)

# 页面标题
st.title("🌿 艾草科普+小工坊平台")
st.markdown("### 动手学艾草，零消耗练制作")
st.divider()

# ---------------------- 绿色效益计算函数 ----------------------
def calculate_green_benefits(moxa_ratio, years):
    fresh_grass = moxa_ratio * 20
    carbon_reduction = fresh_grass * 0.0002
    cost_saving = fresh_grass * 0.01
    return fresh_grass, carbon_reduction, cost_saving

# ---------------------- 艾草智能体核心函数 ----------------------
def call_ai_expert(messages, temperature=DEFAULT_TEMPERATURE):
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEFAULT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """
    你是"艾小博"，一位深耕艾草领域8年的科普专家。语气亲切、耐心、有活力。
    只回答与艾草直接相关的问题，所有回答必须科学准确，通俗易懂。
    回答结束时加上："⚠️ 以上内容仅供科普参考，不能替代专业医生的诊断和治疗"
    """
    
    full_messages = [{"role": "system", "content": system_prompt}] + messages
    
    payload = {
        "model": DEFAULT_ENDPOINT_ID,
        "messages": full_messages,
        "temperature": temperature,
        "stream": True
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, stream=True, timeout=10)
        response.raise_for_status()
        return response
    except Exception as e:
        return f"调用失败：{str(e)}"

# ---------------------- 侧边栏导航 ----------------------
with st.sidebar:
    st.header("功能导航")
    
    if "page" not in st.session_state:
        st.session_state.page = "🌱 艾草的一生"
    
    page_options = ["🌱 艾草的一生", "🪵 艾条制作工坊", "🎐 香囊制作工坊", "📚 艾草趣味科普馆", "🎮 中药功效连连看", "🤖 艾草智慧问答"]
    page = st.radio("", page_options, index=page_options.index(st.session_state.page))
    
    st.session_state.page = page
    st.divider()
    
    st.markdown("人工智能创意作品")

# ---------------------- 图片加载函数 ----------------------
def load_image(filename):
    try:
        if os.path.exists(f"images/{filename}"):
            return Image.open(f"images/{filename}")
        else:
            return None
    except:
        return None

# ---------------------- 香囊图片合并函数（坐标100%校准版） ----------------------
def merge_sachet_image(bag_style, accessories):
    # 加载底图
    if bag_style == "🏮 传统国风款":
        base_img = load_image("传统国风款.png")
    elif bag_style == "🍃 清新简约款":
        base_img = load_image("清新简约款.png")
    else:
        base_img = load_image("可爱卡通款.png")
    
    if base_img is None:
        return None
    
    # 统一底图大小
    base_img = base_img.resize((400, 400), Image.Resampling.LANCZOS)
    
    # 叠加配饰（坐标根据你的截图精确校准）
    if "彩色流苏" in accessories:
        tassel_img = load_image("彩色流苏.png")
        if tassel_img:
            tassel_img = tassel_img.resize((100, 150), Image.Resampling.LANCZOS)
            base_img.paste(tassel_img, (150, 350), tassel_img)
    
    if "丝绸蝴蝶结" in accessories:
        bow_img = load_image("丝绸蝴蝶结.png")
        if bow_img:
            bow_img = bow_img.resize((120, 90), Image.Resampling.LANCZOS)
            base_img.paste(bow_img, (140, 20), bow_img)
    
    if "木质平安符" in accessories:
        pingan_img = load_image("木质平安符.png")
        if pingan_img:
            pingan_img = pingan_img.resize((90, 120), Image.Resampling.LANCZOS)
            base_img.paste(pingan_img, (320, 50), pingan_img)
    
    return base_img

# ---------------------- 页面1：艾草的一生（完整互动版） ----------------------
if page == "🌱 艾草的一生":
    # 🎬 首页展示视频（只保留这个）
    st.markdown('<div class="video-container">', unsafe_allow_html=True)
    if os.path.exists("aicao_show.mp4"):
        st.video("https://cdn.jsdelivr.net/gh/kimaicao2029/aicao@main/展示视频.mp4")
    else:
        st.info("🎬 展示视频正在加载中... 如果没有显示，请刷新页面")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.header("📅 艾草的完整生命周期")
    st.info("拖动滑块穿越艾草的一生，点击彩蛋发现更多有趣的知识！")
    
    stage = st.slider("", 1, 6, 1, format="第%d阶段")
    st.progress(stage/6)
    st.caption(f"生命周期进度：{int(stage/6*100)}%")
    
    # 完整的生命周期数据（恢复所有互动内容）
    stages_data = {
        1: {
            "name": "播种期",
            "time": "每年3-4月",
            "ancient_saying": "清明前后，种瓜点豆，艾草亦如是。",
            "modern_science": "艾草种子发芽的最佳温度是18-22℃，发芽率约70%。",
            "description": "艾草多采用分株繁殖，成活率几乎100%。种子繁殖虽然慢，但能获得更健壮的植株。播种时需与细土混合撒播，覆土1厘米左右，保持土壤湿润。",
            "fun_fact": "艾草种子非常小，1克种子就有10000多粒！",
            "image": "01_艾草播种种植.jpg"
        },
        2: {
            "name": "发芽期",
            "time": "播种后7-15天",
            "ancient_saying": "阳春三月，百草回芽，艾草最先破土。",
            "modern_science": "艾草幼苗含有丰富的叶绿素，光合作用效率是普通植物的1.5倍。",
            "description": "幼苗呈嫩绿色，初期生长缓慢，需注意除草和浇水。当幼苗长到10-15厘米高时，即可进行间苗和移栽。艾草生命力极强，即使被踩断也能重新发芽。",
            "fun_fact": "艾草的根可以深入地下2米，所以它非常耐旱，即使几个月不下雨也能存活。",
            "image": "02_艾草幼苗发芽.jpg"
        },
        3: {
            "name": "生长期",
            "time": "5-7月",
            "ancient_saying": "五月艾草，长得比人高。",
            "modern_science": "艾草在25-30℃时生长最快，每天可以长高2-3厘米。",
            "description": "这是艾草生长最快的时期，植株高度可达1.5-2米。叶片呈羽状深裂，背面有白色绒毛，有浓郁的香气。此时需充足的阳光和水分，每月施一次有机肥。",
            "fun_fact": "艾草会释放一种特殊的化学物质，能驱赶周围的害虫，所以农民经常把艾草种在菜园边。",
            "image": "03_艾草田生长.jpg"
        },
        4: {
            "name": "收割期",
            "time": "端午节前后",
            "ancient_saying": "端午采艾，悬于门户，可避邪驱瘟。",
            "modern_science": "端午节前后，艾草的挥发油含量达到全年最高峰，药效最强。",
            "description": "这是一年中收割艾草的最佳时节。选择晴天上午收割，割取地上部分，留下根部，秋天还能再收一茬。收割后要及时摊开阴干，不能暴晒。",
            "fun_fact": "民间有\"早采三天是个宝，晚采三天是个草\"的说法，说的就是艾草收割的时机非常重要。",
            "image": "04_艾草收割.jpg"
        },
        5: {
            "name": "炮制期",
            "time": "收割后",
            "ancient_saying": "凡用艾叶，须用陈久者，治令细软，谓之熟艾。",
            "modern_science": "新艾挥发油含量过高，燃烧猛烈，容易灼伤皮肤；陈艾挥发油适中，火力温和，渗透力强。",
            "description": "新鲜艾草不能直接入药，需要经过炮制。先放在通风阴凉处阴干，然后反复捶打、筛选，去除杂质和茎秆，得到金黄色的艾绒。艾绒陈放3年以上药效最好。",
            "fun_fact": "制作1公斤30:1的极品艾绒，需要30公斤干艾草，经过上万次的捶打和筛选。",
            "image": "05_艾绒炮制.jpg"
        },
        6: {
            "name": "应用期",
            "time": "全年",
            "ancient_saying": "艾草通十二经，走三阴，理气血，逐寒湿。",
            "modern_science": "现代研究证实，艾草含有桉叶素、龙脑等多种活性成分，具有抗菌、抗病毒、抗炎、镇痛等作用。",
            "description": "艾草是中医里的\"万能草\"，用途非常广泛：✅ 艾灸：温通经络，散寒止痛 ✅ 泡脚：祛湿驱寒，改善睡眠 ✅ 食疗：艾草青团、艾草鸡蛋汤 ✅ 驱蚊：燃烧艾草，天然驱蚊",
            "fun_fact": "艾草是世界上最早被人类使用的药用植物之一，已有5000多年的历史。",
            "image": "06_艾灸应用.jpg"
        }
    }
    
    current_stage = stages_data[stage]
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        img = load_image(current_stage["image"])
        if img:
            st.image(img, caption=f"艾草·{current_stage['name']}", use_column_width=True)
        else:
            st.info(f"图片未找到：{current_stage['image']}")
        
        # 恢复彩蛋按钮
        if st.button("🥚 发现冷知识", type="secondary", use_container_width=True):
            st.info(f"💡 {current_stage['fun_fact']}")
    
    with col2:
        st.subheader(f"第{stage}阶段：{current_stage['name']}")
        st.markdown(f"**⏰ 最佳时间：** {current_stage['time']}")
        st.divider()
        
        # 恢复三个标签页
        tab1, tab2, tab3 = st.tabs(["📖 基本介绍", "👴 古人怎么说", "🔬 现代科学说"])
        
        with tab1:
            st.markdown(current_stage["description"])
        
        with tab2:
            st.markdown(f"> {current_stage['ancient_saying']}")
        
        with tab3:
            st.markdown(current_stage["modern_science"])
        
        st.divider()
        
        # 恢复一键问AI按钮
        if st.button("🤖 问艾小博更多关于这个阶段的问题", type="primary", use_container_width=True):
            # 自动跳转到智能问答页面，并预设问题
            st.session_state.chat_messages = [{"role": "user", "content": f"请详细介绍一下艾草的{current_stage['name']}"}]
            st.session_state.page = "🤖 艾草智慧问答"
            st.rerun()

# ---------------------- 页面2：艾条制作工坊 ----------------------
elif page == "🪵 艾条制作工坊":
    st.header("🪵 标准艾条制作虚拟实训")
    st.success("提示：跟着步骤完成制作，最后查看你的绿色环保贡献！")
    
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "pound_progress" not in st.session_state:
        st.session_state.pound_progress = 0
    
    st.progress((st.session_state.step-1)/4)
    st.caption(f"制作进度：{int((st.session_state.step-1)/4*100)}%")
    
    if st.session_state.step == 1:
        st.subheader("第一步：选择原料")
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            img = load_image("05_艾绒炮制.jpg")
            if img:
                st.image(img, use_column_width=True)
        
        with col2:
            years = st.select_slider("选择艾草年份", options=[1, 3, 5], value=3)
            moxa_ratio = st.select_slider("选择艾绒比例", options=[5, 10, 15, 20, 30], value=10)
            
            if st.button("下一步 →", type="primary"):
                st.session_state.years = years
                st.session_state.moxa_ratio = moxa_ratio
                st.session_state.step = 2
                st.rerun()
    
    elif st.session_state.step == 2:
        st.subheader("第二步：捶打艾绒")
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            img = load_image("08_艾绒捶打.jpg")
            if img:
                st.image(img, use_column_width=True)
        
        with col2:
            pound_bar = st.progress(st.session_state.pound_progress)
            if st.button("⚡ 快速完成", use_container_width=True):
                st.session_state.pound_progress = 100
                pound_bar.progress(100)
            
            if st.session_state.pound_progress >= 100:
                st.success("✅ 捶打完成！")
                if st.button("下一步 →", type="primary"):
                    st.session_state.step = 3
                    st.rerun()
    
    elif st.session_state.step == 3:
        st.subheader("第三步：筛选杂质")
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            img = load_image("09_艾绒筛选.jpg")
            if img:
                st.image(img, use_column_width=True)
        
        with col2:
            purity = st.slider("调整筛选纯度", 1, 100, value=70)
            st.success("✅ 纯度合适，艾绒质量良好")
            
            if st.button("下一步 →", type="primary"):
                st.session_state.purity = purity
                st.session_state.step = 4
                st.rerun()
    
    elif st.session_state.step == 4:
        st.subheader("第四步：卷制艾条")
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            img = load_image("10_手工卷艾条.jpg")
            if img:
                st.image(img, use_column_width=True)
        
        with col2:
            tightness = st.slider("调整艾条松紧度", 1, 10, value=5)
            st.success("✅ 松紧度合适！")
            
            if st.button("完成制作 ✅", type="primary"):
                st.session_state.tightness = tightness
                st.session_state.step = 5
                st.rerun()
    
    elif st.session_state.step == 5:
        st.balloons()
        st.success("🎉 恭喜你，成功制作了一根标准艾条！")
        
        fresh_grass, carbon, cost = calculate_green_benefits(
            st.session_state.moxa_ratio,
            st.session_state.years
        )
        
        st.header("🌱 你的绿色环保贡献")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="节省新鲜艾草", value=f"{fresh_grass}克")
        with col2:
            st.metric(label="减少碳排放", value=f"{carbon:.3f}千克")
        with col3:
            st.metric(label="节约成本", value=f"{cost:.2f}元")
        
        if st.button("🔄 重新制作"):
            keys_to_delete = ["step", "pound_progress", "years", "moxa_ratio", "purity", "tightness"]
            for key in keys_to_delete:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# ---------------------- 页面3：香囊制作工坊（预览图100%对齐版） ----------------------
elif page == "🎐 香囊制作工坊":
    st.header("🎐 艾草香囊制作虚拟实训")
    st.info("跟着步骤亲手制作你的专属艾草香囊！")
    
    if "sachet_step" not in st.session_state:
        st.session_state.sachet_step = 1
    if "crush_progress" not in st.session_state:
        st.session_state.crush_progress = 0
    if "stem_progress" not in st.session_state:
        st.session_state.stem_progress = 0
    if "bag_style" not in st.session_state:
        st.session_state.bag_style = "🏮 传统国风款"
    if "accessories" not in st.session_state:
        st.session_state.accessories = []
    
    st.progress((st.session_state.sachet_step-1)/4)
    st.caption(f"制作进度：{int((st.session_state.sachet_step-1)/4*100)}%")
    
    if st.session_state.sachet_step == 1:
        st.subheader("第一步：选择香囊配方")
        
        formulas = {
            "驱蚊防虫香囊": {"ingredients": {"艾草": 30, "薄荷": 10, "金银花": 10, "丁香": 5}},
            "安神助眠香囊": {"ingredients": {"艾草": 20, "薰衣草": 15, "酸枣仁": 10, "合欢花": 5}},
            "健脾开胃香囊": {"ingredients": {"艾草": 25, "陈皮": 15, "藿香": 10, "砂仁": 5}},
            "防疫避秽香囊": {"ingredients": {"艾草": 35, "苍术": 10, "白芷": 5, "石菖蒲": 5}}
        }
        
        formula_name = st.selectbox("选择你想要制作的香囊类型", list(formulas.keys()))
        formula = formulas[formula_name]
        
        col1, col2 = st.columns([1, 1.5])
        with col1:
            img = load_image("11_艾草香薰制作.jpg")
            if img:
                st.image(img, use_column_width=True)
        
        with col2:
            st.markdown("**📦 药材配比（单位：克）：**")
            for ingredient, amount in formula["ingredients"].items():
                st.text(f"• {ingredient}：{amount}g")
        
        if st.button("下一步 → 处理艾草", type="primary"):
            st.session_state.formula_name = formula_name
            st.session_state.formula = formula
            st.session_state.sachet_step = 2
            st.rerun()
    
    elif st.session_state.sachet_step == 2:
        st.subheader("第二步：处理艾草原料")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔨 揉碎艾草")
            crush_bar = st.progress(st.session_state.crush_progress)
            if st.button("反复揉搓艾草", use_container_width=True):
                st.session_state.crush_progress = min(st.session_state.crush_progress + 15, 100)
                crush_bar.progress(st.session_state.crush_progress)
            
            if st.session_state.crush_progress >= 100:
                st.success("✅ 艾草已揉碎成柔软的绒状")
        
        with col2:
            st.markdown("#### 🧹 挑出硬梗")
            stem_bar = st.progress(st.session_state.stem_progress)
            if st.button("挑出硬梗和杂质", use_container_width=True):
                st.session_state.stem_progress = min(st.session_state.stem_progress + 20, 100)
                stem_bar.progress(st.session_state.stem_progress)
            
            if st.session_state.stem_progress >= 100:
                st.success("✅ 硬梗和杂质已全部挑出")
        
        if st.session_state.crush_progress >= 100 and st.session_state.stem_progress >= 100:
            st.divider()
            if st.button("下一步 → 填充捆扎", type="primary"):
                st.session_state.sachet_step = 3
                st.rerun()
    
    elif st.session_state.sachet_step == 3:
        st.subheader("第三步：填充并捆扎香囊")
        
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            video_path = "images/香囊填充视频.mp4"
            if os.path.exists(video_path):
                st.video(video_path, format="video/mp4", autoplay=True, loop=True, muted=True)
        
        with col2:
            fill_level = st.select_slider(
                "填充饱满度",
                options=["5分满", "七八分满", "10分满"],
                value="七八分满"
            )
            
            st.success("✅ 最佳填充量！香气散发均匀，手感柔软有弹性")
            
            if st.button("🔒 收紧袋口并捆扎", type="primary", use_container_width=True):
                st.session_state.fill_level = fill_level
                st.success("✅ 袋口已用棉线扎实捆紧！")
                time.sleep(1)
                st.session_state.sachet_step = 4
                st.rerun()
    
    elif st.session_state.sachet_step == 4:
        st.subheader("第四步：装饰你的专属香囊")
        st.success("选择你喜欢的布袋款式和配饰，打造独一无二的艾草香囊！")
        
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown("#### 👜 选择布袋款式")
            bag_style = st.radio(
                "",
                ["🏮 传统国风款", "🍃 清新简约款", "🐰 可爱卡通款"],
                index=0
            )
            
            st.divider()
            
            st.markdown("#### 🎀 选择配饰（可多选）")
            accessories = []
            if st.checkbox("🧵 彩色流苏", value="彩色流苏" in st.session_state.get("accessories", [])):
                accessories.append("彩色流苏")
            if st.checkbox("🎀 丝绸蝴蝶结", value="丝绸蝴蝶结" in st.session_state.get("accessories", [])):
                accessories.append("丝绸蝴蝶结")
            if st.checkbox("🔖 木质平安符", value="木质平安符" in st.session_state.get("accessories", [])):
                accessories.append("木质平安符")
            
            st.session_state.bag_style = bag_style
            st.session_state.accessories = accessories
        
        with col2:
            st.markdown("#### 🎨 实时预览")
            preview_img = merge_sachet_image(bag_style, accessories)
            if preview_img:
                st.image(preview_img, caption="你的专属香囊预览", use_column_width=True)
        
        if st.button("✅ 完成制作！", type="primary", use_container_width=True):
            st.session_state.sachet_step = 5
            st.rerun()
    
    elif st.session_state.sachet_step == 5:
        st.balloons()
        st.success("🎉 恭喜你，成功制作了一个独一无二的艾草香囊！")
        
        st.header("🌿 你的专属香囊")
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            final_img = merge_sachet_image(st.session_state.bag_style, st.session_state.accessories)
            if final_img:
                st.image(final_img, caption="完成啦！", use_column_width=True)
        
        with col2:
            st.subheader("制作详情")
            st.markdown(f"""
            **📜 配方：** {st.session_state.formula_name}
            **👜 款式：** {st.session_state.bag_style}
            **🎀 配饰：** {', '.join(st.session_state.accessories) if st.session_state.accessories else '无'}
            """)
            
            st.divider()
            
            total_weight = sum(st.session_state.formula["ingredients"].values())
            carbon_reduction = total_weight * 0.0002
            
            st.subheader("🌱 你的绿色贡献")
            col_green1, col_green2 = st.columns(2)
            with col_green1:
                st.metric(label="节省药材总量", value=f"{total_weight}克")
            with col_green2:
                st.metric(label="减少碳排放", value=f"{carbon_reduction:.3f}千克")
        
        st.divider()
        if st.button("🔄 重新制作一个", type="primary", use_container_width=True):
            keys_to_delete = ["sachet_step", "crush_progress", "stem_progress", 
                             "formula_name", "formula", "fill_level", 
                             "bag_style", "accessories"]
            for key in keys_to_delete:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# ---------------------- 页面4：艾草趣味科普馆 ----------------------
elif page == "📚 艾草趣味科普馆":
    st.header("📚 艾草趣味科普馆")
    st.success("这里整理了关于艾草最有趣、最容易被误解的知识！")
    
    tab1, tab2, tab3, tab4 = st.tabs(["❌ 常见误区", "🥚 冷知识大全", "📜 文化故事", "🌍 全球应用"])
    
    with tab1:
        st.subheader("❌ 关于艾草的5个常见误区")
        
        myths = [
            {"myth": "艾草越陈越好", "truth": "并不是！3年陈艾是日常保健的最佳选择，5年以上的陈艾药效会逐渐下降。"},
            {"myth": "新鲜艾草可以直接艾灸", "truth": "绝对不行！新鲜艾草挥发油含量过高，燃烧猛烈，会灼伤皮肤。"},
            {"myth": "艾灸时间越长越好", "truth": "错！一般每个穴位艾灸10-15分钟即可，时间过长会导致上火。"},
            {"myth": "艾草泡脚人人都适合", "truth": "阴虚火旺、发烧、糖尿病足、严重心脏病患者不适合用艾草泡脚。"},
            {"myth": "艾草只能端午节用", "truth": "艾草全年都可以用！春天吃青团，夏天驱蚊，秋天泡脚，冬天艾灸。"}
        ]
        
        for i, myth in enumerate(myths):
            with st.expander(f"误区{i+1}：{myth['myth']}", expanded=False):
                st.markdown(f"✅ **真相：** {myth['truth']}")
    
    with tab2:
        st.subheader("🥚 你不知道的艾草冷知识")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(label="艾草的历史", value="5000+年")
            st.metric(label="1克种子的数量", value="10000+粒")
            st.metric(label="根的最大深度", value="2米")
        
        with col2:
            st.metric(label="已知的艾草品种", value="300+种")
            st.metric(label="艾草含有的活性成分", value="100+种")
            st.metric(label="最佳陈放时间", value="3年")
    
    with tab3:
        st.subheader("📜 艾草的文化故事")
        st.markdown("""
        ### 端午插艾的由来
        传说在古代，有一个瘟神每年端午节都会下凡传播瘟疫。有一位善良的老婆婆，为了保护村民，在自己家门口插上了艾草。瘟神看到艾草，以为是宝剑，吓得不敢进村。从此，端午插艾的习俗就流传了下来。
        """)
    
    with tab4:
        st.subheader("🌍 艾草在全世界的应用")
        st.markdown("""
        - **中国**：艾灸、泡脚、香囊、青团
        - **日本**：艾草年糕、艾草浴、艾灸
        - **韩国**：艾草汤、艾草煎饼、艾草化妆品
        - **欧洲**：艾草啤酒、艾草精油、驱虫剂
        """)
    
    st.divider()
    if st.button("🤖 还有其他问题？问艾小博吧！", type="primary", use_container_width=True):
        st.session_state.page = "🤖 艾草智慧问答"
        st.rerun()

# ---------------------- 页面5：中药功效连连看（彻底删除连线版） ----------------------
elif page == "🎮 中药功效连连看":
    st.header("🎮 中药功效连连看")
    st.info("点击左边的草药，再点击右边对应的功效，看看你能答对多少！")
    
    if "game_state" not in st.session_state:
        st.session_state.game_state = {
            "selected_herb": None,
            "matched_pairs": [],
            "score": 0,
            "game_complete": False
        }
    
    herb_effect_pairs = [
        {"herb": "🌿 艾草", "effect": "温经散寒，祛湿止痛", "id": 0},
        {"herb": "🌼 金银花", "effect": "清热解毒，疏散风热", "id": 1},
        {"herb": "🍃 薄荷", "effect": "疏散风热，清利头目", "id": 2},
        {"herb": "🌾 藿香", "effect": "化湿和中，发表解暑", "id": 3},
        {"herb": "🌸 红花", "effect": "活血化瘀，通经止痛", "id": 4}
    ]
    
    if "shuffled_effects" not in st.session_state:
        st.session_state.shuffled_effects = random.sample(herb_effect_pairs, len(herb_effect_pairs))
    
    if st.session_state.game_state["game_complete"]:
        st.balloons()
        st.success(f"🎉 恭喜你全部答对了！得分：{st.session_state.game_state['score']}/5")
        
        st.markdown("""
        💡 **科普小知识**
        艾草、薄荷、藿香都属于"芳香化湿药"，它们都含有挥发油，能够通过芳香之气来驱散体内的湿气。
        """)
        
        if st.button("🔄 重新开始游戏", type="primary"):
            st.session_state.game_state = {
                "selected_herb": None,
                "matched_pairs": [],
                "score": 0,
                "game_complete": False
            }
            st.session_state.shuffled_effects = random.sample(herb_effect_pairs, len(herb_effect_pairs))
            st.rerun()
    
    else:
        col_herbs, col_effects = st.columns([1, 2])
        
        with col_herbs:
            st.subheader("🌿 草药")
            st.divider()
            
            for herb in herb_effect_pairs:
                herb_id = herb["id"]
                is_matched = herb_id in [pair[0] for pair in st.session_state.game_state["matched_pairs"]]
                is_selected = st.session_state.game_state["selected_herb"] == herb_id
                
                if is_matched:
                    button_type = "primary"
                    disabled = True
                elif is_selected:
                    button_type = "primary"
                    disabled = False
                else:
                    button_type = "secondary"
                    disabled = False
                
                if st.button(
                    herb["herb"],
                    key=f"herb_{herb_id}",
                    use_container_width=True,
                    type=button_type,
                    disabled=disabled
                ):
                    if not is_matched:
                        st.session_state.game_state["selected_herb"] = herb_id
                        st.rerun()
        
        with col_effects:
            st.subheader("💊 功效")
            st.divider()
            
            for i, effect in enumerate(st.session_state.shuffled_effects):
                effect_id = effect["id"]
                is_matched = effect_id in [pair[1] for pair in st.session_state.game_state["matched_pairs"]]
                
                if is_matched:
                    button_type = "primary"
                    disabled = True
                else:
                    button_type = "secondary"
                    disabled = False
                
                if st.button(
                    effect["effect"],
                    key=f"effect_{effect_id}",
                    use_container_width=True,
                    type=button_type,
                    disabled=disabled
                ):
                    if st.session_state.game_state["selected_herb"] is not None and not is_matched:
                        selected_herb_id = st.session_state.game_state["selected_herb"]
                        
                        if selected_herb_id == effect_id:
                            st.session_state.game_state["matched_pairs"].append((selected_herb_id, effect_id))
                            st.session_state.game_state["score"] += 1
                            st.success("✅ 配对正确！")
                            
                            if len(st.session_state.game_state["matched_pairs"]) == len(herb_effect_pairs):
                                st.session_state.game_state["game_complete"] = True
                        else:
                            correct_herb = next(h["herb"] for h in herb_effect_pairs if h["id"] == effect_id)
                            st.error(f"❌ 不对哦，这是{correct_herb}的功效！")
                        
                        st.session_state.game_state["selected_herb"] = None
                        time.sleep(0.8)
                        st.rerun()
        
        st.divider()
        col_score, col_reset = st.columns([1, 1])
        with col_score:
            st.metric("当前得分", f"{st.session_state.game_state['score']}/5")
        with col_reset:
            if st.button("🔄 重新开始", use_container_width=True):
                st.session_state.game_state = {
                    "selected_herb": None,
                    "matched_pairs": [],
                    "score": 0,
                    "game_complete": False
                }
                st.session_state.shuffled_effects = random.sample(herb_effect_pairs, len(herb_effect_pairs))
                st.rerun()

# ---------------------- 页面6：艾草智慧问答智能体 ----------------------
else:
    st.header("🤖 艾草智慧问答专家")
    st.success("你好！我是艾小博，专门解答所有关于艾草的问题！")
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    st.markdown("#### 💡 热门问题，点击直接提问")
    col1, col2, col3 = st.columns(3)
    
    hot_questions = [
        "艾草什么时候收割最好？",
        "3年陈艾和5年陈艾有什么区别？",
        "艾灸有什么禁忌吗？",
        "家里怎么种艾草？",
        "驱蚊香囊的配方是什么？",
        "新鲜艾草能直接泡脚吗？"
    ]
    
    with col1:
        for q in hot_questions[:2]:
            if st.button(q, use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": q})
                st.rerun()
    
    with col2:
        for q in hot_questions[2:4]:
            if st.button(q, use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": q})
                st.rerun()
    
    with col3:
        for q in hot_questions[4:]:
            if st.button(q, use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": q})
                st.rerun()
    
    st.divider()
    
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.chat_messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    user_input = st.chat_input("输入你想问的关于艾草的问题...")
    
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        st.rerun()
    
    if st.session_state.chat_messages and st.session_state.chat_messages[-1]["role"] == "user":
        with st.spinner("艾小博正在思考中..."):
            response = call_ai_expert(
                st.session_state.chat_messages,
                DEFAULT_TEMPERATURE
            )
            
            if isinstance(response, str):
                st.error(f"{response}")
                st.info("💡 请检查代码最上面的API密钥和接入点ID是否正确！")
            else:
                full_response = ""
                message_placeholder = st.empty()
                
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = line[6:]
                            if data == '[DONE]':
                                break
                            try:
                                json_data = json.loads(data)
                                if 'choices' in json_data and len(json_data['choices']) > 0:
                                    delta = json_data['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        full_response += delta['content']
                                        with message_placeholder.container():
                                            st.markdown(f'<div class="assistant-message">{full_response}▌</div>', unsafe_allow_html=True)
                            except:
                                pass
                
                message_placeholder.markdown(f'<div class="assistant-message">{full_response}</div>', unsafe_allow_html=True)
                st.session_state.chat_messages.append({"role": "assistant", "content": full_response})
                st.rerun()
