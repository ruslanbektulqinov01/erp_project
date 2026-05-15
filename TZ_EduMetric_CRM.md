# EduMetric CRM — To‘liq Texnik Topshiriq (TZ)

## 1. Loyiha nomi
**EduMetric CRM** — talabaning haqiqiy rivojlanishini ko‘rsatadigan, baho, davomat, xulq-atvor va amaliyot natijalari asosida ishlovchi zamonaviy ta’lim boshqaruv tizimi.

---

## 2. Loyiha maqsadi
EduMetric CRM talabaning “yakuniy bahosi”dan tashqari, **rivojlanish dinamikasini** (progress trajectory) ochib beruvchi yagona platforma bo‘ladi.

Asosiy maqsadlar:
- O‘qituvchi, mentor, dekanat va ota-onaga aniq, real vaqtga yaqin analitika berish.
- Talabaning kuchli va sust tomonlarini erta aniqlash.
- Akademik muvaffaqiyatga ta’sir qiluvchi omillar (davomat, xulq, amaliyot)ni bitta indeksda birlashtirish.
- PDP University va kelajakda respublika miqyosidagi ta’lim tizimiga masshtablanadigan arxitektura yaratish.

---

## 3. Qamrov (Scope)
### 3.1. In-scope
- Talaba profili va akademik kartasi.
- Baho moduli (joriy, oraliq, yakuniy, assignment, quiz).
- Davomat moduli (sababli/sababsiz, kechikish).
- Xulq-atvor moduli (intizom, faollik, jamoaviylik, soft-skills).
- Amaliyot/internship moduli (mentor feedback, KPI, hisobot).
- Progress Analytics (grafiklar, trendlar, risk indikatorlari).
- Role-based access (Admin, O‘qituvchi, Mentor, Dekanat, Talaba, Ota-ona).
- Bildirishnomalar (email/telegram/in-app).
- Audit log va xavfsizlik monitoringi.

### 3.2. Out-of-scope (MVPda emas)
- To‘liq LMS funksionalligi (video dars hosting, SCORM player).
- To‘liq moliya/buxgalteriya moduli.
- Biometrik attendance qurilmalari bilan barcha vendor integratsiyalari.

---

## 4. Manfaatdor tomonlar (Stakeholders)
- Universitet rahbariyati
- Dekanat / Academic Office
- O‘qituvchilar va mentorlar
- Talabalar
- Ota-onalar (agar siyosatda ruxsat etilsa)
- IT administratorlar

---

## 5. Foydalanuvchi rollari va huquqlari
1. **Super Admin**
   - Tizim sozlamalari, rollar, vazn koeffitsiyentlari, barcha ma’lumotlarni boshqarish.
2. **Academic Admin / Dekanat**
   - Guruhlar, fanlar, semestr, o‘quv rejasi, hisobotlar.
3. **O‘qituvchi**
   - Baho kiritish, attendance tasdiqlash, talabaga feedback.
4. **Mentor**
   - Xulq va amaliyot bo‘yicha baholash.
5. **Talaba**
   - O‘z profili, natijalari, trendi, tavsiyalarini ko‘rish.
6. **Ota-ona (optional role)**
   - Faqat farzandi bo‘yicha read-only monitoring.

---

## 6. Funksional talablar

### FR-1: Autentifikatsiya va avtorizatsiya
- Email/telefon + parol orqali login.
- JWT-based sessiya boshqaruvi.
- 2FA (MVP+ bosqichida optional).
- RBAC (Role-Based Access Control).

### FR-2: Talaba profili
- Shaxsiy ma’lumotlar, guruh, fakultet, kurs.
- Akademik tarix (semestrlar kesimida).
- Statuslar: active, suspended, graduated, dropped.

### FR-3: Baho moduli
- Baholar turini moslashuvchan yaratish (quiz, homework, exam, project).
- Har bir baho yozuviga: fan, sana, o‘qituvchi, maksimal ball.
- Qayta topshirish (retake) logikasi.
- Baholarni import (CSV/Excel).

### FR-4: Davomat moduli
- Dars kesimida qatnashdi/qatnashmadi/kechikdi.
- Sababli va sababsiz qoldirish.
- Oylik va semestrlik attendance foizi.
- Past attendance uchun avtomatik ogohlantirish.

### FR-5: Xulq-atvor moduli
- Kriteriyalar: intizom, deadlinega rioya, jamoaviy ishlash, liderlik.
- 5 yoki 10 ballik shkala.
- O‘qituvchi/mentor izohi majburiy maydon (past baholarda).

### FR-6: Amaliyot (Internship/Practicum) moduli
- Kompaniya/loyiha nomi.
- Mentor tomonidan KPI asosida baholash.
- Haftalik progress hisobotlari.
- Yakuniy amaliyot balli va kompetensiyalar xaritasi.

### FR-7: EduMetric Score hisoblash
Umumiy indeks (0-100):

`EduMetric Score = Wg*GradeIndex + Wa*AttendanceIndex + Wb*BehaviorIndex + Wp*PracticeIndex`

Shartlar:
- `Wg + Wa + Wb + Wp = 1.0`
- Default vaznlar (MVP):
  - Grade: 0.45
  - Attendance: 0.20
  - Behavior: 0.15
  - Practice: 0.20
- Vaznlar admin tomonidan sozlanadi.
- Har bir indeks normalizatsiya qilinadi (0–100).

### FR-8: Rivojlanish dinamikasi
- Haftalik/oylik/semestrlik trend grafiklari.
- “Improving / Stable / Declining” status.
- Risk flag (qizil-sariq-yashil) algoritmi.
- Erta ogohlantirish: ketma-ket pasayish holatlari.

### FR-9: Tavsiya (Recommendation Engine)
- Past attendance -> “Davomatni tiklash rejasi”.
- Past grade + yaxshi attendance -> “Akademik qo‘llab-quvvatlash”.
- Past behavior -> mentor suhbat tavsiyasi.
- Tavsiyalarni shablon asosida avtomat chiqarish.

### FR-10: Hisobotlar
- Talaba kesimida to‘liq progress report.
- Guruh/fakultet bo‘yicha kesimlar.
- PDF/Excel eksport.
- Davrlar bo‘yicha solishtirma hisobot.

### FR-11: Bildirishnomalar
- Triggerlar: attendance tushishi, score pasayishi, deadline yaqinlashuvi.
- Kanallar: in-app (MVP), email (MVP+), Telegram bot (Phase-2).
- Notification history log.

### FR-12: Audit va izchillik
- Kim qachon qaysi bahoni o‘zgartirgani log qilinadi.
- Soft-delete va restore.
- Muhim o‘zgarishlar uchun immutable audit table.

---

## 7. Nofunksional talablar (NFR)
- **Ishlash tezligi:** 95% API javoblari < 500ms.
- **Masshtablilik:** 100k+ talaba ma’lumotlarini qo‘llab-quvvatlash.
- **Ishonchlilik:** Uptime 99.5% (oylik).
- **Xavfsizlik:** OWASP Top-10 ga mos choralar.
- **Maxfiylik:** Shaxsiy ma’lumotlarni shifrlash va access policy.
- **Auditability:** Har bir kritik amalda iz qoldirish.
- **Lokalizatsiya:** Uzbek (lotin/kiril), Russian, English qo‘llab-quvvatlash.

---

## 8. Arxitektura talablari
- **Backend:** Django + Django REST Framework.
- **DB:** PostgreSQL (prod), SQLite (dev only).
- **Cache/Queue:** Redis (celery tasks uchun).
- **Frontend:** React/Next.js (yoki mavjud ERP UI bilan integratsiya).
- **Auth:** JWT + refresh token.
- **Storage:** MinIO/S3 (fayl hisobotlar uchun).
- **Deployment:** Docker + CI/CD (GitHub Actions/GitLab CI).

---

## 9. Ma’lumotlar modeli (yuqori daraja)
Asosiy entitylar:
- User
- Role
- StudentProfile
- Group / Faculty / Program
- Course / Subject / Semester
- GradeRecord
- AttendanceRecord
- BehaviorRecord
- PracticeRecord
- EduMetricSnapshot
- Recommendation
- Notification
- AuditLog

Asosiy bog‘lanishlar:
- StudentProfile 1:N GradeRecord
- StudentProfile 1:N AttendanceRecord
- StudentProfile 1:N BehaviorRecord
- StudentProfile 1:N PracticeRecord
- StudentProfile 1:N EduMetricSnapshot

---

## 10. API talablari (namunaviy)
- `POST /api/auth/login`
- `GET /api/students/{id}/profile`
- `GET /api/students/{id}/metrics`
- `POST /api/grades`
- `POST /api/attendance`
- `POST /api/behavior`
- `POST /api/practice`
- `GET /api/reports/student/{id}`
- `GET /api/reports/group/{group_id}`
- `GET /api/alerts`

API standartlari:
- JSON response format bir xil bo‘lishi.
- Pagination, filtering, sorting majburiy.
- OpenAPI/Swagger hujjat avtomatik generatsiya.

---

## 11. Biznes qoidalar
- Attendance < 70% bo‘lsa risk = High.
- Oxirgi 4 haftada EduMetric Score ketma-ket 3 marta tushsa “Declining”.
- Behavior average < 60 bo‘lsa mentor session trigger.
- Practice bahosi kiritilmagan bo‘lsa umumiy indeksda Wp vaqtincha pro-rata qayta taqsimlanadi.

---

## 12. Analitika va dashboard KPI
- O‘rtacha EduMetric Score (fakultet/guruh).
- “High risk” talabalar ulushi.
- Attendance trend.
- Fanlar bo‘yicha muvaffaqiyat koeffitsiyenti.
- Mentor intervention natijasi (before/after).

---

## 13. Integratsiyalar
- ERP/LMS mavjud tizimidan user va course sync.
- HR yoki internship platformadan amaliyot ma’lumotlari import.
- Email/SMS gateway (Phase-2).

---

## 14. Xavfsizlik talablari
- Parollar hash (Argon2/Bcrypt).
- HTTPS-only transport.
- Rate limiting (login endpoint).
- Field-level permissions (talaba boshqasining ma’lumotini ko‘rmasligi).
- PII masking (operator rollarda).

---

## 15. Test strategiyasi
- Unit test: indeks hisoblash, business rule.
- Integration test: API + DB oqimlari.
- Permission test: role-based access.
- Performance test: concurrent API load.
- UAT: dekanat va o‘qituvchi ssenariylari.

Qamrov:
- Backend test coverage kamida 75% (MVP uchun minimal threshold).

---

## 16. Joriy etish bosqichlari (Roadmap)
### Phase 1 (MVP, 8–10 hafta)
- Auth/RBAC
- Student profile
- Grade + Attendance
- EduMetric basic score
- Student-level dashboard

### Phase 2 (6–8 hafta)
- Behavior + Practice modullari
- Tavsiya engine
- Group/faculty analytics
- Email/Telegram alert

### Phase 3 (8+ hafta)
- AI-based predictive risk
- Mobile app
- Regional scaling / multi-campus tenancy

---

## 17. Qabul mezonlari (Acceptance Criteria)
- Talaba bo‘yicha to‘liq score 1 klikda ko‘rinishi.
- O‘qituvchi 1 dars attendance ni <2 daqiqada kiritishi.
- Dekanat risk talabalar ro‘yxatini real vaqtga yaqin olishi.
- Hisobot PDF/Excel eksport xatosiz ishlashi.
- Audit log kritik amallarda 100% to‘liq yozilishi.

---

## 18. Xatarlar va kamaytirish rejasi
- **Data quality riski:** noto‘liq kiritish -> validation + mandatory fields.
- **User adoption riski:** onboarding qiyin -> training + UX soddalashtirish.
- **Integratsiya riski:** legacy API cheklovi -> async sync + retry queue.
- **Maxfiylik riski:** noto‘g‘ri ruxsatlar -> qat’iy permission matrisa + audit.

---

## 19. Yakuniy natija
EduMetric CRM ta’limdagi “raqamli baho jurnali”dan yuqori bosqichga chiqib, talabaning haqiqiy o‘sishini ko‘rsatadigan, data-driven boshqaruv platformasiga aylanadi. Bu tizim universitet darajasida samarali ishlashi va keyinchalik respublika miqyosida joriy etilishi uchun texnik asos beradi.
