import streamlit as st
from PIL import Image
import time
import os

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
</style>
"""
st.markdown(hide_default_style, unsafe_allow_html=True)

# 页面标题
st.title("🌿 艾草科普+小工坊平台")
st.markdown("### 动手学艾草，零消耗练制作")
st.divider()

# ---------------------- 绿色效益计算函数 ----------------------
def calculate_green_benefits(moxa_ratio, years):
    # 行业标准数据：制作1根18*200mm标准艾条需20克艾绒
    fresh_grass = moxa_ratio * 20  # 单位：克
    carbon_reduction = fresh_grass * 0.0002  # 单位：千克
    cost_saving = fresh_grass * 0.01  # 单位：元
    return fresh_grass, carbon_reduction, cost_saving

# ---------------------- 侧边栏导航 ----------------------
with st.sidebar:
    st.header("功能导航")
    page = st.radio(
        "",
        ["🌱 艾草的一生", "🪵 艾条制作工坊", "🎐 香囊制作工坊", "📚 艾草知识库"]
    )
    st.divider()
    st.markdown("人工智能创意作品")

# 终极图片加载函数：完全匹配你现在的图片名字
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
    except:
        return None

# ---------------------- 页面1：艾草的一生 ----------------------
if page == "🌱 艾草的一生":
    st.header("📅 艾草的完整生命周期")
    st.info("拖动滑块查看艾草从播种到应用的全过程")
    
    stage = st.slider("", 1, 6, 1, format="第%d阶段")
    st.progress(stage/6, text=f"生命周期进度：{int(stage/6*100)}%")
    
    stages_data = {
        1: {
            "name": "播种期",
            "time": "每年3-4月",
            "description": "艾草多采用种子繁殖或分株繁殖。种子细小，播种时需与细土混合撒播，覆土1厘米左右，保持土壤湿润。适宜温度15-25℃，播种后7-10天即可发芽。",
            "image": "01_艾草播种种植.jpg"
        },
        2: {
            "name": "发芽期",
            "time": "播种后7-15天",
            "description": "幼苗呈嫩绿色，初期生长缓慢，需注意除草和浇水。当幼苗长到10-15厘米高时，即可进行间苗和移栽。艾草生命力极强，移栽成活率几乎100%。",
            "image": "02_艾草幼苗发芽.jpg"
        },
        3: {
            "name": "生长期",
            "time": "5-7月",
            "description": "这是艾草生长最快的时期，植株高度可达1.5-2米。叶片呈羽状深裂，背面有白色绒毛，有浓郁的香气。此时需充足的阳光和水分，每月施一次有机肥。",
            "image": "03_艾草田生长.jpg"
        },
        4: {
            "name": "收割期",
            "time": "端午节前后",
            "description": "这是一年中收割艾草的最佳时节，此时艾草的药效最强。选择晴天上午收割，割取地上部分，留下根部，秋天还能再收一茬。民间有'端午插艾'的习俗。",
            "image": "04_艾草收割.jpg"
        },
        5: {
            "name": "炮制期",
            "time": "收割后",
            "description": "新鲜艾草不能直接入药，需要经过炮制。先放在通风阴凉处阴干（不能暴晒），然后反复捶打、筛选，去除杂质和茎秆，得到金黄色的艾绒。艾绒陈放3年以上药效最好。",
            "image": "05_艾绒炮制.jpg"
        },
        6: {
            "name": "应用期",
            "time": "全年",
            "description": "艾草是中医里的'万能草'，用途非常广泛：✅ 艾灸：温通经络，散寒止痛 ✅ 泡脚：祛湿驱寒，改善睡眠 ✅ 食疗：艾草青团、艾草鸡蛋汤 ✅ 驱蚊：燃烧艾草，天然驱蚊",
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
    with col2:
        st.subheader(f"第{stage}阶段：{current_stage['name']}")
        st.markdown(f"**⏰ 最佳时间：** {current_stage['time']}")
        st.divider()
        st.markdown(current_stage["description"])

# ---------------------- 页面2：艾条制作工坊 ----------------------
elif page == "🪵 艾条制作工坊":
    st.header("🪵 标准艾条制作虚拟实训")
    st.success("提示：跟着步骤完成制作，最后查看你的绿色环保贡献！")
    
    # 初始化会话状态
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "pound_progress" not in st.session_state:
        st.session_state.pound_progress = 0
    
    # 制作进度条
    st.progress((st.session_state.step-1)/4, text=f"制作进度：{int((st.session_state.step-1)/4*100)}%")
    
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
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

# ---------------------- 页面3：香囊制作工坊 ----------------------
elif page == "🎐 香囊制作工坊":
    st.header("🎐 艾草香囊制作虚拟实训")
    st.info("选择不同的配方，制作属于你的专属艾草香囊！")
    
    formulas = {
        "驱蚊香囊": {
            "ingredients": {"艾草": 30, "薄荷": 10, "金银花": 10, "丁香": 5},
            "effect": "驱蚊防虫，清新空气",
            "suitable": "夏季使用，适合放在卧室、客厅"
        },
        "安神香囊": {
            "ingredients": {"艾草": 20, "薰衣草": 15, "酸枣仁": 10, "合欢花": 5},
            "effect": "宁心安神，改善睡眠",
            "suitable": "失眠多梦人群，适合放在枕头边"
        },
        "健脾香囊": {
            "ingredients": {"艾草": 25, "陈皮": 15, "藿香": 10, "砂仁": 5},
            "effect": "健脾开胃，化湿和中",
            "suitable": "脾胃虚弱、消化不良人群"
        }
    }
    
    formula_name = st.selectbox("选择香囊配方", list(formulas.keys()))
    formula = formulas[formula_name]
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        img = load_image("11_艾草香薰制作.jpg")
        if img:
            st.image(img, use_column_width=True)
        else:
            st.info("图片未找到")
    
    with col2:
        st.subheader(f"{formula_name}配方")
        st.markdown(f"**功效：** {formula['effect']}")
        st.markdown(f"**适用人群：** {formula['suitable']}")
        st.divider()
        
        st.markdown("**药材用量（单位：克）：**")
        for ingredient, amount in formula["ingredients"].items():
            st.slider(ingredient, 0, 50, value=amount, disabled=True)
    
    if st.button("✅ 制作完成", type="primary"):
        st.balloons()
        st.success(f"🎉 你成功制作了一个{formula_name}！")
        
        total_weight = sum(formula["ingredients"].values())
        carbon_reduction = total_weight * 0.0002
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="节省药材总量", value=f"{total_weight}克")
        with col2:
            st.metric(label="减少碳排放", value=f"{carbon_reduction:.3f}千克")

# ---------------------- 页面4：艾草知识库 ----------------------
else:
    st.header("📚 艾草知识库")
    st.markdown("""
    ### 艾草的药用价值
    艾草性味苦、辛、温，归肝、脾、肾经，具有温经止血、散寒止痛、祛湿止痒的功效。
    
    ### 艾草的常见用法
    1. **艾灸**：将艾绒制成艾条或艾柱，点燃后熏烤穴位
    2. **泡脚**：用艾草煮水泡脚，可祛湿驱寒
    3. **食疗**：制作艾草青团、艾草鸡蛋汤等
    4. **香囊**：将艾草装入香囊，可驱蚊安神
    
    ### 注意事项
    - 阴虚血热者慎用
    - 孕妇慎用艾灸
    - 艾灸时注意通风，避免烟雾过浓
    """)