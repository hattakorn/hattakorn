# LINE Sticker Generator (จากภาพตัวอย่าง)

สคริปต์นี้ช่วยสร้าง **สติ๊กเกอร์ไลน์หลายอารมณ์/หลายท่าทาง** จากรูปต้นฉบับ 1 รูป โดยใช้ OpenAI Images API

## ความสามารถ
- อัปโหลดรูปตัวอย่าง 1 รูป (ตัวละครต้นฉบับ)
- ใส่ prompt ได้หลายบรรทัด (แต่ละบรรทัด = 1 สติ๊กเกอร์)
- ระบบจะคงสไตล์ตัวละครเดิม แต่เปลี่ยนท่าทาง/อารมณ์ตาม prompt
- บันทึกเป็นไฟล์ `.png`

## ติดตั้ง
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

ตั้งค่า API Key:
```bash
export OPENAI_API_KEY="<your_api_key>"
```

## วิธีใช้
```bash
python line_sticker_generator.py \
  --reference ./example.png \
  --prompt "ยิ้มดีใจ โบกมือทักทาย" \
  --prompt "งอนเล็กน้อย กอดอก" \
  --prompt "หัวเราะหนักมาก ตาเป็นเส้น" \
  --out-dir ./outputs
```

ผลลัพธ์จะอยู่ในโฟลเดอร์ `outputs/` เช่น
- `sticker_01.png`
- `sticker_02.png`
- `sticker_03.png`

## หมายเหตุ
- แนะนำให้ใช้รูปอ้างอิงที่เห็นตัวละครชัดเจน
- หากอยากให้มีข้อความบนสติ๊กเกอร์ ให้เขียนใน prompt เช่น `พร้อมข้อความว่า "โอเค!"`
- หากต้องการขนาดสติ๊กเกอร์แบบทางการของ LINE สามารถ resize ต่อภายหลังเป็นขนาดที่ต้องการ
