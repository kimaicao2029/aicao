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
DEFAULT_API_KEY = "ark-xxxxxxxxxxxxxxxxxxxx"  # 你的ark-开头的API密钥
DEFAULT_ENDPOINT_ID = "ep-20260526134725-dbn8787k"  # 你的ep-开头的接入点ID
DEFAULT_TEMPERATURE = 0.6

# ---------------------- 全局配置 ----------------------
st.set_page_config(
    page_title="艾草科普+小工坊平台",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"  # 隐藏侧边栏
)

# ---------------------- 全局样式（完全模仿微信小程序风格） ----------------------
custom_css = """
<style>
/* 全局背景：浅色渐变 */
.stApp {
    background: linear-gradient(180deg, #fefefe 0%, #f0f9f0 100%);
    padding-bottom: 80px; /* 给底部导航留空间 */
}

/* 隐藏默认的streamlit元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 功能卡片样式：圆角、阴影、马卡龙配色 */
.function-card {
    background: white;
    border-radius: 16px;
    padding: 20px 10px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    transition: all 0.2s;
    cursor: pointer;
    margin-bottom: 15px;
}
.function-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

/* 图标容器：彩色圆形 */
.icon-container {
    width: 60px;
    height: 60px;
    border-radius: 16px;
    margin: 0 auto 10px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
}

/* 不同功能的马卡龙配色 */
.icon-life {background: #E8F5E9; color: #2E7D32;}
.icon-moxa {background: #FFF3E0; color: #E65100;}
.icon-sachet {background: #F3E5F5; color: #7B1FA2;}
.icon-science {background: #E3F2FD; color: #1565C0;}
.icon-game {background: #FFF8E1; color: #F57C00;}
.icon-ai {background: #E0F7FA; color: #00838F;}

/* 信息卡片样式 */
.info-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

/* 按钮样式：圆角 */
.stButton>button {
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: 500;
    transition: all 0.2s;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* 底部导航栏 */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    padding: 10px 0;
    display: flex;
    justify-content: space-around;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    z-index: 999;
}
.nav-item {
    text-align: center;
    color: #999;
    font-size: 12px;
    cursor: pointer;
}
.nav-item.active {
    color: #2E7D32;
}
.nav-item svg {
    width: 24px;
    height: 24px;
    margin-bottom: 4px;
}

/* 顶部横幅 */
.banner {
    background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.banner::after {
    content: "";
    position: absolute;
    right: 20px;
    top: 0;
    bottom: 0;
    width: 150px;
    background: url('https://img.51miz.com/Element/00/71/97/24/28657929_E919E7A3.png') no-repeat center;
    background-size: contain;
}

/* 滑块样式 */
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
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------- 顶部标题栏 ----------------------
st.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 15px;">
    <div style="width: 40px; height: 40px; border-radius: 50%; background: #2E7D32; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px; margin-right: 10px;">🌿</div>
    <div>
        <div style="font-size: 18px; font-weight: bold; color: #333;">艾草科普+小工坊平台</div>
        <div style="font-size: 12px; color: #999;">AI驱动的沉浸式学习平台</div>
    </div>
    <div style="margin-left: auto; display: flex; gap: 10px;">
        <div style="width: 30px; height: 30px; border-radius: 50%; background: #f0f0f0; display: flex; align-items: center; justify-content: center;">🔔</div>
        <div style="width: 30px; height: 30px; border-radius: 50%; background: #f0f0f0; display: flex; align-items: center; justify-content: center;">👤</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------- 绿色效益计算 ----------------------
def calculate_green_benefits(moxa_ratio, years):
    fresh_grass = moxa_ratio * 20
    carbon_reduction = fresh_grass * 0.0002
    cost_saving = fresh_grass * 0.01
    return fresh_grass, carbon_reduction, cost_saving

# ---------------------- AI专家函数 ----------------------
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

# ---------------------- 页面状态 ----------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# ---------------------- 图片加载 ----------------------
def load_image(filename):
    try:
        if os.path.exists(f"images/{filename}"):
            return Image.open(f"images/{filename}")
        else:
            return None
    except:
        return None

# ---------------------- 香囊图片合并 ----------------------
def merge_sachet_image(bag_style, accessories):
    if bag_style == "🏮 传统国风款":
        base_img = load_image("传统国风款.png")
    elif bag_style == "🍃 清新简约款":
        base_img = load_image("清新简约款.png")
    else:
        base_img = load_image("可爱卡通款.png")
    
    if base_img is None:
        return None
    
    base_img = base_img.resize((400, 400), Image.Resampling.LANCZOS)
    
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

# ---------------------- 首页：卡片式功能入口 ----------------------
def render_home():
    # 顶部横幅
    st.markdown("""
    <div class="banner">
        <div style="font-size: 20px; font-weight: bold; color: #2E7D32; margin-bottom: 10px;">欢迎回来！</div>
        <div style="font-size: 14px; color: #666; margin-bottom: 15px;">今天也要一起学习艾草知识吗？</div>
        <div style="background: white; border-radius: 8px; padding: 8px 12px; display: inline-block; font-size: 13px; color: #666;">
            📢 全平台升级：AI专家艾小博已上线！
        </div>
        <span style="float: right; color: #2E7D32; font-size: 13px;">更多公告></span>
    </div>
    """, unsafe_allow_html=True)
    
    # 功能卡片（2行3列）
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="function-card">', unsafe_allow_html=True)
        st.markdown('<div class="icon-container icon-life">🌱</div>', unsafe_allow_html=True)
        if st.button("艾草的一生", key="btn_life", use_container_width=True):
            st.session_state.current_page = "life"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="function-card">', unsafe_allow_html=True)
        st.markdown('<div class="icon-container icon-moxa">🪵</div>', unsafe_allow_html=True)
        if st.button("艾条制作", key="btn_moxa", use_container_width=True):
            st.session_state.current_page = "moxa"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="function-card">', unsafe_allow_html=True)
        st.markdown('<div class="icon-container icon-sachet">🎐</div>', unsafe_allow_html=True)
        if st.button("香囊制作", key="btn_sachet", use_container_width=True):
            st.session_state.current_page = "sachet"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown('<div class="function-card">', unsafe_allow_html=True)
        st.markdown('<div class="icon-container icon-science">📚</div>', unsafe_allow_html=True)
        if st.button("科普馆", key="btn_science", use_container_width=True):
            st.session_state.current_page = "science"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="function-card">', unsafe_allow_html=True)
        st.markdown('<div class="icon-container icon-game">🎮</div>', unsafe_allow_html=True)
        if st.button("连连看", key="btn_game", use_container_width=True):
            st.session_state.current_page = "game"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="function-card">', unsafe_allow_html=True)
        st.markdown('<div class="icon-container icon-ai">🤖</div>', unsafe_allow_html=True)
        if st.button("艾小博", key="btn_ai", use_container_width=True):
            st.session_state.current_page = "ai"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 今日学习进度卡片
    st.markdown("""
    <div class="info-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="font-weight: bold; color: #333;">今日学习进度</span>
            <span style="background: #E8F5E9; color: #2E7D32; padding: 4px 12px; border-radius: 12px; font-size: 12px;">今日课程</span>
        </div>
        <div style="font-size: 14px; color: #666;">
            <span>时间: -- </span>
            <span>| 教室: -- </span>
        </div>
        <div style="margin-top: 10px;">
            <div style="height: 6px; background: #f0f0f0; border-radius: 3px; overflow: hidden;">
                <div style="width: 35%; height: 100%; background: #2E7D32; border-radius: 3px;"></div>
            </div>
            <div style="font-size: 12px; color: #999; margin-top: 5px;">已完成 35% 的学习任务</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 快捷入口卡片
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);">
            <div style="font-size: 16px; font-weight: bold; color: #E65100; margin-bottom: 10px;">📅 我的日程</div>
            <div style="font-size: 13px; color: #666; margin-bottom: 15px;">制定你的学习计划</div>
            <button style="background: #E65100; color: white; border: none; border-radius: 8px; padding: 8px 16px; font-size: 13px;">制定计划</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);">
            <div style="font-size: 16px; font-weight: bold; color: #1565C0; margin-bottom: 10px;">📋 我的审批</div>
            <div style="font-size: 13px; color: #666; margin-bottom: 15px;">查看你的实训申请</div>
            <button style="background: #1565C0; color: white; border: none; border-radius: 8px; padding: 8px 16px; font-size: 13px;">查看审批</button>
        </div>
        """, unsafe_allow_html=True)

# ---------------------- 页面1：艾草的一生 ----------------------
def render_life():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.header("📅 艾草的完整生命周期")
    st.info("拖动滑块穿越艾草的一生，点击彩蛋发现更多有趣的知识！")
    
    stage = st.slider("", 1, 6, 1, format="第%d阶段")
    st.progress(stage/6)
    st.caption(f"生命周期进度：{int(stage/6*100)}%")
    
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
            "fun_fact": "民间有'早采三天是个宝，晚采三天是个草'的说法，说的就是艾草收割的时机非常重要。",
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
            "description": "艾草是中医里的'万能草'，用途非常广泛：✅ 艾灸：温通经络，散寒止痛 ✅ 泡脚：祛湿驱寒，改善睡眠 ✅ 食疗：艾草青团、艾草鸡蛋汤 ✅ 驱蚊：燃烧艾草，天然驱蚊",
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
        
        if st.button("🥚 发现冷知识", type="secondary", use_container_width=True):
            st.info(f"💡 {current_stage['fun_fact']}")
    
    with col2:
        st.subheader(f"第{stage}阶段：{current_stage['name']}")
        st.markdown(f"**⏰ 最佳时间：** {current_stage['time']}")
        st.divider()
        
        tab1, tab2, tab3 = st.tabs(["📖 基本介绍", "👴 古人怎么说", "🔬 现代科学说"])
        
        with tab1:
            st.markdown(current_stage["description"])
        
        with tab2:
            st.markdown(f"> {current_stage['ancient_saying']}")
        
        with tab3:
            st.markdown(current_stage["modern_science"])
        
        st.divider()
        
        if st.button("🤖 问艾小博更多关于这个阶段的问题", type="primary", use_container_width=True):
            st.session_state.chat_messages = [{"role": "user", "content": f"请详细介绍一下艾草的{current_stage['name']}"}]
            st.session_state.current_page = "ai"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("← 返回首页", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()

# ---------------------- 页面2：艾条制作工坊 ----------------------
def render_moxa():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
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
            
            if st.button("下一步 →", type="primary", use_container_width=True):
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
                if st.button("下一步 →", type="primary", use_container_width=True):
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
            
            if st.button("下一步 →", type="primary", use_container_width=True):
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
            
            if st.button("完成制作 ✅", type="primary", use_container_width=True):
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
        
        if st.button("🔄 重新制作", use_container_width=True):
            keys_to_delete = ["step", "pound_progress", "years", "moxa_ratio", "purity", "tightness"]
            for key in keys_to_delete:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("← 返回首页", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()

# ---------------------- 页面3：香囊制作工坊 ----------------------
def render_sachet():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
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
        
        if st.button("下一步 → 处理艾草", type="primary", use_container_width=True):
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
            if st.button("下一步 → 填充捆扎", type="primary", use_container_width=True):
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
    
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("← 返回首页", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()

# ---------------------- 页面4：艾草趣味科普馆 ----------------------
def render_science():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
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
        st.session_state.current_page = "ai"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("← 返回首页", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()

# ---------------------- 页面5：中药功效连连看 ----------------------
def render_game():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
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
        
        if st.button("🔄 重新开始游戏", type="primary", use_container_width=True):
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
    
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("← 返回首页", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()

# ---------------------- 页面6：艾草智慧问答智能体 ----------------------
def render_ai():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
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
    
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("← 返回首页", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()

# ---------------------- 底部导航栏 ----------------------
st.markdown("""
<div class="bottom-nav">
    <div class="nav-item active">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
        <div>首页</div>
    </div>
    <div class="nav-item">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 4h5v8l-2.5-1.5L6 12V4z"/></svg>
        <div>课程</div>
    </div>
    <div class="nav-item">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
        <div>消息</div>
    </div>
    <div class="nav-item">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
        <div>我的</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------- 渲染当前页面 ----------------------
if st.session_state.current_page == "home":
    render_home()
elif st.session_state.current_page == "life":
    render_life()
elif st.session_state.current_page == "moxa":
    render_moxa()
elif st.session_state.current_page == "sachet":
    render_sachet()
elif st.session_state.current_page == "science":
    render_science()
elif st.session_state.current_page == "game":
    render_game()
elif st.session_state.current_page == "ai":
    render_ai()