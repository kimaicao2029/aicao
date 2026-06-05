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
            "description": "艾草多采用分株繁殖，成活率几乎100%。种子繁殖虽然慢，但能获得更健壮的植株。",
            "fun_fact": "艾草种子非常小，1克种子就有10000多粒！",
        },
        2: {
            "name": "发芽期",
            "time": "播种后7-15天",
            "ancient_saying": "阳春三月，百草回芽，艾草最先破土。",
            "modern_science": "艾草幼苗含有丰富的叶绿素，光合作用效率是普通植物的1.5倍。",
            "description": "幼苗呈嫩绿色，初期生长缓慢，需注意除草和浇水。",
            "fun_fact": "艾草的根可以深入地下2米，所以它非常耐旱。",
        },
        3: {
            "name": "生长期",
            "time": "5-7月",
            "ancient_saying": "五月艾草，长得比人高。",
            "modern_science": "艾草在25-30℃时生长最快，每天可以长高2-3厘米。",
            "description": "这是艾草生长最快的时期，植株高度可达1.5-2米。",
            "fun_fact": "艾草会释放一种特殊的化学物质，能驱赶周围的害虫。",
        },
        4: {
            "name": "收割期",
            "time": "端午节前后",
            "ancient_saying": "端午采艾，悬于门户，可避邪驱瘟。",
            "modern_science": "端午节前后，艾草的挥发油含量达到全年最高峰，药效最强。",
            "description": "这是一年中收割艾草的最佳时节。选择晴天上午收割。",
            "fun_fact": "早采三天是个宝，晚采三天是个草，说的就是收割时机。",
        },
        5: {
            "name": "炮制期",
            "time": "收割后",
            "ancient_saying": "凡用艾叶，须用陈久者，治令细软，谓之熟艾。",
            "modern_science": "新艾挥发油含量过高，陈艾挥发油适中，火力温和。",
            "description": "新鲜艾草不能直接入药，需要经过炮制，反复捶打筛选。",
            "fun_fact": "制作1公斤30:1的极品艾绒，需要30公斤干艾草。",
        },
        6: {
            "name": "应用期",
            "time": "全年",
            "ancient_saying": "艾草通十二经，走三阴，理气血，逐寒湿。",
            "modern_science": "现代研究证实，艾草含有桉叶素、龙脑等多种活性成分。",
            "description": "艾草是中医里的'万能草'，艾灸、泡脚、香囊、驱蚊都能用。",
            "fun_fact": "艾草是世界上最早被人类使用的药用植物之一，已有5000多年历史。",
        }
    }
    
    current_stage = stages_data[stage]
    
    # 👇 补上了图片占位和所有内容的渲染！
    col_img, col_info = st.columns([1, 1.2])
    
    with col_img:
        # 图片占位，你之后准备好了图片，把这里的链接换成自己的就行
        st.image(
            "https://via.placeholder.com/600x300/e2e8f0/718096?text=图片占位", 
            caption=f"艾草{current_stage['name']}",
            use_column_width=True
        )
    
    with col_info:
        # 显示当前阶段的基本信息
        st.subheader(current_stage['name'])
        st.caption(f"⏰ 时间：{current_stage['time']}")
        
        st.divider()
        
        # 显示古谚语
        st.markdown(f"""
        <div class="info-card ancient-card" style="padding: 15px; margin-bottom: 15px;">
            <h3 style="margin-top: 0; font-size: 16px;">📜 古谚语</h3>
            <p style="margin: 0;">{current_stage['ancient_saying']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 显示现代科学
        st.markdown(f"""
        <div class="info-card modern-card" style="padding: 15px; margin-bottom: 15px;">
            <h3 style="margin-top: 0; font-size: 16px;">🔬 现代科学</h3>
            <p style="margin: 0;">{current_stage['modern_science']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 显示生长描述
        st.markdown(f"""
        <div class="info-card description-card" style="padding: 15px; margin-bottom: 15px;">
            <h3 style="margin-top: 0; font-size: 16px;">📝 生长描述</h3>
            <p style="margin: 0;">{current_stage['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 按钮区域
    col1, col2 = st.columns([1, 1.2])
    with col1:
        if st.button("🥚 发现冷知识", use_container_width=True):
            st.info(f"💡 {current_stage['fun_fact']}")
    
    with col2:
        if st.button("🤖 问艾小博更多", type="primary", use_container_width=True):
            st.session_state.chat_messages = [{"role": "user", "content": f"请详细介绍一下艾草的{current_stage['name']}"}]
            st.session_state.current_page = "ai"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("← 返回首页", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()
