แบบฝึกหัดภาคปฏิบัติรายเรื่อง สอวน. คอมพิวเตอร์ ค่าย 2 — 33 เรื่อง เรียงจากพื้นฐานไปขั้นสูง (แต่ละเรื่องเรียงจากง่ายไปยาก)
============================================================================================

Core  (เนื้อหาหลักของค่าย 2)
  01_Brute_Force_and_Implementation          Brute Force and Implementation
  02_Strings_and_Parsing                     Strings and Parsing
  03_Prefix_Sums_and_Two_Pointers            Prefix Sums and Two Pointers
  04_Binary_Search                           Binary Search
  05_Greedy                                  Greedy
  06_Sorting_and_Sweep_Line                  Sorting and Sweep Line
  07_Number_Theory_and_Counting              Number Theory and Counting
  08_Divide_and_Conquer                      Divide and Conquer
  09_DP_I_Foundations                        DP I: Foundations
  10_DP_II_Classic_Patterns                  DP II: Classic Patterns
  11_DP_III_Faster_Transitions               DP III: Faster Transitions
  12_Graph_Traversal                         Graph Traversal
  13_Shortest_Paths                          Shortest Paths
  14_DSU_and_MST                             DSU and MST

Intermediate  (เนื้อหาเสริมของค่าย 2)
  15_Trees                                   Trees
  16_Monotonic_Stack_and_Queue               Monotonic Stack and Queue
  17_Fenwick_and_Segment_Tree                Fenwick and Segment Tree
  18_Sparse_Table                            Sparse Table
  19_Lazy_Segment_Tree                       Lazy Segment Tree
  20_Tree_DP                                 Tree DP
  21_Rerooting                               Rerooting
  22_Euler_Tour                              Euler Tour
  23_LCA_and_Binary_Lifting                  LCA and Binary Lifting
  24_SCC_Bridges_and_Articulation_Points     SCC, Bridges and Articulation Points
  25_Trie                                    Trie

Advanced (TOI)  (เกินค่าย 2: ระดับ TOI)
  26_Bitmask_and_Digit_DP                    Bitmask and Digit DP

โครงสร้างโฟลเดอร์
  01_Brute_Force_and_Implementation ... 26_Bitmask_and_Digit_DP
      <ชื่อโฟลเดอร์>.pdf   โจทย์ของเรื่อง (หน้าปก + โจทย์ทุกข้อ)
      1.cpp, 2.cpp, ...   ไฟล์คำตอบของแต่ละข้อ (เริ่มต้นเป็นไฟล์ว่าง เขียน code ลงไฟล์เหล่านี้ได้เลย)
  Judge            ตัวตรวจและชุดทดสอบ (ไม่ต้องแก้อะไรในโฟลเดอร์นี้)

ย้ายจากเวอร์ชันเก่า (Topic_1 ... Topic_15): ไฟล์ที่เขียนไว้ย้ายไปอยู่กับโจทย์ของมันในโฟลเดอร์ใหม่ให้เองครั้งเดียว
  ไฟล์ว่างไม่ถูกย้าย ไม่มีไฟล์ใดถูกลบ โฟลเดอร์ Topic_K ที่ยังมีไฟล์ของเราเหลืออยู่จะมี README_MOVED.txt บอกว่าย้ายไปไหน
วิธีตรวจ (ต้องมี Python 3.7+ และ g++) — เลือกวิธีที่สะดวก
  ก) VS Code (ง่ายที่สุด): File > Open Folder... เลือกโฟลเดอร์ C2_Practice (ไม่ใช่ 04_Binary_Search)
     ต้องเป็นโฟลเดอร์ที่มี Judge อยู่ข้างในทันที (ถ้ามี C2_Practice ซ้อนอยู่ใน C2_Practice ให้เลือกอันข้างใน)
     ถ้ากด Ctrl+Shift+B แล้วขึ้นรายการ g++ / gcc ให้เลือกแทนการตรวจ แปลว่าเปิดผิดโฟลเดอร์
     เปิดไฟล์ที่ทำ เช่น 04_Binary_Search/5.cpp แล้วกด Ctrl+Shift+B (Mac: Cmd+Shift+B) = ตรวจข้อนั้น
     ตรวจทั้งเรื่อง: Terminal > Run Task... > Judge whole set
  ข) terminal ในโฟลเดอร์เรื่องที่ทำ (เช่น cd 04_Binary_Search)
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
ถ้าคัดลอกโฟลเดอร์ ชื่อต้องขึ้นต้นด้วยเลขเรื่องสองหลักเหมือนเดิม เช่น 04_Binary_Search (judge ดูเลขเรื่องจากชื่อโฟลเดอร์)
หรือระบุเอง: python3 ../Judge/judge.py 5.cpp 4-5

คะแนน: ข้อละ 100 คิดตามสัดส่วนชุดทดสอบที่ผ่าน · ชุดทดสอบ 5–6 ชุดแรกของแต่ละข้อคือตัวอย่างในโจทย์

การอัปเดต: เมื่อต่ออินเทอร์เน็ต judge จะอัปเดตตัวเองจาก GitHub อัตโนมัติ (ตรวจสอบไม่เกินทุก 10 นาที ไฟล์ .cpp ของคุณ
จะไม่ถูกแก้) บังคับตรวจสอบทันที: python3 ../Judge/judge.py --update  (เลขเวอร์ชันแสดงในกรอบหัวเรื่อง)
