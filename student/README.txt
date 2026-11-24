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
  27_DSU_on_Tree                             DSU on Tree
  28_Heavy_Light_Decomposition               Heavy-Light Decomposition
  29_Centroid_Decomposition                  Centroid Decomposition
  30_Persistent_Segment_Tree                 Persistent Segment Tree
  31_Convex_Hull                             Convex Hull
  32_Convex_Hull_Trick_and_DP_Optimization   Convex Hull Trick and DP Optimization
  33_Mo_Algorithm                            Mo's Algorithm

ชุดฝึกรวม  (โจทย์จากหลายเรื่องปนกัน ไม่บอกว่าข้อใดใช้เรื่องใด: ฝึกอ่านโจทย์แล้วคิดเองว่าควรใช้วิธีใด)
  00_Mixed/M01 ... M11                       ชุดละ 6 ข้อ ตรวจเหมือนโฟลเดอร์เรื่อง (เปิด Problems_M01.pdf ในโฟลเดอร์ 00_Mixed/M01)

โครงสร้างโฟลเดอร์  (หนึ่งข้อ หนึ่งโฟลเดอร์)
  C2_Practice/
    00_Mixed/                              ชุดฝึกรวมทุกชุด (อยู่บนสุด)
      README.txt
      M01/                                 ชุดฝึกรวม: โฟลเดอร์ข้อเป็นเลขหลักเดียว 1 ... 6
        Problems_M01.pdf
        Makefile, judge.bat
        3/
          M01-3.cpp
          3_<ชื่อโจทย์ภาษาอังกฤษ>.pdf
      ...
      M11/
    04_Binary_Search/                      โฟลเดอร์เรื่อง
      Problems_04_Binary_Search.pdf        โจทย์ทั้งเรื่อง (หน้าปก + โจทย์ทุกข้อ)
      Makefile, judge.bat                  ใช้ตรวจทั้งเรื่อง หรือตรวจทีละข้อ (make 5 / judge 5)
      01/
      ...
      05/                                  โฟลเดอร์ของข้อ 5
        04-05.cpp                          ไฟล์คำตอบของข้อนี้ (เรื่อง 04 ข้อ 05) เริ่มต้นเป็นไฟล์ว่าง เขียน code ลงไฟล์นี้ได้เลย
        05_<ชื่อโจทย์ภาษาอังกฤษ>.pdf         โจทย์ของข้อนี้ข้อเดียว (ในโฟลเดอร์ของข้อมีแค่สองไฟล์นี้)
      ...
      20/                                  (บางเรื่องมี 12 หรือ 15 ข้อ)
    Judge/                                 ตัวตรวจและชุดทดสอบ (ไม่ต้องแก้อะไรในโฟลเดอร์นี้)
  ห้ามเปลี่ยนชื่อโฟลเดอร์และชื่อไฟล์ .cpp เพราะ judge รู้ว่าเป็นโจทย์ข้อใดจากชื่อไฟล์ (04-05.cpp) หรือจากโฟลเดอร์ที่ไฟล์อยู่
  (04_Binary_Search/05/) ชื่อไฟล์ .cpp ไม่ซ้ำกันทั้งชุด เปิดหลายข้อพร้อมกันใน editor ก็ไม่สับสน

โฟลเดอร์ old/ (เช่น 04_Binary_Search/old/ มีเฉพาะเมื่อจำเป็น): เมื่ออัปเดตแล้วโจทย์ข้อใดถูกเปลี่ยนเป็นโจทย์ใหม่ code ที่เขียนไว้
  ของโจทย์เดิมจะถูกย้ายมาเก็บที่ <โฟลเดอร์เรื่อง>/old/<ข้อ>_<ชื่อโจทย์เดิม>.cpp ไม่ปนกับโจทย์ใหม่ ส่วนโจทย์ที่ย้ายไปอยู่ข้ออื่น
  ไฟล์ที่เขียนไว้จะย้ายตามโจทย์ไปเอง (ถ้าที่ใหม่มี code อยู่แล้ว ไฟล์ที่ย้ายมาจะไปอยู่ใน old/ แทน)
  judge แจ้งทุกไฟล์ที่ย้าย ไม่มีไฟล์ใดถูกลบหรือถูกเขียนทับ ไฟล์ว่างที่ยังไม่ได้เขียนไม่ถูกย้าย
  ไฟล์ใน old/ เก็บไว้ให้ดูเท่านั้น จะลบทิ้งเองเมื่อไม่ใช้แล้วก็ได้

วิธีตรวจ (ต้องมี Python 3.7+ และ g++) — เลือกวิธีที่สะดวก
  ก) VS Code (ง่ายที่สุด): File > Open Folder... เลือกโฟลเดอร์ C2_Practice (ไม่ใช่ 04_Binary_Search)
     ต้องเป็นโฟลเดอร์ที่มี Judge อยู่ข้างในทันที (ถ้ามี C2_Practice ซ้อนอยู่ใน C2_Practice ให้เลือกอันข้างใน)
     ถ้ากด Ctrl+Shift+B แล้วขึ้นรายการ g++ / gcc ให้เลือกแทนการตรวจ แปลว่าเปิดผิดโฟลเดอร์
     เปิดไฟล์ที่ทำ เช่น 04_Binary_Search/05/04-05.cpp แล้วกด Ctrl+Shift+B (Mac: Cmd+Shift+B) = ตรวจข้อนั้น
     ตรวจทั้งเรื่อง: Terminal > Run Task... > Judge whole topic
  ข) terminal ในโฟลเดอร์เรื่อง (เช่น cd 04_Binary_Search)
       Linux / macOS     make 5        (เฉพาะข้อ 5 พิมพ์ make 05 ก็ได้)   make            (ทั้งเรื่อง)
       Windows           judge 5       (PowerShell: .\judge 5)          judge           (ทั้งเรื่อง)
     หรือดับเบิลคลิก judge.bat ในโฟลเดอร์เรื่องนั้น (Windows) เพื่อตรวจทั้งเรื่อง
     ชุดฝึกรวมใช้แบบเดียวกันในโฟลเดอร์ชุด เช่น cd 00_Mixed/M01 แล้ว make 3 หรือ judge 3
     (ถ้าไม่มีคำสั่ง make: Linux ใช้ sudo apt install make · macOS มากับ xcode-select --install)
     ในโฟลเดอร์ของข้อไม่มี Makefile และ judge.bat จึงสั่ง make หรือ judge ในนั้นไม่ได้ ให้สั่งจากโฟลเดอร์เรื่องตามนี้
     หรือใช้วิธี ก) หรือ ค)
  ค) เรียก judge ตรง ๆ (ทุกระบบ)
       ในโฟลเดอร์ข้อ      python3 ../../Judge/judge.py   (ชุดฝึกรวมลึกกว่าหนึ่งชั้น: ใน 00_Mixed/M01/3 ใช้ ../../../Judge/judge.py)
       ในโฟลเดอร์เรื่อง    python3 ../Judge/judge.py   (ทั้งเรื่อง)   หรือ   python3 ../Judge/judge.py 5   (เฉพาะข้อ 5)
       ในชุดฝึกรวม        python3 ../../Judge/judge.py   (เช่นใน 00_Mixed/M01 ทั้งชุด)   หรือ   python3 ../../Judge/judge.py 3
       จากที่ใดก็ได้       python3 <ที่อยู่ของ C2_Practice>/Judge/judge.py <ไฟล์ .cpp>
     Windows ใช้ python แทน python3
  ไฟล์ที่ compile แล้วอยู่ใน Judge/.build/ ชั่วคราวและถูกลบเมื่อตรวจเสร็จ ไม่มีไฟล์ใดเพิ่มในโฟลเดอร์ของข้อ

macOS (ทำครั้งเดียว)
  - ติดตั้ง compiler + Python:  xcode-select --install
  - g++ บน Mac คือ clang ซึ่งไม่มี <bits/stdc++.h>  judge จัดการให้เองแล้ว (ใช้ Judge/include)
    แต่ถ้าจะ compile เองด้วย g++ หรือใน VS Code ให้ติดตั้ง header นี้ครั้งเดียว (ในโฟลเดอร์ C2_Practice):
      sudo mkdir -p /usr/local/include/bits
      sudo cp Judge/include/bits/stdc++.h /usr/local/include/bits/

ตัวเลือกเพิ่มเติม: --tl 2 (เวลาต่อชุดทดสอบ) --ml 512 (หน่วยความจำ MB, ปกติ 256) --stop (หยุดที่ชุดแรกที่ผิด) --ascii --no-color
ดูรายชื่อโจทย์ทั้งหมด (พร้อมโฟลเดอร์และชื่อไฟล์ของแต่ละข้อ): python3 ../Judge/judge.py --list   (พิมพ์ในโฟลเดอร์เรื่อง)
ถ้าคัดลอกโฟลเดอร์เรื่อง ชื่อต้องขึ้นต้นด้วยเลขเรื่องสองหลักเหมือนเดิม เช่น 04_Binary_Search (judge ดูเลขเรื่องจากชื่อโฟลเดอร์)
ถ้าจะตรวจไฟล์ชื่ออื่นหรือไฟล์ที่อยู่ที่อื่น ให้ระบุข้อเอง: python3 ../../Judge/judge.py my.cpp 4-5   (เรื่อง 4 ข้อ 5 · ชุดฝึกรวม: M01-3)

ความคืบหน้า: ทุกครั้งที่ตรวจ judge บันทึกคะแนนดีที่สุดของแต่ละข้อไว้ใน Judge/progress.json (ได้ 100 ครั้งแรกจะขึ้นว่า First 100 on this problem!)

คะแนน: ข้อละ 100 คิดตามสัดส่วนชุดทดสอบที่ผ่าน · ชุดทดสอบ 5–6 ชุดแรกของแต่ละข้อคือตัวอย่างในโจทย์

Reports to your teacher (Discord) and code copies
  The first time you judge on a computer, the judge asks for the student code your teacher gave you
  (<name>-XXXX; press Enter to skip if you have none yet). In VS Code, click into the terminal panel before typing.
  Then it asks two separate questions:
    1) Send your scores to your teacher? (answer y to get messages in your own Discord channel)
    2) Keep a copy of your code with your teacher? (to move to another computer; n is fine, scores are still sent)
  One login per computer, for both C2_Practice and C2_Mock (file ~/.config/stupidgrader/student.json,
  Windows: %APPDATA%\stupidgrader\student.json).
  What is sent: your student code, the problem, the score, the result of each test (e.g. AAAW), the run number,
  the time, a checksum of your file, and the code of that problem only when code copies are on (64 KB at most).
  Nothing else from your computer.
  It is sent after you see your result (3 seconds at most). Without internet the judge works as usual and sends
  later ("... waiting to be sent to your teacher"). With both turned off, judging works exactly the same.
  Commands (in a topic folder; on Windows type python instead of python3)
    python3 ../Judge/judge.py --report status        who you are logged in as, login file, last send, results waiting
    python3 ../Judge/judge.py --report off           stop sending scores (--report on starts again)
    python3 ../Judge/judge.py --sync off             stop keeping code copies (--sync on starts again)
    python3 ../Judge/judge.py --login <name>-XXXX    log in or change account; --logout logs out (your files stay)
  Moving to a new computer
    a) Online (code copies must have been on): install the package on the new computer, judge any problem and
       enter the same code; the judge offers to copy your code there. Later: python3 ../Judge/judge.py --pull
    b) Offline: on the old computer run python3 ../Judge/judge.py --backup (it makes
       <package>_backup_<date-time>.zip next to the Judge folder), copy the zip to the new computer and run
       python3 ../Judge/judge.py --restore <zip file>
    Neither one overwrites a file that already has code: an empty file gets its code back; if there is other code
    in it, the copy goes to <topic folder>/old/<problem>_cloud_<date>.cpp (from a zip: _backup_), so you can compare
    and choose.
  Shared computer: put your own code on one line in Judge/.student; this package then uses that file instead.

การอัปเดต: เมื่อต่ออินเทอร์เน็ต judge จะอัปเดตตัวเองจาก GitHub อัตโนมัติ (ตรวจสอบไม่เกินทุก 10 นาที ไฟล์ .cpp ของคุณ
จะไม่ถูกแก้ ถ้าโจทย์ถูกย้ายหรือถูกเปลี่ยน ไฟล์ที่เขียนไว้จะย้ายตามที่อธิบายในหัวข้อโฟลเดอร์ old/ ข้างบน)
บังคับตรวจสอบทันที (พิมพ์ในโฟลเดอร์เรื่อง): python3 ../Judge/judge.py --update  (เลขเวอร์ชันแสดงในกรอบหัวเรื่อง)
