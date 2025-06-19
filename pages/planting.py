import streamlit as st

def show():

    st.title("🌿 General Planting Procedures")
    st.markdown("Select a crop from the dropdown to view step-by-step planting instructions.")

    procedure_info = {
        "Rice": """**Rice Planting Steps:**
1. Choose a high-yielding variety like IR64 or MTU1010.
2. Prepare nursery beds and sow pre-soaked seeds.
3. Transplant 25–30 day-old seedlings with 20x15 cm spacing.
4. Maintain shallow water (2–5 cm) for first 30 days, then 5–10 cm.
5. Apply nitrogen fertilizers in 3 split doses.
6. Harvest when 85% of the grains turn golden yellow.""",

        "Wheat": """**Wheat Planting Steps:**
1. Prepare soil with deep ploughing and harrowing.
2. Use certified seeds and sow in rows 20 cm apart.
3. Apply DAP and urea in 2–3 splits.
4. Weed regularly in the first 40 days.
5. Irrigate at tillering, booting, and grain filling stages.
6. Harvest when grains are hard and straw is yellow.""",

        "Maize": """**Maize Planting Steps:**
1. Select hybrid varieties suited to your region.
2. Sow seeds with spacing 60x20 cm.
3. Apply NPK: 120:60:40 kg/ha.
4. Irrigate during flowering and grain filling.
5. Control stem borers using neem extract or Trichogramma.
6. Harvest when husks dry and kernels are hard.""",

        "Brinjal": """**Brinjal Planting Steps:**
1. Raise seedlings in nursery for 30–35 days.
2. Transplant with 60x60 cm spacing.
3. Apply 25 t/ha FYM and NPK 100:50:50 kg/ha.
4. Stake plants to support growth.
5. Spray neem oil or Bt for pest control.
6. Harvest fruits when tender, shiny, and deep-colored.""",

        "Tomato": """**Tomato Planting Steps:**
1. Sow seeds in trays or nursery beds; transplant at 25 days.
2. Spacing: 60x45 cm.
3. Apply 20 t/ha compost and 100:60:60 NPK kg/ha.
4. Install drip irrigation and mulching film.
5. Stake and prune to improve yield.
6. Harvest red-ripe fruits every 2–3 days.""",

        "Onion": """**Onion Planting Steps:**
1. Raise seedlings and transplant after 6 weeks.
2. Use spacing 10x15 cm.
3. Apply well-rotted FYM and NPK 80:40:40 kg/ha.
4. Irrigate at 7–10 day intervals.
5. Stop watering 10 days before harvest.
6. Harvest when tops dry and fall over.""",

        "Sugarcane": """**Sugarcane Planting Steps:**
1. Select healthy 3-budded setts.
2. Plant in furrows at 90 cm spacing.
3. Apply 25 t/ha FYM and NPK 150:60:60 kg/ha.
4. Use trash mulching to conserve moisture.
5. Control early shoot borer with carbofuran or neem cake.
6. Harvest at 10–12 months when canes mature.""",

        "Groundnut": """**Groundnut Planting Steps:**
1. Use bold-seeded varieties like TG-37A.
2. Sow at 30x10 cm spacing.
3. Apply gypsum at flowering stage.
4. Weed manually after 20 and 40 days.
5. Irrigate during pegging and pod development.
6. Harvest when leaves turn yellow and pods harden.""",

        "Soybean": """**Soybean Planting Steps:**
1. Select early maturing varieties like JS-335.
2. Sow with spacing of 45x5 cm.
3. Apply Rhizobium and PSB culture.
4. Use pre-emergent herbicides to suppress weeds.
5. Irrigate at pod development stage if needed.
6. Harvest when 80% pods turn brown.""",

        "Potato": """**Potato Planting Steps:**
1. Use sprouted, disease-free seed tubers.
2. Sow at 60x20 cm spacing and 5–8 cm depth.
3. Apply NPK 120:60:60 kg/ha and 25 t/ha compost.
4. Earth up after 30 days to cover tubers.
5. Control late blight with mancozeb or copper oxychloride.
6. Harvest when leaves yellow and plants dry.""",

        "Cauliflower": """**Cauliflower Planting Steps:**
1. Transplant 30-day-old seedlings.
2. Use spacing of 45x45 cm.
3. Apply 15 t/ha FYM and 100:50:50 NPK kg/ha.
4. Irrigate weekly during head formation.
5. Protect from aphids using neem-based sprays.
6. Harvest when curds are compact and white.""",

        "Cabbage": """**Cabbage Planting Steps:**
1. Prepare nursery beds and transplant 25–30 day seedlings.
2. Use spacing of 60x45 cm.
3. Apply 20 t/ha FYM and 100:50:50 NPK kg/ha.
4. Mulch and irrigate during head formation.
5. Monitor for diamondback moth and treat early.
6. Harvest when heads are firm and compact.""",

        "Chilli": """**Chilli Planting Steps:**
1. Transplant 40-day-old seedlings.
2. Spacing: 60x45 cm.
3. Apply basal dose of FYM + NPK.
4. Irrigate at flowering and fruiting stages.
5. Control thrips and mites using neem oil.
6. Harvest green chillies at 60 days and red after ripening.""",

        "Peas": """**Peas Planting Steps:**
1. Sow seeds directly in beds at 30x10 cm spacing.
2. Apply compost + basal NPK fertilizer.
3. Stake tall varieties for support.
4. Irrigate lightly during flowering and pod setting.
5. Monitor for powdery mildew.
6. Harvest pods when green and filled.""",

        "Carrot": """**Carrot Planting Steps:**
1. Sow seeds directly in sandy loam soil.
2. Use spacing of 30x10 cm.
3. Apply 20 t/ha FYM and balanced NPK dose.
4. Thin seedlings 2 weeks after germination.
5. Irrigate every 7–10 days.
6. Harvest when roots reach marketable size (2–3 cm diameter)."""
    }


    selected_crop = st.selectbox("🌱 Select a crop to view planting procedure", sorted(procedure_info.keys()))

    if selected_crop:
        st.markdown(procedure_info[selected_crop])
