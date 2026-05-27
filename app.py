import streamlit as st
from PIL import Image
import time
import os
import requests
import json
import random

# ---------------------- 全局配置 ----------------------
st.set_page_config(
    page_title="艾草科普+小工坊平台",
    page_icon="🌿",
    layout="wide"
)

# 隐藏Streamlit默认元素，美化界面
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

/* 连线样式 */
.connection-line {
    position: absolute;
    height: 3px;
    background-color: #2E7D32;
    z-index: 1000;
    transform-origin: left center;
}

/* 视频容器样式 */
.video-container {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    margin-bottom: 30px;
}

/* 选中按钮的样式 */
.selected-button {
    background-color: #c8e6c9 !important;
    border-color: #2E7D32 !important;
    color: #1b5e20 !important;
}
</style>
"""
st.markdown(hide_default_style, unsafe_allow_html=True)

# 页面标题
st.title("🌿 艾草科普+小工坊平台")
st.markdown("### 动手学艾草，零消耗练制作")
st.divider()

# 🎬 首页展示视频（只保留这个）
st.markdown('<div class="video-container">', unsafe_allow_html=True)
if os.path.exists("aicao_show.mp4"):
    st.video("aicao_show.mp4", format="video/mp4", start_time=0)
else:
    st.info("🎬 展示视频正在加载中... 如果没有显示，请刷新页面")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- 绿色效益计算函数 ----------------------
def calculate_green_benefits(moxa_ratio, years):
    # 行业标准数据：制作1根18*200mm标准艾条需20克艾绒
    fresh_grass = moxa_ratio * 20  # 单位：克
    carbon_reduction = fresh_grass * 0.0002  # 单位：千克
    cost_saving = fresh_grass * 0.01  # 单位：元
    return fresh_grass, carbon_reduction, cost_saving

# ---------------------- 艾草智能体核心函数（内置密钥版） ----------------------
# 内置用户的密钥，用户不用自己输入了
DEFAULT_API_KEY = "ark-xxxxxxxxxxxxxxxxxxxx"  # 从用户截图获取的密钥
DEFAULT_ENDPOINT_ID = "ep-20260526134725-dbn8787k"  # 从用户截图获取的接入点ID
DEFAULT_TEMPERATURE = 0.6

def call_ai_expert(messages, temperature=DEFAULT_TEMPERATURE):
    """调用火山方舟DeepSeek-V4-Flash API，实现艾草专家问答（内置密钥）"""
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEFAULT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 艾草专家系统提示词（专业优化版）
    system_prompt = """
    你是"艾小博"，一位深耕艾草领域8年的科普专家，同时也是传统中医药文化的年轻传播者。
    你的语气亲切、耐心、有活力，像一个懂艾草的好朋友，适合给中小学生和普通大众做科普。

    【核心原则】
    1. 只回答与艾草直接相关的问题，绝对不回答无关话题
    2. 所有回答必须科学准确，有权威依据，不编造信息
    3. 语言通俗易懂，把复杂的中医和农业知识讲得简单有趣
    4. 永远保持积极正面的态度，传播正确的艾草知识

    【你精通的知识领域】
    ✅ 生长与种植：生命周期、播种时间、土壤要求、水肥管理、病虫害防治、不同产地艾草的区别（蕲艾、南阳艾等）
    ✅ 采收与炮制：最佳采收时间、阴干方法、陈化原理、艾绒制作工艺、不同比例艾绒的区别
    ✅ 产品与应用：艾条、艾柱、艾饼、香囊、泡脚包、艾草食品的制作和使用方法
    ✅ 功效与禁忌：中医理论中的性味归经、现代科学研究证实的功效、不同人群的使用禁忌
    ✅ 文化与历史：端午插艾的由来、艾草在古代的应用、相关的诗词和民间传说
    ✅ 绿色与环保：艾草的固碳能力、虚拟实训的环保意义、艾草产业的可持续发展
    ✅ 常见误区：新鲜艾草不能直接艾灸、不是越陈越好、艾灸不是包治百病等

    【回答黄金法则】
    1. 结构化回答：多用分点（1. 2. 3.）和加粗**重点**，让用户一眼就能看到关键信息
    2. 加入实用小贴士：每回答一个问题，尽量加一个💡小提示或⚠️避坑指南
    3. 结合平台功能：如果用户问制作相关的问题，可以说"你可以在我们的【艾条制作工坊】里体验这个过程哦！"
    4. 纠正错误认知：如果用户有错误的理解，要温和地纠正，并给出正确的解释
    5. 引导深入提问：回答结束时，可以说"你还想了解关于艾草的什么知识呢？"
    6. 医疗免责声明：所有涉及健康的回答，最后必须加上"⚠️ 以上内容仅供科普参考，不能替代专业医生的诊断和治疗"

    【无关问题回复模板】
    "抱歉呀😉 我是专门的艾草科普小助手，只能回答和艾草相关的问题。关于艾草的种植、制作、功效、文化，我都可以帮你解答哦！"

    现在，用你专业又亲切的语气，开始为用户解答关于艾草的问题吧！
    """
    
    # 构造消息列表
    full_messages = [{"role": "system", "content": system_prompt}] + messages
    
    payload = {
        "model": DEFAULT_ENDPOINT_ID,
        "messages": full_messages,
        "temperature": temperature,
        "stream": True,
        "stream_options": {"include_usage": False}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, stream=True)
        response.raise_for_status()
        return response
    except Exception as e:
        return str(e)

# ---------------------- 侧边栏导航 ----------------------
with st.sidebar:
    st.header("功能导航")
    
    # 初始化页面状态
    if "page" not in st.session_state:
        st.session_state.page = "🌱 艾草的一生"
    
    page_options = ["🌱 艾草的一生", "🪵 艾条制作工坊", "🎐 香囊制作工坊", "📚 艾草趣味科普馆", "🎮 中药功效连连看", "🤖 艾草智慧问答"]
    page = st.radio(
        "",
        page_options,
        index=page_options.index(st.session_state.page)
    )
    
    # 同步页面状态
    st.session_state.page = page
    st.divider()
    
    st.markdown("人工智能创意作品")

# 终极图片加载函数
def load_image(filename):
    try:
        # 先尝试相对路径
        if os.path.exists(f"images/{filename}"):
            return Image.open(f"images/{filename}")
        # 再尝试绝对路径
        elif os.path.exists(f"C:/Users/Administrator/Desktop/images/{filename}"):
            return Image.open(f"C:/Users/Administrator/Desktop/images/{filename}")
        # 都找不到就返回None
        else:
            return None
    except Exception as e:
        st.warning(f"图片加载失败：{filename}")
        return None

# ---------------------- 香囊图片合并函数 ----------------------
def merge_sachet_image(bag_style, accessories):
    """合并香囊底图和配饰图"""
    # 加载底图
    if bag_style == "🏮 传统国风款":
        base_img = load_image("bag_traditional.jpg")
    elif bag_style == "🍃 清新简约款":
        base_img = load_image("bag_simple.jpg")
    else:  # 可爱卡通款
        base_img = load_image("bag_cute.jpg")
    
    if base_img is None:
        return None
    
    # 调整底图大小
    base_img = base_img.resize((400, 400), Image.Resampling.LANCZOS)
    
    # 加载配饰并叠加
    if "彩色流苏" in accessories:
        tassel_img = load_image("accessory_tassel.jpg")
        if tassel_img:
            tassel_img = tassel_img.resize((80, 200), Image.Resampling.LANCZOS)
            # 放在底部中间
            base_img.paste(tassel_img, (160, 320), tassel_img if tassel_img.mode == 'RGBA' else None)
    
    if "丝绸蝴蝶结" in accessories:
        bow_img = load_image("accessory_bow.jpg")
        if bow_img:
            bow_img = bow_img.resize((120, 80), Image.Resampling.LANCZOS)
            # 放在顶部中间
            base_img.paste(bow_img, (140, -20), bow_img if bow_img.mode == 'RGBA' else None)
    
    if "木质平安符" in accessories:
        pingan_img = load_image("accessory_pingan.jpg")
        if pingan_img:
            pingan_img = pingan_img.resize((80, 100), Image.Resampling.LANCZOS)
            # 放在右侧
            base_img.paste(pingan_img, (330, 50), pingan_img if pingan_img.mode == 'RGBA' else None)
    
    return base_img

# ---------------------- 页面1：艾草时间线博物馆 ----------------------
if page == "🌱 艾草的一生":
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
        
        # 彩蛋按钮
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
        
        # 一键问AI按钮
        if st.button("🤖 问艾小博更多关于这个阶段的问题", type="primary", use_container_width=True):
            # 自动跳转到智能问答页面，并预设问题
            st.session_state.chat_messages = [{"role": "user", "content": f"请详细介绍一下艾草的{current_stage['name']}"}]
            st.session_state.page = "🤖 艾草智慧问答"
            st.rerun()

# ---------------------- 页面2：艾条制作工坊 ----------------------
elif page == "🪵 艾条制作工坊":
    st.header("🪵 标准艾条制作虚拟实训")
    st.success("提示：跟着步骤完成制作，最后查看你的绿色环保贡献！")
    
    # 初始化会话状态（增加边界检查）
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "pound_progress" not in st.session_state:
        st.session_state.pound_progress = 0
    else:
        # 强制限制进度值在0-100之间
        st.session_state.pound_progress = max(0, min(st.session_state.pound_progress, 100))
    
    # 制作进度条（兼容所有版本）
    st.progress((st.session_state.step-1)/4)
    st.caption(f"制作进度：{int((st.session_state.step-1)/4*100)}%")
    
    # 步骤1：选料
    if st.session_state.step == 1:
        st.subheader("第一步：选择原料")
        col1, col2 = st.columns(2)
        
        with col1:
            img = load_image("05_艾绒炮制.jpg")
            if img:
                st.image(img, use_column_width=True)
            else:
                st.info("图片未找到")
        
        with col2:
            years = st.select_slider(
                "选择艾草年份",
                options=[1, 3, 5],
                value=3,
                help="陈艾药效更温和，火力更持久"
            )
            moxa_ratio = st.select_slider(
                "选择艾绒比例",
                options=[5, 10, 15, 20, 30],
                value=10,
                help="比例越高，艾绒越纯，燃烧效果越好"
            )
            
            st.markdown(f"""
            **📚 知识点：**
            - {years}年陈艾：经过{years}年陈放，挥发油含量适中，适合日常保健
            - {moxa_ratio}:1艾绒：{moxa_ratio}公斤新鲜艾草才能制成1公斤艾绒
            """)
            
            if st.button("下一步 →", type="primary"):
                st.session_state.years = years
                st.session_state.moxa_ratio = moxa_ratio
                st.session_state.step = 2
                st.rerun()
    
    # 步骤2：捶打
    elif st.session_state.step == 2:
        st.subheader("第二步：捶打艾绒")
        col1, col2 = st.columns(2)
        
        with col1:
            img = load_image("08_艾绒捶打.jpg")
            if img:
                st.image(img, use_column_width=True)
            else:
                st.info("图片未找到")
        
        with col2:
            st.markdown("反复捶打艾草，直到变成柔软的艾绒。捶打次数越多，艾绒越细腻。")
            
            pound_bar = st.progress(st.session_state.pound_progress)
            col_pound1, col_pound2 = st.columns(2)
            with col_pound1:
                if st.button("🔨 捶打一次"):
                    # 修复进度条溢出问题
                    st.session_state.pound_progress = min(st.session_state.pound_progress + 10, 100)
                    pound_bar.progress(st.session_state.pound_progress)
            with col_pound2:
                if st.button("⚡ 快速完成"):
                    st.session_state.pound_progress = 100
                    pound_bar.progress(100)
            
            if st.session_state.pound_progress >= 100:
                st.success("✅ 捶打完成！艾绒变得柔软细腻")
                if st.button("下一步 →", type="primary"):
                    st.session_state.step = 3
                    st.rerun()
    
    # 步骤3：筛选
    elif st.session_state.step == 3:
        st.subheader("第三步：筛选杂质")
        col1, col2 = st.columns(2)
        
        with col1:
            img = load_image("09_艾绒筛选.jpg")
            if img:
                st.image(img, use_column_width=True)
            else:
                st.info("图片未找到")
        
        with col2:
            purity = st.slider(
                "调整筛选纯度",
                1, 100,
                value=50,
                help="纯度越高，去除的杂质越多"
            )
            
            if purity < 70:
                st.warning("⚠️ 纯度太低，艾绒中含有较多茎秆和杂质，会影响燃烧效果")
            else:
                st.success("✅ 纯度合适，艾绒质量良好")
            
            if st.button("下一步 →", type="primary"):
                st.session_state.purity = purity
                st.session_state.step = 4
                st.rerun()
    
    # 步骤4：卷制
    elif st.session_state.step == 4:
        st.subheader("第四步：卷制艾条")
        col1, col2 = st.columns(2)
        
        with col1:
            img = load_image("10_手工卷艾条.jpg")
            if img:
                st.image(img, use_column_width=True)
            else:
                st.info("图片未找到")
        
        with col2:
            tightness = st.slider(
                "调整艾条松紧度",
                1, 10,
                value=5,
                help="松紧度适中的艾条燃烧均匀，火力持久"
            )
            
            st.markdown(f"当前松紧度：{tightness}/10")
            if tightness < 3:
                st.warning("⚠️ 太松了！艾条容易熄灭，燃烧速度快")
            elif tightness > 8:
                st.warning("⚠️ 太紧了！艾条燃烧不充分，容易产生浓烟")
            else:
                st.success("✅ 松紧度合适！")
            
            if st.button("完成制作 ✅", type="primary"):
                st.session_state.tightness = tightness
                st.session_state.step = 5
                st.rerun()
    
    # 步骤5：完成与绿色效益
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
        
        st.markdown("""
        💡 **绿色科普小知识**
        传统中医药实训中，每个学生制作10根艾条就要消耗约2公斤新鲜艾草，
        且不合格率高达60%。使用虚拟实训系统，不仅零原料消耗，
        还能避免明火带来的安全隐患，让学习者先熟练掌握技能再进行真实操作。
        """)
        
        if st.button("🔄 重新制作"):
            # 只删除艾条制作相关的状态，不影响其他页面
            keys_to_delete = ["step", "pound_progress", "years", "moxa_ratio", "purity", "tightness"]
            for key in keys_to_delete:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# ---------------------- 页面3：香囊制作工坊（真实图片叠加版） ----------------------
elif page == "🎐 香囊制作工坊":
    st.header("🎐 艾草香囊制作虚拟实训")
    st.info("跟着步骤亲手制作你的专属艾草香囊，体验传统手工艺的魅力！")
    
    # 初始化会话状态
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
    
    # 制作总进度条
    st.progress((st.session_state.sachet_step-1)/4)
    st.caption(f"制作进度：{int((st.session_state.sachet_step-1)/4*100)}%")
    
    # 步骤1：选择配方
    if st.session_state.sachet_step == 1:
        st.subheader("第一步：选择香囊配方")
        
        formulas = {
            "驱蚊防虫香囊": {
                "ingredients": {"艾草": 30, "薄荷": 10, "金银花": 10, "丁香": 5},
                "effect": "天然驱蚊，清新空气",
                "suitable": "夏季卧室、客厅、车内使用"
            },
            "安神助眠香囊": {
                "ingredients": {"艾草": 20, "薰衣草": 15, "酸枣仁": 10, "合欢花": 5},
                "effect": "宁心安神，改善睡眠质量",
                "suitable": "失眠多梦人群，放于枕头边"
            },
            "健脾开胃香囊": {
                "ingredients": {"艾草": 25, "陈皮": 15, "藿香": 10, "砂仁": 5},
                "effect": "健脾化湿，增进食欲",
                "suitable": "脾胃虚弱、消化不良人群"
            },
            "防疫避秽香囊": {
                "ingredients": {"艾草": 35, "苍术": 10, "白芷": 5, "石菖蒲": 5},
                "effect": "芳香化浊，避秽防疫",
                "suitable": "公共场所佩戴，增强抵抗力"
            }
        }
        
        formula_name = st.selectbox("选择你想要制作的香囊类型", list(formulas.keys()))
        formula = formulas[formula_name]
        
        col1, col2 = st.columns([1, 1.5])
        with col1:
            img = load_image("11_艾草香薰制作.jpg")
            if img:
                st.image(img, use_column_width=True)
            else:
                st.info("图片未找到")
        
        with col2:
            st.markdown(f"**✨ 功效：** {formula['effect']}")
            st.markdown(f"**📍 适用场景：** {formula['suitable']}")
            st.divider()
            
            st.markdown("**📦 药材配比（单位：克）：**")
            for ingredient, amount in formula["ingredients"].items():
                st.text(f"• {ingredient}：{amount}g")
        
        if st.button("下一步 → 处理艾草", type="primary"):
            st.session_state.formula_name = formula_name
            st.session_state.formula = formula
            st.session_state.sachet_step = 2
            st.rerun()
    
    # 步骤2：处理艾草
    elif st.session_state.sachet_step == 2:
        st.subheader("第二步：处理艾草原料")
        st.info("将干艾草揉碎，仔细挑出硬梗，让艾绒变得蓬松柔软，香气才能更好地散发出来。")
        
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
    
    # 步骤3：填充及捆扎
    elif st.session_state.sachet_step == 3:
        st.subheader("第三步：填充并捆扎香囊")
        
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            img = load_image("12_香囊填充.jpg")
            if img:
                st.image(img, use_column_width=True)
            else:
                st.info("图片未找到")
        
        with col2:
            st.markdown("#### 📏 选择填充量")
            fill_level = st.select_slider(
                "填充饱满度",
                options=["5分满", "七八分满", "10分满"],
                value="七八分满"
            )
            
            # 不同填充量的反馈
            if fill_level == "5分满":
                st.warning("⚠️ 填充较少，香气较淡，晃动时内部会有较大空隙")
            elif fill_level == "七八分满":
                st.success("✅ 最佳填充量！香气散发均匀，手感柔软有弹性")
            else:
                st.warning("⚠️ 填充过满，袋口难以收紧，香气不易散发，容易漏料")
            
            st.divider()
            
            if st.button("🔒 收紧袋口并捆扎", type="primary", use_container_width=True):
                st.session_state.fill_level = fill_level
                st.success("✅ 袋口已用棉线扎实捆紧，不会漏料！")
                time.sleep(1)
                st.session_state.sachet_step = 4
                st.rerun()
    
    # 步骤4：装饰美化（真实图片叠加版）
    elif st.session_state.sachet_step == 4:
        st.subheader("第四步：装饰你的专属香囊")
        st.info("选择你喜欢的布袋款式和配饰，打造独一无二的艾草香囊！点击选项，左边预览会实时更新！")
        
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
            
            # 保存选择到session_state
            st.session_state.bag_style = bag_style
            st.session_state.accessories = accessories
            
            if not accessories:
                st.info("你可以选择不添加任何配饰，保持简约风格")
        
        with col2:
            st.markdown("#### 🎨 实时预览")
            st.markdown(f"""
            **款式：** {bag_style}
            **配方：** {st.session_state.formula_name}
            **填充量：** {st.session_state.fill_level}
            **配饰：** {', '.join(accessories) if accessories else '无'}
            """)
            
            # 合并图片并显示
            preview_img = merge_sachet_image(bag_style, accessories)
            if preview_img:
                st.image(preview_img, caption="你的专属香囊预览", use_column_width=True)
            else:
                st.info("图片加载中...")
        
        if st.button("✅ 完成制作！", type="primary", use_container_width=True):
            st.session_state.sachet_step = 5
            st.rerun()
    
    # 步骤5：完成展示
    elif st.session_state.sachet_step == 5:
        st.balloons()
        st.success("🎉 恭喜你，成功制作了一个独一无二的艾草香囊！")
        
        st.header("🌿 你的专属香囊")
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            # 生成最终成品图片
            final_img = merge_sachet_image(st.session_state.bag_style, st.session_state.accessories)
            if final_img:
                st.image(final_img, caption="完成啦！", use_column_width=True)
            else:
                st.info("图片加载中...")
        
        with col2:
            st.subheader("制作详情")
            st.markdown(f"""
            **📜 配方：** {st.session_state.formula_name}
            **👜 款式：** {st.session_state.bag_style}
            **📏 填充量：** {st.session_state.fill_level}
            **🎀 配饰：** {', '.join(st.session_state.accessories) if st.session_state.accessories else '无'}
            """)
            
            st.divider()
            
            # 绿色环保贡献
            total_weight = sum(st.session_state.formula["ingredients"].values())
            carbon_reduction = total_weight * 0.0002
            
            st.subheader("🌱 你的绿色贡献")
            col_green1, col_green2 = st.columns(2)
            with col_green1:
                st.metric(label="节省药材总量", value=f"{total_weight}克")
            with col_green2:
                st.metric(label="减少碳排放", value=f"{carbon_reduction:.3f}千克")
        
        st.divider()
        col_restart, col_share = st.columns(2)
        with col_restart:
            if st.button("🔄 重新制作一个", type="primary", use_container_width=True):
                # 清除香囊相关状态
                keys_to_delete = ["sachet_step", "crush_progress", "stem_progress", 
                                 "formula_name", "formula", "fill_level", 
                                 "bag_style", "accessories"]
                for key in keys_to_delete:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        with col_share:
            st.info("💡 你可以把这个香囊截图分享给你的朋友哦！")

# ---------------------- 页面4：艾草趣味科普馆 ----------------------
elif page == "📚 艾草趣味科普馆":
    st.header("📚 艾草趣味科普馆")
    st.success("这里整理了关于艾草最有趣、最容易被误解的知识，智能问答可不会主动告诉你这些哦！")
    
    tab1, tab2, tab3, tab4 = st.tabs(["❌ 常见误区", "🥚 冷知识大全", "📜 文化故事", "🌍 全球应用"])
    
    with tab1:
        st.subheader("❌ 关于艾草的9个常见误区")
        
        myths = [
            {
                "myth": "艾草越陈越好",
                "truth": "并不是！3年陈艾是日常保健的最佳选择，5年以上的陈艾药效会逐渐下降，而且容易滋生霉菌。市面上所谓的\"10年陈艾\"几乎都是假的。"
            },
            {
                "myth": "新鲜艾草可以直接艾灸",
                "truth": "绝对不行！新鲜艾草挥发油含量过高，燃烧猛烈，火力暴躁，不仅没有疗效，还会灼伤皮肤，产生大量有害烟雾。"
            },
            {
                "myth": "艾灸时间越长越好",
                "truth": "错！一般每个穴位艾灸10-15分钟即可，时间过长会导致上火、头晕、乏力等不适。"
            },
            {
                "myth": "艾草泡脚人人都适合",
                "truth": "阴虚火旺、发烧、糖尿病足、严重心脏病患者不适合用艾草泡脚。孕妇和经期女性也要慎用。"
            },
            {
                "myth": "艾草只能端午节用",
                "truth": "艾草全年都可以用！春天可以吃艾草青团，夏天可以用艾草驱蚊，秋天可以用艾草泡脚，冬天可以用艾草艾灸。"
            }
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
        
        st.divider()
        
        fun_facts = [
            "艾草是唯一一种被写入二十四节气的药用植物。",
            "宇航员在太空中用艾草提取物来净化空气。",
            "日本有一个\"艾草节\"，每年5月5日举行。",
            "艾草可以用来制作天然染料，染出漂亮的黄绿色。",
            "蜜蜂非常喜欢艾草花，艾草蜜是一种非常珍贵的蜂蜜。"
        ]
        
        for fact in fun_facts:
            st.markdown(f"• 💡 {fact}")
    
    with tab3:
        st.subheader("📜 艾草的文化故事")
        
        st.markdown("""
        ### 端午插艾的由来
        传说在古代，有一个瘟神每年端午节都会下凡传播瘟疫。有一位善良的老婆婆，为了保护村民，在自己家门口插上了艾草。瘟神看到艾草，以为是宝剑，吓得不敢进村。从此，端午插艾的习俗就流传了下来。
        
        ### 艾草与屈原
        相传屈原投江后，人们为了防止鱼虾啃食他的身体，就往江里扔粽子和艾草。艾草的香气可以驱赶鱼虾，还能净化江水。
        
        ### 艾草与中医
        艾草是中医里最重要的药用植物之一，被称为"医草"。李时珍在《本草纲目》中记载："艾叶生则微苦太辛，熟则微辛太苦，生温熟热，纯阳也。可以取太阳真火，可以回垂绝元阳。"
        """)
    
    with tab4:
        st.subheader("🌍 艾草在全世界的应用")
        
        st.markdown("""
        - **中国**：艾灸、泡脚、香囊、青团
        - **日本**：艾草年糕、艾草浴、艾灸
        - **韩国**：艾草汤、艾草煎饼、艾草化妆品
        - **欧洲**：艾草啤酒、艾草精油、驱虫剂
        - **非洲**：用艾草治疗疟疾和腹泻
        """)
        
        st.info("艾草是真正的\"世界植物\"，在全世界几乎所有国家都有应用，这在药用植物中是非常罕见的。")
    
    st.divider()
    
    # 一键问AI按钮
    if st.button("🤖 还有其他问题？问艾小博吧！", type="primary", use_container_width=True):
        st.session_state.page = "🤖 艾草智慧问答"
        st.rerun()

# ---------------------- 页面5：中药功效连连看（修复版） ----------------------
elif page == "🎮 中药功效连连看":
    st.header("🎮 中药功效连连看")
    st.info("点击左边的草药，再点击右边对应的功效，正确就会画出连线！选中的草药会变成绿色哦~")
    
    # 初始化游戏状态
    if "game_state" not in st.session_state:
        st.session_state.game_state = {
            "selected_herb": None,
            "matched_pairs": [],
            "score": 0,
            "game_complete": False
        }
    
    # 草药-功效配对数据
    herb_effect_pairs = [
        {"herb": "🌿 艾草", "effect": "温经散寒，祛湿止痛", "id": 0},
        {"herb": "🌼 金银花", "effect": "清热解毒，疏散风热", "id": 1},
        {"herb": "🍃 薄荷", "effect": "疏散风热，清利头目", "id": 2},
        {"herb": "🌾 藿香", "effect": "化湿和中，发表解暑", "id": 3},
        {"herb": "🌸 红花", "effect": "活血化瘀，通经止痛", "id": 4}
    ]
    
    # 打乱右边功效的顺序
    if "shuffled_effects" not in st.session_state:
        st.session_state.shuffled_effects = random.sample(herb_effect_pairs, len(herb_effect_pairs))
    
    # 游戏完成提示
    if st.session_state.game_state["game_complete"]:
        st.balloons()
        st.success(f"🎉 恭喜你全部答对了！得分：{st.session_state.game_state['score']}/5")
        
        st.markdown("""
        💡 **科普小知识**
        艾草、薄荷、藿香都属于"芳香化湿药"，它们都含有挥发油，能够通过芳香之气来驱散体内的湿气。
        这也是为什么它们经常被一起用来制作香囊和驱蚊药包的原因！
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
        # 游戏主界面：左右两列布局
        col_herbs, col_lines, col_effects = st.columns([2, 1, 3])
        
        # 左边：草药列
        with col_herbs:
            st.subheader("🌿 草药")
            st.divider()
            
            for herb in herb_effect_pairs:
                herb_id = herb["id"]
                is_matched = herb_id in [pair[0] for pair in st.session_state.game_state["matched_pairs"]]
                is_selected = st.session_state.game_state["selected_herb"] == herb_id
                
                # 按钮样式
                if is_matched:
                    button_type = "primary"
                    disabled = True
                elif is_selected:
                    # 选中的按钮，用primary样式，变成绿色
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
        
        # 中间：连线区域
        with col_lines:
            # 绘制已经匹配成功的连线
            for pair in st.session_state.game_state["matched_pairs"]:
                herb_id, effect_id = pair
                # 准确计算每个按钮的y坐标，修复错位问题
                herb_y = 80 + herb_id * 50
                effect_index = [e["id"] for e in st.session_state.shuffled_effects].index(effect_id)
                effect_y = 80 + effect_index * 50
                
                # 计算连线长度和角度
                line_length = 200
                angle = (effect_y - herb_y) / line_length * 180 / 3.14159
                
                st.markdown(f"""
                <div class="connection-line" style="
                    top: {herb_y}px;
                    left: 320px;
                    width: {line_length}px;
                    transform: rotate({angle}deg);
                "></div>
                """, unsafe_allow_html=True)
        
        # 右边：功效列
        with col_effects:
            st.subheader("💊 功效")
            st.divider()
            
            for i, effect in enumerate(st.session_state.shuffled_effects):
                effect_id = effect["id"]
                is_matched = effect_id in [pair[1] for pair in st.session_state.game_state["matched_pairs"]]
                
                # 按钮样式
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
                        
                        # 判断是否匹配正确
                        if selected_herb_id == effect_id:
                            st.session_state.game_state["matched_pairs"].append((selected_herb_id, effect_id))
                            st.session_state.game_state["score"] += 1
                            st.success("✅ 配对正确！")
                            
                            # 检查是否全部完成
                            if len(st.session_state.game_state["matched_pairs"]) == len(herb_effect_pairs):
                                st.session_state.game_state["game_complete"] = True
                        else:
                            st.error("❌ 配对错误，请再试一次！")
                        
                        # 清除选中状态
                        st.session_state.game_state["selected_herb"] = None
                        time.sleep(0.8)
                        st.rerun()
        
        # 底部：游戏信息
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

# ---------------------- 页面6：艾草智慧问答智能体（内置密钥版） ----------------------
else:
    st.header("🤖 艾草智慧问答专家")
    st.success("你好！我是艾小博，专门解答所有关于艾草的问题，有什么想问我的吗？")
    
    # 初始化聊天历史
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # 🔥 热门问题一键提问
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
    
    # 聊天容器
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # 渲染历史消息
        for message in st.session_state.chat_messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 输入框
    user_input = st.chat_input("输入你想问的关于艾草的问题...")
    
    if user_input:
        # 添加用户消息
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        st.rerun()
    
    # 自动生成AI回复（当最后一条是用户消息时）
    if st.session_state.chat_messages and st.session_state.chat_messages[-1]["role"] == "user":
        # 生成AI回复
        with st.spinner("艾小博正在思考中..."):
            response = call_ai_expert(
                st.session_state.chat_messages,
                DEFAULT_TEMPERATURE
            )
            
            if isinstance(response, str):
                st.error(f"调用失败：{response}")
            else:
                # 流式输出
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
                
                # 最终渲染
                message_placeholder.markdown(f'<div class="assistant-message">{full_response}</div>', unsafe_allow_html=True)
                
                # 添加到历史
                st.session_state.chat_messages.append({"role": "assistant", "content": full_response})
                st.rerun()
