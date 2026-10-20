แบบฝึกหัดภาคปฏิบัติรายเรื่อง สอวน. คอมพิวเตอร์ ค่าย 2 — 13 เรื่อง เรื่องละ 20 ข้อ (เรียงจากง่ายไปยาก)
=====================================================================================

เรื่องที่ 1  ผลรวมสะสมและ two pointers    เรื่องที่ 7   graph
เรื่องที่ 2  binary search               เรื่องที่ 8   เส้นทางสั้นที่สุด
เรื่องที่ 3  greedy                      เรื่องที่ 9   DSU และ MST
เรื่องที่ 4  sweep line                  เรื่องที่ 10  tree
เรื่องที่ 5  dynamic programming 1       เรื่องที่ 11  segment tree และ Fenwick tree
เรื่องที่ 6  dynamic programming 2       เรื่องที่ 12  brute force และ implementation
                                         เรื่องที่ 13  divide and conquer
ลำดับที่แนะนำ: 12 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 13 → 8 → 9 → 10 → 11
(หมายเลขเรื่องไม่เปลี่ยน เรื่องที่ 12 และ 13 เพิ่มภายหลังจึงอยู่ท้าย)

โครงสร้างโฟลเดอร์
  Topic_1 ... Topic_13
      Topic_K.pdf   โจทย์เรื่องที่ K (หน้าปก + 20 ข้อ)
      1.cpp ... 20.cpp  ไฟล์คำตอบของแต่ละข้อ (เขียน code ลงไฟล์เหล่านี้ได้เลย)
  Judge            ตัวตรวจและชุดทดสอบ (ไม่ต้องแก้อะไรในโฟลเดอร์นี้)

วิธีตรวจ (ต้องมี Python 3.7+ และ g++) — เลือกวิธีที่สะดวก
  ก) VS Code (ง่ายที่สุด): File > Open Folder... เลือกโฟลเดอร์ C2_Practice (ไม่ใช่ Topic_3)
     ต้องเป็นโฟลเดอร์ที่มี Judge อยู่ข้างในทันที (ถ้ามี C2_Practice ซ้อนอยู่ใน C2_Practice ให้เลือกอันข้างใน)
     ถ้ากด Ctrl+Shift+B แล้วขึ้นรายการ g++ / gcc ให้เลือกแทนการตรวจ แปลว่าเปิดผิดโฟลเดอร์
     เปิดไฟล์ที่ทำ เช่น Topic_3/5.cpp แล้วกด Ctrl+Shift+B (Mac: Cmd+Shift+B) = ตรวจข้อนั้น
     ตรวจทั้งเรื่อง: Terminal > Run Task... > Judge whole set
  ข) terminal ในโฟลเดอร์เรื่องที่ทำ (เช่น cd Topic_3)
       Linux / macOS     make          (ทั้งเรื่อง)   make 5          (เฉพาะข้อ 5)
       Windows           judge         (ทั้งเรื่อง)   judge 5         (PowerShell: .\judge 5)
     หรือดับเบิลคลิก judge.bat ในโฟลเดอร์เรื่องนั้น (Windows) เพื่อตรวจทั้งเรื่อง
     (ถ้าไม่มีคำสั่ง make: Linux ใช้ sudo apt install make · macOS มากับ xcode-select --install)
  ค) เรียก judge ตรง ๆ (ทุกระบบ):  python3 ../Judge/judge.py   หรือ   python3 ../Judge/judge.py 5.cpp
     Windows ใช้ python แทน python3

macOS (ทำครั้งเดียว)
  - ติดตั้ง compiler + Python:  xcode-select --install
  - g++ บน Mac คือ clang ซึ่งไม่มี <bits/stdc++.h>  judge จัดการให้เองแล้ว (ใช้ Judge/include)
    แต่ถ้าจะ compile เองด้วย g++ หรือใน VS Code ให้ติดตั้ง header นี้ครั้งเดียว (ในโฟลเดอร์ C2_Practice):
      sudo mkdir -p /usr/local/include/bits
      sudo cp Judge/include/bits/stdc++.h /usr/local/include/bits/

ตัวเลือกเพิ่มเติม: --tl 2 (เวลาต่อชุดทดสอบ) --ml 512 (หน่วยความจำ MB, ปกติ 256) --stop (หยุดที่ชุดแรกที่ผิด) --ascii --no-color
ดูรายชื่อโจทย์ทั้งหมด: python3 ../Judge/judge.py --list
ถ้าคัดลอกโฟลเดอร์ ให้ตั้งชื่อเป็น Topic_K เสมอ (judge ดูเลขเรื่องจากชื่อโฟลเดอร์) หรือระบุเอง: python3 ../Judge/judge.py 5.cpp 3-5

คะแนน: ข้อละ 100 คิดตามสัดส่วนชุดทดสอบที่ผ่าน · ชุดทดสอบ 5–6 ชุดแรกของแต่ละข้อคือตัวอย่างในโจทย์

การอัปเดต: เมื่อต่ออินเทอร์เน็ต judge จะอัปเดตตัวเองจาก GitHub อัตโนมัติ (ตรวจสอบไม่เกินทุก 10 นาที ไฟล์ .cpp ของคุณ
จะไม่ถูกแก้) บังคับตรวจสอบทันที: python3 ../Judge/judge.py --update  (เลขเวอร์ชันแสดงในกรอบหัวเรื่อง)
