import streamlit as st
from datetime import date

# 页面配置
st.set_page_config(page_title="艾草科普小工坊", page_icon="🌿", layout="wide")

# 初始化状态（刷新页面数据不丢失）
if "study_plans" not in st.session_state:
    st.session_state.study_plans = []
if "approval_records" not in st.session_state:
    st.session_state.approval_records = [
        {"title": "艾条制作基础作业", "status": "已通过", "comment": "卷制均匀紧实，艾绒比例达标，很棒！", "submit_time": "2026-06-03"},
        {"title": "艾草品种识别作业", "status": "待批改", "comment": "老师正在批改中，预计明天出结果", "submit_time": "2026-06-04"}
    ]

# 顶部导航栏
tab1, tab2, tab3 = st.tabs(["🏠 首页", "💬 消息", "👤 我的"])

# ------------------- 首页 -------------------
with tab1:
    st.title("🌿 艾草科普·小工坊平台")
    st.write("让每个人都能轻松学会艾草知识与手工制作")
    
    # 新增：首页视频展示框
    st.video("show.mp4", autoplay=False, format="video/mp4")
    
    st.divider()
    st.subheader("📚 开始学习")
    
    # 底部功能卡片（已删除课程项）
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://via.placeholder.com/300x200?text=艾的一生", use_column_width=True)
        st.button("🌱 艾的一生", use_container_width=True)
    
    with col2:
        st.image("https://via.placeholder.com/300x200?text=艾条制作", use_column_width=True)
        st.button("🔥 艾条制作", use_container_width=True)
    
    with col3:
        st.image("https://via.placeholder.com/300x200?text=香囊DIY", use_column_width=True)
        st.button("🎁 香囊DIY", use_container_width=True)

# ------------------- 消息页（已细化） -------------------
with tab2:
    st.title("💬 我的消息")
    
    st.subheader("📌 学习提醒")
    st.info("你收藏的《艾条制作进阶》已更新第3集")
    st.warning("你的香囊DIY作业还有1天截止提交")
    
    st.subheader("🔔 系统通知")
    st.success("平台艾草养生专题已上线")
    st.info("端午艾草包限时活动即将开始，敬请期待")
    
    st.subheader("💌 互动消息")
    st.write("暂无新的互动消息")

# ------------------- 我的页（已细化） -------------------
with tab3:
    st.title("👤 我的工坊")
    
    # 个人信息
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://via.placeholder.com/100x100?text=头像", width=100)
    with col2:
        st.subheader("艾草新手爱好者")
        st.write("学习进度：3/10 个课程")
        st.progress(30)
    
    st.divider()
    
    # 左右两栏：我的日程 + 我的审批
    col_left, col_right = st.columns(2)
    
    # 可互动：我的日程
    with col_left:
        st.subheader("📅 我的日程")
        st.write("制定你的艾草学习计划")
        
        with st.form("plan_form", clear_on_submit=True):
            plan_date = st.date_input("选择学习日期", value=date.today())
            plan_tasks = st.multiselect(
                "选择学习内容",
                ["认识艾草品种", "艾条制作练习", "香囊DIY", "艾草养生知识", "艾草种植技巧"]
            )
            submit_plan = st.form_submit_button("✅ 确认制定计划", type="primary")
            
            if submit_plan and plan_tasks:
                st.session_state.study_plans.append({
                    "date": plan_date,
                    "tasks": plan_tasks
                })
                st.success("计划制定成功！")
        
        # 显示已制定的计划
        if st.session_state.study_plans:
            st.subheader("📋 我的计划")
            for i, plan in enumerate(st.session_state.study_plans):
                with st.expander(f"{plan['date']} 的学习计划", expanded=False):
                    for task in plan["tasks"]:
                        st.checkbox(task, key=f"task_{i}_{task}")
    
    # 可互动：我的审批
    with col_right:
        st.subheader("✅ 我的作业审批")
        st.write("查看艾草手工作业的反馈")
        
        if st.button("📄 查看全部审批记录", use_container_width=True):
            for record in st.session_state.approval_records:
                with st.expander(f"{record['title']} - {record['submit_time']}", expanded=True):
                    if record["status"] == "已通过":
                        st.success(f"批改状态：{record['status']}")
                    else:
                        st.warning(f"批改状态：{record['status']}")
                    st.write(f"老师评语：{record['comment']}")