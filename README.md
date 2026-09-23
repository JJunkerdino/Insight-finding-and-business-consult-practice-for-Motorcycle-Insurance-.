# Motorcycle Insurance Insight finding and business decision making recommendation practice

## Business Recommendation

### ข้อเสนอแนะเชิงธุรกิจของผมเอง

- หลังจากที่เรารู้ insight แล้วว่า กลุ่มคนอายุต่ำกว่า 25 ปี อยู่ในโซน 2 ขับรถ class 6 ค่อนข้างจะมีอุบัติเหตุบ่อยและเคลมบ่อย ผมเลยอยากลองทำ business recommendation ของตัวเองจากความเข้าใจที่มี
- **แนวทางที่ 1:** เพิ่มค่าเบี้ยประกันที่ลูกค้ากลุ่มนี้ต้องจ่าย เพื่อที่จะได้อยู่ในโปรแกรมความคุ้มครอง (การเคลม) ของกรมธรรม์นี้ต่อไปได้
- **แนวทางที่ 2:** เก็บค่าเบี้ยประกันเท่าเดิม แต่ลดวงเงินความคุ้มครองลง (เคลมได้น้อยลง ถูกลง) ถ้าลูกค้ากลุ่มนี้ไม่ยอมรับเงื่อนไขนี้ ก็ให้เปลี่ยนไปใช้โปรแกรมประกันแบบอื่นแทน
- ผมได้ลองเอาไอเดียแนวทางที่ 2 ไปถามความเห็นกับคนที่ใช้ประกันมอเตอร์ไซค์จริง ๆ ได้ insight กลับมาว่า:
  - จริง ๆ แล้วคนส่วนใหญ่ไม่ได้ซื้อประกันเพราะคาดหวังว่าจะเกิดอุบัติเหตุอยู่แล้ว ดังนั้นถ้าจ่ายเบี้ยประกันเท่าเดิม แต่ได้ค่าเคลมน้อยลง ก็ไม่ได้ติดปัญหาอะไรมากสำหรับพวกเขา — นี่คือหนึ่ง insight ที่ได้มา
  - แต่ลูกค้าก็ยังมีแนวโน้มที่จะไปดูบริษัทประกันเจ้าอื่นว่ามีเงื่อนไขที่ดีกว่าของเราหรือเปล่า ซึ่งอาจเสี่ยงต่อการเสียลูกค้าให้คู่แข่งได้

### My own business recommendation (English)

- After finding the insight that riders under 25 years old, in zone 2, riding class 6 vehicles tend to have accidents and claim fairly often, I wanted to try writing my own business recommendation based on what I understand.
- **Option 1:** Increase the premium these customers have to pay, so they can stay in this policy's coverage/claim program.
- **Option 2:** Keep the premium the same, but reduce the coverage amount (lower claim payout). If this group of customers doesn't accept these terms, let them switch to a different insurance program instead.
- I actually took Option 2 and asked for feedback from a real motorcycle insurance user, and got this insight back:
  - Most people don't actually buy insurance expecting to get into an accident, so if the premium stays the same but the claim payout is reduced, it's not really a big problem for them — that's one insight.
  - But customers would still likely check other insurance companies to see if their terms are better than ours, which could risk losing the customer to a competitor.

### ข้อเสนอแนะจากโมเดล / Recommendations from the model

**ไทย:**
1. **ขึ้นราคากลุ่มเสี่ยงสูงที่ยืนยันแล้ว** — อายุต่ำกว่า 25, โซน 2, class 6 มีข้อมูลจริงพอ (75 policy-years, 8 เคลม) ต้นทุนสูงถึง ~17.7 เท่าของค่าเฉลี่ย ราคาตอนนี้น่าจะต่ำเกินไป ควรขึ้นราคาเฉพาะกลุ่มนี้ โดยอิงจากประวัติเคลมจริง ไม่ใช่แค่ค่าที่โมเดลปรับให้เรียบแล้ว
2. **อย่าใช้ `bonus_class` ตั้งราคาอย่างเดียว** — ไม่มีนัยสำคัญในทั้งสองโมเดลเมื่อคุมอายุ/โซน/คลาสรถแล้ว เก็บไว้เป็นเครื่องมือรักษาลูกค้า (loyalty) ได้ แต่ไม่ใช่ตัวบอกความเสี่ยง
3. **ตั้งเพดานส่วนลด/ส่วนเพิ่มรวม (cap)** — ตารางแบบคูณหลายตัวต่อกัน (ไม่มี interaction) ทำให้ราคาต่างกันเกินจริง (>1,000 เท่า) เมื่อปัจจัยดีหรือแย่มาซ้อนกัน ต้องมี cap ก่อนใช้งานจริง
4. **ระวังโซน 7 และกลุ่มที่ข้อมูลน้อย** — โซน 7 มีเคลมแค่ 1 ครั้ง ยังเชื่อค่า severity ไม่ได้ ควรรวมกับโซนใกล้เคียง หรือใช้ credibility weighting จนกว่าจะมีข้อมูลมากขึ้น

**English:**
1. **Reprice the confirmed high-risk segment** — under 25, zone 2, class 6 is well-observed (75 policy-years, 8 claims) and costs ~17.7x the average. It's very likely under-priced; recommend a targeted rate increase based on real claims history, not just the model's smoothed estimate.
2. **Stop using `bonus_class` as a standalone rating signal** — not significant in either model once age, zone and vehicle class are controlled for. Keep it as a loyalty tool, not a risk indicator.
3. **Cap combined discounts/loadings** — the multiplicative tariff (no interaction terms) can stack factors into unrealistic extremes (>1,000x). Add a maximum combined multiplier before production.
4. **Treat zone 7 and other thin segments with caution** — zone 7 has only 1 claim. Merge it with a similar zone or apply credibility weighting until more data comes in.


## Key Results

**ไทย:** ส่วนนี้สำคัญที่สุด เป็นผลสรุปของทั้งโปรเจกต์ — ตารางราคาเบี้ยประกัน (tariff) ที่ได้จากโมเดล frequency × severity

**English:** This is the most important part — the final pricing output of the whole project, built from the frequency × severity models.

### 1. Tariff table — Top 10 highest base rates

**ไทย:** ตารางราคาจะเห็น top 10 กลุ่มที่มีค่าความเสี่ยงเยอะที่สุด ดูได้เลยว่ากลุ่มไหนเสี่ยง เช่น อายุต่ำกว่า 25 โซน 1 และจะเห็นเลยว่า **vehicle_class 6 ค่อนข้างเยอะ** (ติด 4 อันดับแรกทั้งหมด) ราคานี้คิดที่โปรไฟล์อ้างอิง: bonus_class 1, ผู้หญิง, รถอายุ 0-2 ปี

**English:** The top 10 riskiest groups in the tariff — e.g. under 25 in zone 1 — and **vehicle_class 6 dominates** (all of the top 4). Base rates are priced at a reference profile: bonus_class 1, Female, vehicle age 0-2.

<details>
<summary>Code</summary>

```python
base_bonus = "1"
base_gender = "Female"
base_vehicle_age_group = "0-2"

zones = [str(z) for z in range(1, 8)]
vehicle_classes = [str(c) for c in range(1, 8)]

grid_rows = list(itertools.product(age_labels, zones, vehicle_classes))
tariff = pd.DataFrame(grid_rows, columns=["age_group", "zone", "vehicle_class"])
tariff["bonus_class"] = base_bonus
tariff["gender"] = base_gender
tariff["vehicle_age_group"] = base_vehicle_age_group

tariff["predicted_frequency"] = freq_model.predict(tariff, offset=np.zeros(len(tariff)))
tariff["predicted_severity"] = sev_model.predict(tariff)
tariff["base_pure_premium"] = tariff["predicted_frequency"] * tariff["predicted_severity"]

tariff.sort_values("base_pure_premium", ascending=False).head(10)
```

</details>

| age_group | zone | vehicle_class | predicted_frequency | predicted_severity | base_pure_premium |
|---|---|---|---|---|---|
| <25 | 1 | 6 | 0.2648 | 36,896 | 9,768.7 |
| 25-34 | 1 | 6 | 0.1363 | 64,775 | 8,829.2 |
| <25 | 2 | 6 | 0.1551 | 43,344 | 6,720.8 |
| 25-34 | 2 | 6 | 0.0798 | 76,096 | 6,074.5 |
| <25 | 1 | 7 | 0.1678 | 30,485 | 5,114.8 |
| <25 | 1 | 5 | 0.1681 | 28,701 | 4,824.3 |
| <25 | 1 | 2 | 0.1710 | 28,039 | 4,794.5 |
| 25-34 | 1 | 7 | 0.0864 | 53,520 | 4,622.9 |
| 25-34 | 1 | 5 | 0.0865 | 50,389 | 4,360.4 |
| 25-34 | 1 | 2 | 0.0880 | 49,225 | 4,333.4 |

### 2. Modifier tables (ตัวคูณ)

**ไทย:** อันนี้คือตัวคูณสำหรับ `bonus_class`, `gender` และ `vehicle_age_group` ซึ่งได้จากการคูณความถี่ (frequency) กับความเสียหาย (severity) ออกมาได้ผลแบบนี้ เอาไปคูณกับราคาในตารางข้างบนได้เลย

**English:** Multipliers for `bonus_class`, `gender` and `vehicle_age_group`, from frequency × severity combined. Multiply them onto the base rate above.

$$\text{final price} = \text{base rate} \times \text{bonus modifier} \times \text{gender modifier} \times \text{vehicle age modifier}$$

ตัวอย่าง / Example: อายุ <25, โซน 1, class 6, ผู้ชาย, bonus 1, รถอายุ 3-5 ปี → 9,768.7 × 1.0 × 1.4093 × 0.4436 ≈ **6,107** ต่อปี / per year

<details>
<summary>Code</summary>

```python
def build_modifier_table(factor_col, levels, ref_level):
    rows = pd.DataFrame(
        {
            "age_group": "25-34",
            "zone": "1",
            "vehicle_class": "1",
            "bonus_class": base_bonus,
            "gender": base_gender,
            "vehicle_age_group": base_vehicle_age_group,
        },
        index=levels,
    )
    rows[factor_col] = levels

    freq = freq_model.predict(rows, offset=np.zeros(len(rows)))
    sev = sev_model.predict(rows)
    pure_premium = freq * sev

    return pd.DataFrame(
        {
            "predicted_frequency": freq,
            "predicted_severity": sev,
            "pure_premium": pure_premium,
            "modifier": pure_premium / pure_premium.loc[ref_level],
        }
    )


bonus_table = build_modifier_table("bonus_class", [str(i) for i in range(1, 8)], base_bonus)
gender_table = build_modifier_table("gender", ["Female", "Male"], base_gender)
vehicle_age_table = build_modifier_table("vehicle_age_group", veh_labels, base_vehicle_age_group)
```

</details>

| bonus_class | modifier |
|---|---|
| 1 (reference) | 1.0000 |
| 2 | 1.1037 |
| 3 | 1.5015 |
| 4 | 1.1679 |
| 5 | 1.2680 |
| 6 | 1.7149 |
| 7 | 1.1768 |

| gender | modifier |
|---|---|
| Female (reference) | 1.0000 |
| Male | 1.4093 |

| vehicle_age_group | modifier |
|---|---|
| 0-2 (reference) | 1.0000 |
| 3-5 | 0.4436 |
| 6-9 | 0.2711 |
| 10-14 | 0.0949 |
| 15+ | 0.0524 |



## ทำไมถึงทำโปรเจกต์นี้

- จริง ๆ ที่เลือกทำโปรเจกต์นี้เพราะอยากซ้อมการทำ data analytics และ data science พวกทำโมเดล predict อะไรพวกนี้ โดยเฉพาะเกี่ยวกับพวกประกันภัย (insurance) บ้าง
- เพราะว่าตอนนี้ในชีวิตก็คือกำลังฝึกงานอยู่ แต่ว่าฝึกงานเป็นพวกโรงงาน ก็เลยอยู่แต่กับพวก manufacturing technology แต่ว่าไม่ได้ไปอยู่กับพวก insurance เลย ก็เลยไม่อยากให้ลืม ไม่ได้ไม่เชิงลืม แต่อยากจะฝึกบ้างพวกการหา insight หรือว่าการที่จะ predict ข้อมูล data อะไรก็ตาม
- ความหวังของโปรเจกต์นี้ไม่ได้หวังว่า practice นี้มันจะออกมาดีหรืออะไร แค่อยากลองทำ
- เพราะจริง ๆ แล้วในเมื่อยุคนี้ก็คือ 2026 AI มันสามารถที่จะช่วยเราทุกอย่างได้ ทั้งการเขียน code เขียนโค้ดคือช่วยได้เลย แล้วก็ทุกอย่างที่มันเกี่ยวกับ technical แต่ผมรู้สึกว่า ตั้งแต่ที่ผมได้ฝึกงานมาในพวก manufacturing (อาจจะเป็นทุกบริษัทแหละ) สิ่งที่ AI จะยังช่วยไม่ได้ก็คือการที่เราเข้าใจ process นั้น ๆ ของบริษัทนั้น ๆ
- ขอยกตัวอย่างจากผมเอง: สมมุติว่ามี process 12 อัน แล้วใน 12 อันนั้นต้องผ่านการตรวจตามลำดับ 1 2 3 4 5 6 7 ... จนถึง 12 ซึ่งอันที่ 12 ก็คือ final test แปลว่าอันที่ 1 ถึง 11 คือการตรวจด้วยสายตา แต่ขั้นตอนสุดท้ายคือการตรวจจากข้างใน เราไม่สามารถรู้เลยว่าเขาใช้อะไรตรวจ AI ไม่สามารถรู้ได้
- นั่นทำให้ผมต้องลองไปถามคนที่ทำงานจริงเอง จึงได้รู้ว่า บาง material ที่ไป reject ในขั้นตอนสุดท้ายคือ final test electrical fail มันแปลว่า จาก process 1 ถึง 11 เนี่ย มันไม่สามารถมองได้ด้วยตาเลย ซึ่งข้อมูลแบบนี้เองไม่มีทางรู้ได้ ต้องเป็นคนหาเอง และนั่นคือตัวอย่างของผมว่าทำไมผมถึงมาลองทำ ทั้งที่ AI มันสามารถช่วยเราโค้ดได้ทุกอย่าง (ซึ่งผมก็ใช้ AI จริง ๆ)
- แต่สิ่งหลัก ๆ ที่ผมอยากจะฝึกก็คือ อยากที่จะหา insight เอง โดยการอ่านจากโค้ดที่ AI ส่งมานี่แหละ เราก็แค่ให้เขาช่วย
- และอยากที่จะฝึกเรื่อง storytelling ว่าเราเข้าใจ data มากแค่ไหน และเราจะเอาสิ่งที่เรามีไป translate มันเป็น business decision making ยังไง ให้บริษัทเข้าใจว่ามีอะไรมีปัญหา หรือสามารถ improve ได้ ซึ่งสิ่งนั้นคือสิ่งที่ผมอยากจะฝึก

## Why I made this project (English)

- The real reason I picked this project is because I want to practice data analytics and data science — building models, prediction, that kind of thing — specifically something related to insurance.
- Right now in life I'm doing an internship, but the internship is at a factory, so I'm only around manufacturing technology, not around insurance at all. So I don't want to forget — not really "forget", but I want to keep practicing finding insight and predicting data, whatever that data is.
- The hope for this project isn't that the "practice" turns out great or anything, I just want to try doing it.
- Because honestly, in this era — 2026 — AI can help with everything, including writing code, AI can definitely help with that, and everything technical. But I feel that, ever since I started my internship in manufacturing (maybe it's like this at every company), the thing AI still can't help with is understanding the specific process of that specific company.
- Let me give an example from myself: suppose there are 12 process steps, and within those 12 steps, each one has to pass inspection in order — 1, 2, 3, 4, 5, 6, 7 ... up to 12 — where step 12 is the "final test." That means steps 1 to 11 are visual inspection, but the last step checks something from the inside. We have no way of knowing what they use to test it — AI can't know that either.
- That made me go and ask the people who actually work there myself, and that's how I found out that some materials get rejected at the final step because of a "final test electrical fail" — which means that from process 1 to 11, it's something that simply cannot be seen by eye at all. This kind of insight has no way of being known except by going and finding it out yourself, and that's my example of why I decided to try this, even though AI can help us code everything (which I do use AI for, genuinely).
- But the main thing I want to practice is finding the insight myself, by reading through the code that AI gives me — I just let it help me with that part.
- And I want to practice storytelling — how well do I actually understand the data, and how do I translate what I have into business decision making, so the company understands what the problem is or what can be improved. That's the thing I really want to practice.

---

## 01 — Data Cleaning

### เปลี่ยนชื่อคอลัมน์จากภาษาสวีเดนเป็นภาษาอังกฤษ / Rename Swedish columns to English

**ไทย:** ไฟล์ดิบใช้ชื่อคอลัมน์เป็นตัวย่อภาษาสวีเดน (`agarald`, `kon`, `skadkost`, ...) เลยเปลี่ยนเป็นภาษาอังกฤษให้ใครก็อ่านเข้าใจ ไม่ต้องเปิด data dictionary ดูคู่กัน และเปลี่ยนค่า `gender` จาก M/K เป็น Male/Female (K = Kvinna = ผู้หญิงในภาษาสวีเดน)

**English:** The raw file uses short Swedish codes as column names (`agarald`, `kon`, `skadkost`, ...), so I renamed them to clear English names that anyone can read without the data dictionary open. I also mapped `gender` from M/K to Male/Female (K = Kvinna = woman in Swedish).

```python
rename_map = {
    "rownames": "policy_id",
    "agarald": "owner_age",
    "kon": "gender",
    "zon": "zone",
    "mcklass": "vehicle_class",
    "fordald": "vehicle_age",
    "bonuskl": "bonus_class",
    "duration": "duration_years",
    "antskad": "claim_count",
    "skadkost": "claim_cost",
}

df = df_raw.rename(columns=rename_map)

# M = "Man", K = "Kvinna" (Swedish for woman) -> spell them out for readability
df["gender"] = df["gender"].map({"M": "Male", "K": "Female"})

df.head()
```

Output:

| policy_id | owner_age | gender | zone | vehicle_class | vehicle_age | bonus_class | duration_years | claim_count | claim_cost |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | Male | 1 | 4 | 12 | 1 | 0.175342 | 0 | 0 |
| 2 | 4 | Male | 3 | 6 | 9 | 1 | 0.000000 | 0 | 0 |
| 3 | 5 | Female | 3 | 3 | 18 | 1 | 0.454795 | 0 | 0 |
| 4 | 5 | Female | 4 | 1 | 25 | 1 | 0.172603 | 0 | 0 |
| 5 | 6 | Female | 2 | 1 | 26 | 1 | 0.180822 | 0 | 0 |

### แต่ละคอลัมน์คืออะไร / What each column means

| ชื่อเดิม (สวีเดน) | ชื่อใหม่ | ความหมาย (ไทย) | Meaning (English) |
|---|---|---|---|
| `rownames` | `policy_id` | เลขประจำตัวกรมธรรม์ ใช้แยกแต่ละแถว ไม่มีความหมายทางสถิติ | Policy ID, just separates rows, no statistical meaning |
| `agarald` | `owner_age` | อายุเจ้าของรถ (0-92 ปี) | Owner's age (0-92) |
| `kon` | `gender` | เพศเจ้าของรถ (Male / Female) | Owner's gender (Male / Female) |
| `zon` | `zone` | โซนพื้นที่ (1-7) ตามการแบ่งเขตของสวีเดน | Geographic zone (1-7), Swedish area standard |
| `mcklass` | `vehicle_class` | คลาสความแรงของรถ (1-7) จากกำลังเครื่องเทียบน้ำหนักรถ ยิ่งเลขสูงยิ่งแรง | Vehicle power class (1-7), engine power vs. weight — higher = more powerful |
| `fordald` | `vehicle_age` | อายุตัวรถ (0-99 ปี) | Vehicle age (0-99) |
| `bonuskl` | `bonus_class` | ระดับส่วนลดไม่เคลม (1-7) เริ่มที่ 1 ขับดีไม่เคลมขึ้นทีละระดับ ถ้าเคลมร่วงลง 2 ระดับ | No-claims bonus level (1-7): start at 1, +1 per claim-free year, -2 after a claim |
| `duration` | `duration_years` | ระยะเวลาที่กรมธรรม์คุ้มครองจริง หน่วยเป็นปี (0.5 = 6 เดือน) | Actual coverage time in years (0.5 = 6 months) |
| `antskad` | `claim_count` | จำนวนครั้งที่เคลม (มีแค่ 0, 1, 2) | Number of claims (only 0, 1, 2) |
| `skadkost` | `claim_cost` | ค่าเสียหายรวมที่จ่ายไป (0 ถ้าไม่เคยเคลม) | Total claim cost paid (0 if no claim) |

---

## 02 — Exploratory Data Analysis (EDA)

### 1. Top 10 riskiest combinations (Combined risk ranking)

**คำอธิบายของผม:** ตารางนี้คือการ rank ว่า combination ไหน (อายุ × โซน × คลาสรถ) มีการเคลมเยอะที่สุด และมีค่าเบี้ยประกัน (pure premium) สูงที่สุด แล้วเรียงออกมาเป็น top 10 combination

**คำอธิบายจากโค้ด:** เอา 3 ปัจจัยที่แรงที่สุด (กลุ่มอายุ × โซน × คลาสรถ) มารวมกัน แล้วคำนวณ pure premium (ต้นทุนความเสี่ยงต่อปี) ของแต่ละชุด โดยกรองเอาเฉพาะชุดที่มีข้อมูลมากพอ (exposure ≥ 50 policy-years) เพื่อไม่ให้อันดับถูกกำหนดโดยกรมธรรม์แค่ 2-3 อันที่บังเอิญโชคร้าย ชุดที่เสี่ยงที่สุดคือ **อายุต่ำกว่า 25 + โซน 2 + คลาสรถ 6** มี pure premium สูงถึง **17.7 เท่า** ของค่าเฉลี่ยรวม

**English:** This ranks every age group × zone × vehicle class combination by pure premium (expected cost per policy-year), and shows the top 10. Only combinations with at least 50 policy-years of exposure are kept, so the ranking isn't driven by a couple of unlucky policies. The riskiest is **age under 25 + zone 2 + vehicle class 6**, at **17.7x** the overall average.

```python
combo = df_exp.groupby(["age_group", "zone", "vehicle_class"], observed=True).agg(
    exposure=("duration_years", "sum"),
    claims=("claim_count", "sum"),
    total_cost=("claim_cost", "sum"),
)
combo = combo[combo["exposure"] >= 50]  # keep only groups with enough data to trust
combo["frequency"] = combo["claims"] / combo["exposure"]
combo["pure_premium"] = combo["total_cost"] / combo["exposure"]

print(f"Groups with at least 50 policy-years of exposure: {len(combo)}")
print(f"Overall pure premium for comparison: {overall_pure_premium:,.1f}")
print("\nTop 10 riskiest combinations (highest pure premium):")
combo.sort_values("pure_premium", ascending=False).head(10)
```

Output:

```text
Groups with at least 50 policy-years of exposure: 154
Overall pure premium for comparison: 259.7
```

| age_group | zone | vehicle_class | exposure | claims | total_cost | frequency | pure_premium |
|---|---|---|---|---|---|---|---|
| <25 | 2 | 6 | 75.1 | 8 | 345,595 | 0.1065 | 4,601 |
| 25-34 | 1 | 6 | 183.1 | 21 | 788,104 | 0.1147 | 4,305 |
| <25 | 1 | 4 | 61.2 | 7 | 235,049 | 0.1143 | 3,838 |
| <25 | 1 | 3 | 121.9 | 14 | 256,551 | 0.1148 | 2,104 |
| 25-34 | 1 | 3 | 509.7 | 27 | 969,440 | 0.0530 | 1,902 |
| 25-34 | 1 | 5 | 345.6 | 18 | 631,411 | 0.0521 | 1,827 |
| <25 | 3 | 5 | 161.6 | 8 | 289,385 | 0.0495 | 1,790 |
| <25 | 2 | 4 | 122.4 | 6 | 217,576 | 0.0490 | 1,777 |
| 25-34 | 1 | 4 | 352.9 | 14 | 620,906 | 0.0397 | 1,760 |
| 25-34 | 3 | 2 | 82.0 | 4 | 133,435 | 0.0488 | 1,628 |

### 2. แบ่งกลุ่มอายุ / Build readable groups

**ไทย:** แบ่งอายุคนขับ (`owner_age`) และอายุรถ (`vehicle_age`) ออกเป็นช่วง ๆ เพื่อให้เปรียบเทียบแต่ละกลุ่มได้ง่ายขึ้น

**English:** Bucket owner age and vehicle age into groups so segments are easier to compare.

```python
age_bins = [0, 25, 35, 45, 55, 65, 100]
age_labels = ["<25", "25-34", "35-44", "45-54", "55-64", "65+"]
df_exp["age_group"] = pd.cut(df_exp["owner_age"], bins=age_bins, labels=age_labels, right=False)

veh_bins = [0, 3, 6, 10, 15, 100]
veh_labels = ["0-2", "3-5", "6-9", "10-14", "15+"]
df_exp["vehicle_age_group"] = pd.cut(df_exp["vehicle_age"], bins=veh_bins, labels=veh_labels, right=False)

df_exp[["owner_age", "age_group", "vehicle_age", "vehicle_age_group"]].head()
```

Output:

| | owner_age | age_group | vehicle_age | vehicle_age_group |
|---|---|---|---|---|
| 0 | 0 | <25 | 12 | 10-14 |
| 2 | 5 | <25 | 18 | 15+ |
| 3 | 5 | <25 | 25 | 15+ |
| 4 | 6 | <25 | 26 | 15+ |
| 5 | 9 | <25 | 8 | 6-9 |

### 3. "ปี" ในที่นี้คืออะไร / What is a "policy-year"?

```text
Total exposure (policy-years): 65,236.8
Total claims: 693
Overall claim frequency: 0.0106 claims per policy-year
Overall average severity (cost per claim): 24,446
Overall pure premium (cost per policy-year): 259.7
```

**ไทย:** คำว่า **policy-year (ปีกรมธรรม์)** ไม่ใช่ปีปฏิทิน แต่คือ "ระยะเวลาที่กรมธรรม์คุ้มครองจริง" รวมกันทั้งหมด

- กรมธรรม์ 1 อัน คุ้มครองเต็มปี = 1 policy-year
- กรมธรรม์ 1 อัน คุ้มครอง 6 เดือน = 0.5 policy-year
- เอา `duration_years` ของทุกกรมธรรม์มาบวกกัน → total exposure = 65,236.8 policy-years

ตัวอย่าง: กรมธรรม์ 3 อัน คุ้มครอง 1 ปี, 0.5 ปี, 0.3 ปี → รวมเป็น 1.8 policy-years ตัวเลขนี้ใช้เป็นตัวหารตอนคำนวณ "อัตราการเคลมต่อปี" (frequency) เพื่อให้เทียบกันได้ยุติธรรม ไม่ว่ากรมธรรม์แต่ละอันจะคุ้มครองนานแค่ไหน

**English:** A **policy-year** is not a calendar year — it's the total time policies were actually covered. One policy covered for a full year = 1 policy-year; covered for 6 months = 0.5. Adding up `duration_years` of every policy gives 65,236.8 policy-years. Example: 3 policies covered for 1, 0.5 and 0.3 years = 1.8 policy-years. This is the denominator for claim frequency, so policies with different coverage lengths can be compared fairly.

### 4. Claim frequency by segment (อัตราการเคลมต่อปี)

![Claim frequency by segment](Motorcycle%20Insurance/reports/figures/frequency_by_segment.png)

**ไทย:** กราฟ 6 อันคือ "อัตราการเคลมต่อปี" (แกน y) แยกตามแต่ละปัจจัย เส้นแดงคือค่าเฉลี่ยรวม (0.0106) ไว้ดูว่าแท่งไหนสูงหรือต่ำกว่าค่าเฉลี่ย สิ่งที่เจอคือ **อายุ (โดยเฉพาะต่ำกว่า 25) และโซน 1** ทำให้อัตราเคลมสูงกว่าค่าเฉลี่ยชัดเจนที่สุด

**English:** Claims per policy-year (y-axis) for each factor; the red line is the overall average (0.0106). **Age (especially under 25) and zone 1** push claim frequency above average the most.

### 5. Total claims by segment (จำนวนเคลมรวม)

![Total claims by segment](Motorcycle%20Insurance/reports/figures/total_claims_by_segment.png)

**ไทย:** กราฟชุดนี้ใช้ **จำนวนเคลมรวมจริง ๆ** (ไม่หารด้วย exposure) เรียงจากมากไปน้อย เส้นแดงคือค่าเฉลี่ยของแท่งในกราฟนั้น

- **age_group:** กราฟ frequency บอกว่า `<25` เสี่ยงสุด แต่กราฟนี้ `25-34` มีเคลมรวมมากที่สุด เพราะกลุ่ม `25-34` มีจำนวนกรมธรรม์เยอะกว่ามาก ถึงเคลมต่อปีจะน้อยกว่า แต่พอคนเยอะ ผลรวมเลยมากกว่า
- **bonus_class:** class 7 มีเคลมรวมมากที่สุด ทั้งที่ frequency ไม่ได้สูงสุด เพราะคนสะสมอยู่ใน class 7 เยอะที่สุด

กราฟนี้ตอบคำถาม **"เคลมส่วนใหญ่มาจากกลุ่มไหน"** (ใช้วางแผนจัดการเคลม) ส่วนกราฟ frequency ตอบ **"กลุ่มไหนเสี่ยงต่อกรมธรรม์ 1 อันมากที่สุด"** (ใช้ตั้งราคา) — สองคำถามนี้คำตอบไม่จำเป็นต้องตรงกัน

**English:** Raw total claim counts (not divided by exposure), sorted high to low; the red line is the average bar in each chart. `25-34` has the most total claims (not `<25`) simply because it has far more policies, and `bonus_class 7` leads because most long-tenured riders sit there. This chart answers **"where do most claims come from"** (operations), while the frequency chart answers **"which group is riskiest per policy"** (pricing).

### 6. Claim severity by segment (ค่าเสียหายต่อการเคลม)

![Claim severity by segment](Motorcycle%20Insurance/reports/figures/severity_by_segment.png)

**ไทย:** กราฟชุดนี้เปลี่ยนจาก "เคลมบ่อยแค่ไหน" เป็น **"เคลมแต่ละครั้งแพงแค่ไหน"** (แกน y = ค่าเสียหายเฉลี่ยต่อครั้ง) ใช้เฉพาะกรมธรรม์ที่เคยเคลมจริง (693 ครั้ง) รูปแบบไม่เหมือนกราฟความถี่ เช่น **อายุ 25-44 มีค่าเสียหายเฉลี่ยสูงสุด** ทั้งที่อายุต่ำกว่า 25 เคลม*บ่อย*กว่า — นี่คือเหตุผลที่ต้องแยกโมเดล "ความถี่" กับ "ความรุนแรง" ออกจากกัน

**English:** Average cost per claim (only the 693 real claims). The pattern differs from frequency — **ages 25-44 have the highest average severity** even though under-25s claim more *often*. That's why frequency and severity need separate models.

**เช็คจำนวนเคลมของแต่ละโซน / Sample size check by zone:**

| zone | n_claims | total_cost | avg_severity |
|---|---|---|---|
| 1 | 182 | 5,513,403 | 30,293 |
| 2 | 166 | 4,779,266 | 28,791 |
| 3 | 122 | 2,509,647 | 20,571 |
| 4 | 195 | 3,745,300 | 19,207 |
| 5 | 9 | 104,739 | 11,638 |
| 6 | 18 | 288,045 | 16,003 |
| 7 | 1 | 650 | 650 |

**ไทย:** โซน 5, 6, 7 มีเคลมน้อยมาก (โซน 7 มีแค่ **1 ครั้ง**) ค่าเฉลี่ยของโซนพวกนี้เลยยังเชื่อถือไม่ได้

**English:** Zones 5, 6 and 7 have very few claims (zone 7 has only **1**), so their average severity isn't reliable.

**การกระจายตัวของค่าเสียหาย / Distribution of claim cost:**

![Claim cost distribution](Motorcycle%20Insurance/reports/figures/claim_cost_distribution.png)

```text
Top 1% most expensive claims (6 claims) = 8.3% of total claim cost
Largest single claim: 365,347
Median claim: 8,920
```

**ไทย:** ฮิสโตแกรมซ้ายเป็นสเกลปกติ ขวาเป็นสเกล log ข้อมูล **เบ้ขวาชัดเจน** คือเคลมส่วนใหญ่มูลค่าน้อย มีส่วนน้อยที่แพงมาก — ค่ามัธยฐาน 8,920 แต่ค่าเฉลี่ย 24,446 (ถูกดึงขึ้นโดยเคลมแพง ๆ ไม่กี่ครั้ง) และเคลมที่แพงที่สุด 1% (6 ครั้ง) คิดเป็น 8.3% ของค่าเสียหายทั้งหมด

**English:** Left = normal scale, right = log scale. Claim cost is **strongly right-skewed**: median 8,920 vs mean 24,446, and the top 1% of claims (6 claims) make up 8.3% of total cost.

### EDA summary / สรุป EDA

**ไทย:**
- **ค่าพื้นฐาน:** อัตราเคลม 0.0106 ครั้งต่อ policy-year, ค่าเสียหายเฉลี่ย 24,446 ต่อครั้ง, pure premium ~260 ต่อ policy-year
- **อายุคือตัวแปรที่แรงที่สุด:** อายุต่ำกว่า 25 เคลม 0.035 ต่อปี (มากกว่า 3 เท่าของค่าเฉลี่ย) ลดลงเรื่อย ๆ จนเหลือ 0.003 ที่อายุ 65+
- **โซนมีผลมาก:** โซน 1 (0.029) เสี่ยงกว่าโซน 7 (0.004) ประมาณ 7 เท่า
- **คลาสรถ:** class 6-7 (แรงสุด) อัตราเคลม 0.018-0.019 ประมาณ 2 เท่าของ class 1, 3, 4
- **รถใหม่เคลมบ่อยกว่า:** อายุรถ 0-2 ปี (0.021) เทียบกับ 15+ ปี (0.004)
- **เพศ:** ผู้ชาย (0.0108) เคลมบ่อยกว่าผู้หญิง (0.0086) เล็กน้อย
- **bonus_class ใช้บอกความเสี่ยงคนเดียวไม่ได้:** class 4 เคลมบ่อยที่สุด (0.014) และอายุเฉลี่ยเพิ่มตาม class (39.9 → 45.7) แปลว่ามันสะท้อนประสบการณ์ขับมากกว่า
- **ค่าเสียหายไม่ได้ไปทางเดียวกับความถี่:** อายุ 25-44 ค่าเสียหายเฉลี่ยสูงสุด (~30,000) ส่วนต่ำกว่า 25 แค่ ~19,000
- **กลุ่มเสี่ยงที่สุด:** อายุต่ำกว่า 25, โซน 2, class 6 (~4,601 ต่อปี = 17.7 เท่า) อันดับ 2 คือ 25-34, โซน 1, class 6 (~16.6 เท่า)

**English:**
- **Baseline:** frequency 0.0106 claims per policy-year, severity 24,446 per claim, pure premium ~260 per policy-year.
- **Age is the strongest driver:** under 25 claims at 0.035/year (over 3x average), falling to 0.003 for 65+.
- **Zone matters a lot:** zone 1 (0.029) is ~7x riskier than zone 7 (0.004).
- **Vehicle class:** classes 6-7 run at 0.018-0.019, about double classes 1, 3 and 4.
- **Newer bikes claim more:** 0.021 for 0-2 years vs 0.004 for 15+ years.
- **Gender:** males (0.0108) claim slightly more than females (0.0086).
- **Bonus class is not a clean risk signal on its own:** class 4 is the highest (0.014), and average age rises with bonus class (39.9 → 45.7), so it mostly reflects experience.
- **Severity doesn't follow frequency:** ages 25-44 have the highest severity (~30,000) vs ~19,000 for under 25.
- **Riskiest segment:** age under 25, zone 2, class 6 (~4,601/year = 17.7x average); 2nd is 25-34, zone 1, class 6 (~16.6x).

---

## 03 — Frequency & Severity GLM (Model)

### 1. Frequency model (Poisson GLM) — เคลมบ่อยแค่ไหน

**ไทย:** โมเดลนี้ทำนายว่า **กรมธรรม์แต่ละแบบจะเคลมบ่อยแค่ไหนต่อปี** จากปัจจัยเสี่ยง (อายุ, โซน, คลาสรถ, bonus class, เพศ, อายุรถ) โดยใส่ `duration_years` เป็น offset เพื่อบอกโมเดลว่ากรมธรรม์ที่คุ้มครองครึ่งปีควรเคลมประมาณครึ่งหนึ่งของกรมธรรม์เต็มปี ก่อน fit เช็คก่อนว่าใช้ Poisson ได้ไหม (variance / mean ใกล้ 1 = ใช้ได้)

**English:** Predicts **how often each type of policy claims per year** from the rating factors, with `log(duration_years)` as an offset (a half-year policy should expect about half the claims of a full-year one). First check that Poisson fits: variance / mean close to 1 means no overdispersion.

```text
Mean of claim_count: 0.01109
Variance of claim_count: 0.01183
Variance / Mean ratio: 1.067 (close to 1.0 -> Poisson is fine; much higher -> use Negative Binomial)
```

```python
rating_factors = ["age_group", "zone", "vehicle_class", "bonus_class", "gender", "vehicle_age_group"]
freq_formula = "claim_count ~ " + " + ".join(f"C({col})" for col in rating_factors)

freq_model = smf.glm(
    formula=freq_formula,
    data=df_exp,
    family=sm.families.Poisson(),
    offset=np.log(df_exp["duration_years"]),
).fit()

print(freq_model.summary())
```

Output:

```text
                 Generalized Linear Model Regression Results                  
==============================================================================
Dep. Variable:            claim_count   No. Observations:                62474
Model:                            GLM   Df Residuals:                    62445
Model Family:                 Poisson   Df Model:                           28
Link Function:                    Log   Scale:                          1.0000
Method:                          IRLS   Log-Likelihood:                -3543.2
Deviance:                      5737.9   Pearson chi2:                 1.12e+05
No. Iterations:                     8   Pseudo R-squ. (CS):            0.01446
=================================================================================================
                                    coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------------------
Intercept                        -2.6688      0.232    -11.507      0.000      -3.123      -2.214
C(age_group)[T.35-44]            -1.0303      0.125     -8.249      0.000      -1.275      -0.786
C(age_group)[T.45-54]            -1.2414      0.110    -11.324      0.000      -1.456      -1.027
C(age_group)[T.55-64]            -1.1276      0.152     -7.440      0.000      -1.425      -0.831
C(age_group)[T.65+]              -1.6507      0.415     -3.975      0.000      -2.465      -0.837
C(age_group)[T.<25]               0.6639      0.111      6.006      0.000       0.447       0.881
C(zone)[T.2]                     -0.5351      0.108     -4.944      0.000      -0.747      -0.323
C(zone)[T.3]                     -1.0226      0.119     -8.626      0.000      -1.255      -0.790
C(zone)[T.4]                     -1.4698      0.106    -13.928      0.000      -1.677      -1.263
C(zone)[T.5]                     -1.6808      0.342     -4.912      0.000      -2.352      -1.010
C(zone)[T.6]                     -1.3605      0.249     -5.473      0.000      -1.848      -0.873
C(zone)[T.7]                     -1.8392      1.003     -1.833      0.067      -3.805       0.127
C(vehicle_class)[T.2]             0.2388      0.200      1.193      0.233      -0.154       0.631
C(vehicle_class)[T.3]            -0.2991      0.170     -1.762      0.078      -0.632       0.034
C(vehicle_class)[T.4]            -0.1848      0.181     -1.019      0.308      -0.540       0.171
C(vehicle_class)[T.5]             0.2216      0.172      1.287      0.198      -0.116       0.559
C(vehicle_class)[T.6]             0.6760      0.172      3.919      0.000       0.338       1.014
C(vehicle_class)[T.7]             0.2198      0.437      0.503      0.615      -0.637       1.077
C(bonus_class)[T.2]              -0.0061      0.147     -0.041      0.967      -0.294       0.282
C(bonus_class)[T.3]               0.0711      0.159      0.446      0.655      -0.241       0.383
C(bonus_class)[T.4]               0.3007      0.155      1.944      0.052      -0.002       0.604
C(bonus_class)[T.5]               0.0864      0.176      0.491      0.623      -0.258       0.431
C(bonus_class)[T.6]               0.0064      0.183      0.035      0.972      -0.352       0.365
C(bonus_class)[T.7]               0.2435      0.118      2.058      0.040       0.012       0.475
C(gender)[T.Male]                 0.3093      0.135      2.287      0.022       0.044       0.574
C(vehicle_age_group)[T.10-14]    -0.9423      0.114     -8.278      0.000      -1.165      -0.719
C(vehicle_age_group)[T.15+]      -1.5185      0.124    -12.199      0.000      -1.762      -1.275
C(vehicle_age_group)[T.3-5]      -0.4666      0.116     -4.025      0.000      -0.694      -0.239
C(vehicle_age_group)[T.6-9]      -0.7534      0.119     -6.334      0.000      -0.986      -0.520
=================================================================================================
```

> ### วิธีดู: ถ้า `coef` เป็นบวก = ปัจจัยนั้นมีความเสี่ยงมาก → แล้วไปดู `P>|z|` ถ้าน้อยกว่า 0.05 แปลว่าค่านั้นเป็นของจริง ไม่ใช่ความบังเอิญจากการสุ่ม
>
> ### How to read: positive `coef` = higher risk → then check `P>|z|`: below 0.05 means the effect is real, not random chance.

**คอลัมน์อื่น ๆ (จากโค้ด):**
- `std err` = ความคลาดเคลื่อนของ `coef` ยิ่งน้อยยิ่งมั่นใจ (เช่น `zone 7` มีเคลมน้อย ค่านี้เลยสูงถึง 1.003)
- `[0.025, 0.975]` = ช่วงความเชื่อมั่น 95% ถ้าช่วงนี้คร่อมเลข 0 (มีทั้งบวกและลบ) แปลว่าปัจจัยนั้นยังไม่มีผลชัดเจน
- ตัวอย่างจริง: `C(vehicle_class)[T.6]` coef = +0.676, P = 0.000 → รถ class 6 เพิ่มความเสี่ยงเคลมจริง ตรงกับ EDA

**Other columns (from the code):** `std err` = uncertainty of `coef` (smaller = more confident; `zone 7` is 1.003 because it has very few claims). `[0.025, 0.975]` = 95% confidence interval — if it crosses 0, the effect isn't clear. Real example: `vehicle_class 6` has coef +0.676 with P = 0.000 → a real risk increase, matching the EDA.

### 2. Relativities (frequency) — แปลง coef ให้อ่านง่าย

> ### อันนี้คือโมเดลเดิมจากข้อที่แล้ว แต่เอามาใส่ exponential (`exp`) ให้อ่านง่ายขึ้น: ถ้า `relativity` สูง แปลว่ามีความเสี่ยง → พอเจอตัวที่เสี่ยงแล้วให้ไปดู p-value ถ้าน้อยกว่า 0.05 คอลัมน์ `significant_at_5pct` จะขึ้นว่า `True` แปลว่าค่านี้เป็นของจริง
>
> ### Same model as above, with `exp()` applied so it's easier to read: high `relativity` = risky → then check the p-value: below 0.05 shows `True` in `significant_at_5pct`, meaning it's real.

**วิธีอ่านตัวเลข / Reading the number:** `1.97` = เคลมมากกว่ากลุ่มอ้างอิง 1.97 เท่า (claims 1.97x more than the reference group), `0.57` = เหลือแค่ 0.57 เท่า (43% less), `1.0` = ไม่ต่างกัน (no difference). กลุ่มอ้างอิง / reference groups: age `25-34`, zone `1`, vehicle_class `1`, bonus_class `1`, `Female`, vehicle age `0-2`.

```python
def relativities_table(model):
    out = pd.DataFrame({
        "relativity": np.exp(model.params),
        "p_value": model.pvalues,
    })
    out = out.drop("Intercept")
    out["significant_at_5pct"] = out["p_value"] < 0.05
    return out.sort_values("relativity", ascending=False)


freq_relativities = relativities_table(freq_model)
freq_relativities
```

Output:

| factor | relativity | p_value | significant_at_5pct |
|---|---|---|---|
| C(vehicle_class)[T.6] | 1.9659 | 0.0001 | True |
| C(age_group)[T.<25] | 1.9424 | 0.0000 | True |
| C(gender)[T.Male] | 1.3624 | 0.0222 | True |
| C(bonus_class)[T.4] | 1.3508 | 0.0519 | False |
| C(bonus_class)[T.7] | 1.2757 | 0.0396 | True |
| C(vehicle_class)[T.2] | 1.2697 | 0.2330 | False |
| C(vehicle_class)[T.5] | 1.2481 | 0.1981 | False |
| C(vehicle_class)[T.7] | 1.2458 | 0.6151 | False |
| C(bonus_class)[T.5] | 1.0902 | 0.6233 | False |
| C(bonus_class)[T.3] | 1.0737 | 0.6553 | False |
| C(bonus_class)[T.6] | 1.0064 | 0.9720 | False |
| C(bonus_class)[T.2] | 0.9939 | 0.9670 | False |
| C(vehicle_class)[T.4] | 0.8313 | 0.3083 | False |
| C(vehicle_class)[T.3] | 0.7415 | 0.0781 | False |
| C(vehicle_age_group)[T.3-5] | 0.6271 | 0.0001 | True |
| C(zone)[T.2] | 0.5856 | 0.0000 | True |
| C(vehicle_age_group)[T.6-9] | 0.4708 | 0.0000 | True |
| C(vehicle_age_group)[T.10-14] | 0.3897 | 0.0000 | True |
| C(zone)[T.3] | 0.3596 | 0.0000 | True |
| C(age_group)[T.35-44] | 0.3569 | 0.0000 | True |
| C(age_group)[T.55-64] | 0.3238 | 0.0000 | True |
| C(age_group)[T.45-54] | 0.2890 | 0.0000 | True |
| C(zone)[T.6] | 0.2565 | 0.0000 | True |
| C(zone)[T.4] | 0.2300 | 0.0000 | True |
| C(vehicle_age_group)[T.15+] | 0.2190 | 0.0000 | True |
| C(age_group)[T.65+] | 0.1919 | 0.0001 | True |
| C(zone)[T.5] | 0.1862 | 0.0000 | True |
| C(zone)[T.7] | 0.1590 | 0.0667 | False |

**ไทย (จากโค้ด):**
- `vehicle_class 6` (1.97 เท่า) และ `age <25` (1.94 เท่า) คือ 2 ตัวที่เสี่ยงที่สุดและมั่นใจที่สุด ตรงกับ EDA
- `zone` และ `vehicle_age_group` ลดลงเป็นขั้น ๆ ชัดเจน ยิ่งห่างจากโซน 1 / รถใหม่ ยิ่งเสี่ยงน้อยลง
- `bonus_class` ส่วนใหญ่ **ไม่มีนัยสำคัญ** เมื่อคุมอายุ/โซน/รถแล้ว ส่วน `bonus_class 7` (1.28 เท่า, p = 0.04) อาจเป็นความบังเอิญจากการทดสอบหลายตัวพร้อมกัน (~28 ตัว) ไม่ควรตีความว่า "class 7 เสี่ยงกว่า"

**English (from the code):**
- `vehicle_class 6` (1.97x) and `age <25` (1.94x) are the strongest, most confident risk multipliers — both match the EDA.
- `zone` and `vehicle_age_group` decrease cleanly and significantly away from zone 1 / newest bikes.
- `bonus_class` is mostly **not significant**. `bonus_class 7` (1.28x, p = 0.04) is likely multiple-testing noise (~28 coefficients tested), not "class 7 riders are riskier."

### 3. Severity model (Gamma GLM) — เคลมแต่ละครั้งแพงแค่ไหน

**ไทย:** โมเดลนี้ถาม **"ถ้าเคลมเกิดขึ้นแล้ว จะเสียหายเท่าไหร่"** เลยใช้แค่ข้อมูลที่เคยเคลมจริง (693 ครั้ง) ที่ใช้ Gamma ไม่ใช่ Poisson เพราะค่าเสียหายเป็น "จำนวนเงิน" ที่เบ้ขวา ไม่ใช่ "จำนวนครั้ง"

**English:** Asks **"given a claim happens, how expensive is it?"**, so only the 693 real claims are used. Gamma (not Poisson) because claim cost is a right-skewed money amount, not a count.

```python
claims_only = df_exp[df_exp["claim_count"] > 0].copy()

# 27 policies have 2 claims recorded as one combined claim_cost -> use average cost per claim as the target
claims_only["avg_claim_cost"] = claims_only["claim_cost"] / claims_only["claim_count"]

sev_formula = "avg_claim_cost ~ " + " + ".join(f"C({col})" for col in rating_factors)

sev_model = smf.glm(
    formula=sev_formula,
    data=claims_only,
    family=sm.families.Gamma(link=sm.families.links.Log()),
    var_weights=claims_only["claim_count"],  # policies with 2 claims carry more weight in the average
).fit()

print(f"Number of claims used: {int(claims_only['claim_count'].sum())}")
print(sev_model.summary())
```

Output:

```text
Number of claims used: 693
                 Generalized Linear Model Regression Results                  
==============================================================================
Dep. Variable:         avg_claim_cost   No. Observations:                  666
Model:                            GLM   Df Residuals:                      637
Model Family:                   Gamma   Df Model:                           28
Link Function:                    Log   Scale:                          1.4239
Method:                          IRLS   Log-Likelihood:                -7208.1
Deviance:                      1061.5   Pearson chi2:                     907.
No. Iterations:                    29   Pseudo R-squ. (CS):             0.2841
=================================================================================================
                                    coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------------------
Intercept                        10.5038      0.280     37.461      0.000       9.954      11.053
C(age_group)[T.35-44]             0.1943      0.154      1.258      0.208      -0.108       0.497
C(age_group)[T.45-54]            -0.4539      0.135     -3.354      0.001      -0.719      -0.189
C(age_group)[T.55-64]            -0.7644      0.183     -4.185      0.000      -1.122      -0.406
C(age_group)[T.65+]              -1.0049      0.504     -1.995      0.046      -1.992      -0.018
C(age_group)[T.<25]              -0.5628      0.131     -4.309      0.000      -0.819      -0.307
C(zone)[T.2]                      0.1611      0.133      1.215      0.224      -0.099       0.421
C(zone)[T.3]                     -0.2795      0.143     -1.956      0.051      -0.560       0.001
C(zone)[T.4]                     -0.2562      0.129     -1.980      0.048      -0.510      -0.003
C(zone)[T.5]                     -0.2846      0.417     -0.683      0.494      -1.101       0.532
C(zone)[T.6]                     -0.4727      0.306     -1.546      0.122      -1.072       0.127
C(zone)[T.7]                     -3.9320      1.205     -3.264      0.001      -6.293      -1.571
C(vehicle_class)[T.2]             0.3004      0.241      1.248      0.212      -0.171       0.772
C(vehicle_class)[T.3]             0.4061      0.204      1.995      0.046       0.007       0.805
C(vehicle_class)[T.4]             0.1841      0.218      0.845      0.398      -0.243       0.611
C(vehicle_class)[T.5]             0.3238      0.206      1.574      0.116      -0.080       0.727
C(vehicle_class)[T.6]             0.5749      0.205      2.807      0.005       0.174       0.976
C(vehicle_class)[T.7]             0.3841      0.537      0.715      0.475      -0.669       1.437
C(bonus_class)[T.2]               0.1048      0.178      0.588      0.556      -0.244       0.454
C(bonus_class)[T.3]               0.3353      0.193      1.736      0.083      -0.043       0.714
C(bonus_class)[T.4]              -0.1455      0.188     -0.772      0.440      -0.515       0.224
C(bonus_class)[T.5]               0.1511      0.215      0.704      0.482      -0.270       0.572
C(bonus_class)[T.6]               0.5330      0.223      2.385      0.017       0.095       0.971
C(bonus_class)[T.7]              -0.0807      0.144     -0.561      0.575      -0.363       0.201
C(gender)[T.Male]                 0.0338      0.164      0.206      0.837      -0.288       0.356
C(vehicle_age_group)[T.10-14]    -1.4131      0.139    -10.200      0.000      -1.685      -1.142
C(vehicle_age_group)[T.15+]      -1.4299      0.152     -9.401      0.000      -1.728      -1.132
C(vehicle_age_group)[T.3-5]      -0.3463      0.140     -2.469      0.014      -0.621      -0.071
C(vehicle_age_group)[T.6-9]      -0.5521      0.144     -3.826      0.000      -0.835      -0.269
=================================================================================================
```

> ### วิธีดูเหมือน frequency model เลย: `coef` เป็นบวก = ค่าเสียหายต่อครั้งสูงขึ้น → ดู `P>|z|` ถ้าน้อยกว่า 0.05 = ของจริง
>
> ### Read it exactly like the frequency model: positive `coef` = more expensive per claim → `P>|z|` below 0.05 = real.

### 4. Relativities (severity)

> ### อ่านเหมือน relativity ของ frequency: `relativity` สูง = เสี่ยง (แพงกว่าต่อครั้ง) → `significant_at_5pct` เป็น `True` = ของจริง
>
> ### Same as frequency relativities: high `relativity` = more expensive per claim → `True` in `significant_at_5pct` = real.

```python
sev_relativities = relativities_table(sev_model)
sev_relativities
```

Output:

| factor | relativity | p_value | significant_at_5pct |
|---|---|---|---|
| C(vehicle_class)[T.6] | 1.7770 | 0.0050 | True |
| C(bonus_class)[T.6] | 1.7040 | 0.0171 | True |
| C(vehicle_class)[T.3] | 1.5009 | 0.0460 | True |
| C(vehicle_class)[T.7] | 1.4682 | 0.4746 | False |
| C(bonus_class)[T.3] | 1.3984 | 0.0826 | False |
| C(vehicle_class)[T.5] | 1.3823 | 0.1156 | False |
| C(vehicle_class)[T.2] | 1.3504 | 0.2119 | False |
| C(age_group)[T.35-44] | 1.2145 | 0.2084 | False |
| C(vehicle_class)[T.4] | 1.2022 | 0.3981 | False |
| C(zone)[T.2] | 1.1748 | 0.2243 | False |
| C(bonus_class)[T.5] | 1.1631 | 0.4817 | False |
| C(bonus_class)[T.2] | 1.1104 | 0.5565 | False |
| C(gender)[T.Male] | 1.0344 | 0.8370 | False |
| C(bonus_class)[T.7] | 0.9225 | 0.5747 | False |
| C(bonus_class)[T.4] | 0.8646 | 0.4401 | False |
| C(zone)[T.4] | 0.7740 | 0.0477 | True |
| C(zone)[T.3] | 0.7562 | 0.0505 | False |
| C(zone)[T.5] | 0.7523 | 0.4945 | False |
| C(vehicle_age_group)[T.3-5] | 0.7073 | 0.0135 | True |
| C(age_group)[T.45-54] | 0.6352 | 0.0008 | True |
| C(zone)[T.6] | 0.6233 | 0.1221 | False |
| C(vehicle_age_group)[T.6-9] | 0.5758 | 0.0001 | True |
| C(age_group)[T.<25] | 0.5696 | 0.0000 | True |
| C(age_group)[T.55-64] | 0.4656 | 0.0000 | True |
| C(age_group)[T.65+] | 0.3661 | 0.0460 | True |
| C(vehicle_age_group)[T.10-14] | 0.2434 | 0.0000 | True |
| C(vehicle_age_group)[T.15+] | 0.2393 | 0.0000 | True |
| C(zone)[T.7] | 0.0196 | 0.0011 | True |

**ไทย (จากโค้ด):**
- `vehicle_class 6` = 1.78 เท่า แปลว่ารถ class 6 ถ้าเคลม จะเสียหายแพงกว่ากลุ่มอ้างอิง 1.78 เท่า
- `age <25` = 0.57 เท่า คือค่าเสียหาย *ต่ำกว่า* ทั้งที่เคลมบ่อยที่สุด — เด็กวัยรุ่นชนบ่อยแต่ชนแต่ละครั้งเสียหายน้อยกว่า
- `vehicle_age_group` ลดลงชัดเจน รถเก่าซ่อม/เปลี่ยนถูกกว่า
- **`zone 7` = 0.02 เท่า ห้ามเชื่อ** เพราะทั้งข้อมูลมีเคลมโซน 7 แค่ 1 ครั้ง (650)
- `bonus_class` บางตัวดูมีนัยสำคัญ (เช่น class 6 = 1.70 เท่า) แต่ต้องระวังเรื่องความบังเอิญจากการทดสอบหลายตัวเหมือนเดิม

**English (from the code):**
- `vehicle_class 6` = 1.78x: class 6 claims cost 1.78x more than the reference.
- `age <25` = 0.57x: *lower* severity despite the highest frequency — young riders crash more often but cheaper each time.
- `vehicle_age_group` decreases cleanly — older bikes cost less to repair.
- **`zone 7` = 0.02x — do not trust it**: zone 7 has exactly 1 claim (650) in the whole dataset.
- Some `bonus_class` levels look significant (e.g. class 6 = 1.70x) — same multiple-testing caution applies.

> ## BIG INSIGHT
>
> **ไทย:** จากที่เช็คมา ปัจจัยที่เสี่ยงจริง ๆ และเห็นได้ชัดมี 2 ตัว คือ **vehicle_class 6** และ **คนที่อายุต่ำกว่า 25 ปี** — แต่ **vehicle_class 6 เสี่ยงทั้งความถี่ในการเกิดเคลม (1.97 เท่า) และค่าเสียหายต่อการเคลม (1.78 เท่า) เลย**
>
> **English:** The two clearly risky factors are **vehicle_class 6** and **riders under 25** — but **vehicle_class 6 is risky on BOTH claim frequency (1.97x) AND claim cost (1.78x).**

### 5. Combine: คำนวณเบี้ยประกัน / Calculate the premium

**ไทย:** ต่อไปเราจะมาคำนวณเบี้ยประกัน (pure premium) กัน แล้วเทียบว่าที่เราทำนายไว้กับของจริงต่างกันเท่าไหร่ ตามสูตร:

**English:** Now calculate the premium (pure premium) and compare what we predicted against what actually happened, using:

$$\text{pure premium} = \text{frequency} \times \text{severity}$$

```python
# offset=0 -> predicted rate per 1 policy-year (not scaled by each row's actual duration)
predicted_frequency = freq_model.predict(df_exp, offset=np.zeros(len(df_exp)))
predicted_severity = sev_model.predict(df_exp)

df_exp["predicted_pure_premium"] = predicted_frequency * predicted_severity
df_exp["predicted_cost"] = df_exp["predicted_pure_premium"] * df_exp["duration_years"]

total_predicted = df_exp["predicted_cost"].sum()
total_actual = df_exp["claim_cost"].sum()

print(f"Total actual claim cost: {total_actual:,.0f}")
print(f"Total predicted claim cost: {total_predicted:,.0f}")
print(f"Ratio (predicted / actual): {total_predicted / total_actual:.3f}")
```

Output:

```text
Total actual claim cost: 16,941,050
Total predicted claim cost: 17,471,471
Ratio (predicted / actual): 1.031
```

**ไทย:** ค่าที่ทำนายกับของจริงห่างกันแค่ 3.1% (`ratio = 1.031`) ถือว่าแม่นมาก พร้อมเอาไปตั้งราคาต่อ

**English:** Predicted vs actual total cost is only 3.1% apart (`ratio = 1.031`) — accurate enough to use for pricing.

**แยกตามกลุ่มอายุ / By age group:**

![Actual vs predicted pure premium by age group](Motorcycle%20Insurance/reports/figures/actual_vs_predicted_by_age.png)

| age_group | exposure | actual_cost | predicted_cost | actual_pure_premium | predicted_pure_premium |
|---|---|---|---|---|---|
| <25 | 4,520.9 | 3,032,472 | 2,744,845 | 670.8 | 607.2 |
| 25-34 | 10,153.6 | 7,185,533 | 7,585,366 | 707.7 | 747.1 |
| 35-44 | 13,988.9 | 2,804,155 | 3,419,818 | 200.5 | 244.5 |
| 45-54 | 25,240.3 | 3,017,945 | 2,831,810 | 119.6 | 112.2 |
| 55-64 | 9,379.0 | 810,456 | 826,094 | 86.4 | 88.1 |
| 65+ | 1,954.2 | 90,489 | 63,538 | 46.3 | 32.5 |

**ไทย:** จะเห็นว่าคนที่อายุต่ำกว่า 25 ค่าจริง (670.8) **มากกว่า** ที่เราทำนายไว้ (607.2) แปลว่ากลุ่มนี้มีค่าเคลมจริงเยอะกว่าที่เราคาดไว้

**English:** For riders under 25, the actual pure premium (670.8) is **higher** than predicted (607.2) — this group really claims more than the model expected.

### 6. Price the riskiest segment from the EDA

**ไทย:** เอามาดูเลยว่ากลุ่มไหนเสี่ยงที่สุด — กลุ่มที่เสี่ยงที่สุดคือ **คนที่อายุต่ำกว่า 25 ปี อยู่โซน 2 และขับรถ class 6**

**English:** Look directly at the riskiest group — **riders under 25, in zone 2, on class 6 bikes**.

```python
overall_pure_premium = total_actual / df_exp["duration_years"].sum()

riskiest_segment = df_exp[
    (df_exp["age_group"] == "<25") & (df_exp["zone"] == "2") & (df_exp["vehicle_class"] == "6")
]

exposure = riskiest_segment["duration_years"].sum()
actual_pure_premium = riskiest_segment["claim_cost"].sum() / exposure
predicted_pure_premium = riskiest_segment["predicted_cost"].sum() / exposure

print(f"Riskiest segment: age <25, zone 2, vehicle_class 6 ({len(riskiest_segment)} policies, {exposure:.1f} policy-years)")
print(f"Actual pure premium:    {actual_pure_premium:,.0f} per policy-year")
print(f"Model's predicted pure premium: {predicted_pure_premium:,.0f} per policy-year")
print(f"Overall average pure premium for comparison: {overall_pure_premium:,.0f}")
print(f"Model says this segment is {predicted_pure_premium / overall_pure_premium:.1f}x the average risk")
```

Output:

```text
Riskiest segment: age <25, zone 2, vehicle_class 6 (132 policies, 75.1 policy-years)
Actual pure premium:    4,601 per policy-year
Model's predicted pure premium: 2,594 per policy-year
Overall average pure premium for comparison: 260
Model says this segment is 10.0x the average risk
```

**ไทย (จากโค้ด):** ของจริงคือ 4,601 ต่อปี (17.7 เท่า) แต่โมเดลทำนายแค่ 2,594 (10.0 เท่า) ไม่ใช่ bug — กลุ่มนี้มีข้อมูลแค่ 75 policy-years ค่าเฉลี่ยจริงเลยแกว่งได้ง่าย โมเดล GLM เลย "ยืมข้อมูล" จากภาพรวมทั้งหมดมาช่วยปรับให้เรียบขึ้น แต่ถ้ากลุ่มนี้เสี่ยงกว่าที่โมเดลคิดจริง ๆ 2,594 ก็จะต่ำเกินไป ขั้นต่อไปที่น่าลองคือเพิ่ม interaction term หรือใช้ credibility weighting

**English (from the code):** Actual is 4,601/year (17.7x), but the model predicts 2,594 (10.0x). Not a bug — with only 75 policy-years, the raw average is noisy, so the GLM "borrows strength" from the whole dataset. But if this group really is worse than the model assumes, 2,594 is an underestimate. A next step would be an interaction term or credibility weighting.

### GLM summary / สรุปโมเดล

**ไทย:**
- **เลือกโมเดล:** variance / mean = 1.07 → ใช้ Poisson ได้ (ไม่ต้อง Negative Binomial) และใช้ Gamma สำหรับค่าเสียหาย
- **ความแม่น:** ทำนายรวม 17,471,471 เทียบของจริง 16,941,050 ห่างกันแค่ 3.1%
- **ปัจจัยที่เชื่อถือได้:** `vehicle_class 6` (ความถี่ 1.97 เท่า + ค่าเสียหาย 1.78 เท่า), `age <25` (ความถี่ 1.94 เท่า แต่ค่าเสียหาย 0.57 เท่า), `zone` และ `vehicle_age_group`
- **ต้องระวัง:** `bonus_class` ส่วนใหญ่ไม่มีนัยสำคัญ และ `zone 7` มาจากเคลมแค่ 1 ครั้ง

**English:**
- **Model choice:** variance / mean = 1.07 → plain Poisson is fine; Gamma for severity.
- **Calibration:** predicted 17,471,471 vs actual 16,941,050 — within 3.1%.
- **Reliable factors:** `vehicle_class 6` (1.97x frequency + 1.78x severity), `age <25` (1.94x frequency but 0.57x severity), `zone` and `vehicle_age_group`.
- **Be careful with:** `bonus_class` (mostly not significant) and `zone 7` (based on 1 claim).

---

## 04 — Tariff Table & Recommendation

**ไทย:** ตารางราคา (tariff) และตัวคูณ (modifier) อยู่ใน [Key Results](#key-results) ด้านบน ส่วนข้อเสนอแนะอยู่ใน [Business Recommendation](#business-recommendation)

**English:** The tariff table and modifier tables are in [Key Results](#key-results) at the top, and the recommendations are in [Business Recommendation](#business-recommendation).
