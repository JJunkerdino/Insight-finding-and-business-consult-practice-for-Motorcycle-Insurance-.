# Motorcycle Insurance Pricing Project

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

## ข้อเสนอแนะเชิงธุรกิจของผมเอง

- หลังจากที่เรารู้ insight แล้วว่า กลุ่มคนอายุต่ำกว่า 25 ปี อยู่ในโซน 2 ขับรถ class 6 ค่อนข้างจะมีอุบัติเหตุบ่อยและเคลมบ่อย ผมเลยอยากลองทำ business recommendation ของตัวเองจากความเข้าใจที่มี
- **แนวทางที่ 1:** เพิ่มค่าเบี้ยประกันที่ลูกค้ากลุ่มนี้ต้องจ่าย เพื่อที่จะได้อยู่ในโปรแกรมความคุ้มครอง (การเคลม) ของกรมธรรม์นี้ต่อไปได้
- **แนวทางที่ 2:** เก็บค่าเบี้ยประกันเท่าเดิม แต่ลดวงเงินความคุ้มครองลง (เคลมได้น้อยลง ถูกลง) ถ้าลูกค้ากลุ่มนี้ไม่ยอมรับเงื่อนไขนี้ ก็ให้เปลี่ยนไปใช้โปรแกรมประกันแบบอื่นแทน
- ผมได้ลองเอาไอเดียแนวทางที่ 2 ไปถามความเห็นกับคนที่ใช้ประกันมอเตอร์ไซค์จริง ๆ ได้ insight กลับมาว่า:
  - จริง ๆ แล้วคนส่วนใหญ่ไม่ได้ซื้อประกันเพราะคาดหวังว่าจะเกิดอุบัติเหตุอยู่แล้ว ดังนั้นถ้าจ่ายเบี้ยประกันเท่าเดิม แต่ได้ค่าเคลมน้อยลง ก็ไม่ได้ติดปัญหาอะไรมากสำหรับพวกเขา — นี่คือหนึ่ง insight ที่ได้มา
  - แต่ลูกค้าก็ยังมีแนวโน้มที่จะไปดูบริษัทประกันเจ้าอื่นว่ามีเงื่อนไขที่ดีกว่าของเราหรือเปล่า ซึ่งอาจเสี่ยงต่อการเสียลูกค้าให้คู่แข่งได้

## My own business recommendation (English)

- After finding the insight that riders under 25 years old, in zone 2, riding class 6 vehicles tend to have accidents and claim fairly often, I wanted to try writing my own business recommendation based on what I understand.
- **Option 1:** Increase the premium these customers have to pay, so they can stay in this policy's coverage/claim program.
- **Option 2:** Keep the premium the same, but reduce the coverage amount (lower claim payout). If this group of customers doesn't accept these terms, let them switch to a different insurance program instead.
- I actually took Option 2 and asked for feedback from a real motorcycle insurance user, and got this insight back:
  - Most people don't actually buy insurance expecting to get into an accident, so if the premium stays the same but the claim payout is reduced, it's not really a big problem for them — that's one insight.
  - But customers would still likely check other insurance companies to see if their terms are better than ours, which could risk losing the customer to a competitor.
