# Kurulum (mentor için, yaklaşık 15 dakika)

Bunu öğrenenin bilgisayarına sistemi kuran kişi yapar. Öğrenen için rehber [BASLA.md](BASLA.md) dosyasında.

## 1. Gerekenler

- [ ] **VS Code** (1.94 veya üstü).
- [ ] **Claude Code eklentisi** (Anthropic). Kurulduktan sonra öğrenenin Claude hesabıyla giriş yapılır. **Ücretli plan gerekir** (Pro veya üstü). Ücretsiz planda Claude Code yok.
- [ ] **Sadece Windows'ta: Git for Windows** (https://git-scm.com/download/win). Claude Code komutları Windows'ta Git Bash ile çalıştırır. Git kurulu değilse sistemin script'leri çalışmaz.

## 2. Repoyu indir

```bash
git clone https://github.com/GDenizKaratas/teach-anything.git
```

Git kullanmıyorsan GitHub'dan "Download ZIP" ile indirip klasörü açabilirsin.

## 3. Mentor notunu ekle

`learner/intake.md` dosyası git'e girmez (kişisel bilgi), bu yüzden klonda olmaz. Ya hazırladığın dosyayı kopyala, ya da `learner/intake.example.md` dosyasını `learner/intake.md` adıyla kopyalayıp doldur.

## 4. Python'u kur (uv ile)

Terminalde:

| macOS / Linux | Windows (PowerShell) |
|---|---|
| `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |

Sonra **VS Code'u kapatıp yeniden aç**, klasörde bir terminal aç (``Ctrl+` ``) ve şunu çalıştır:

```bash
uv sync
```

Bu komut `.venv/` klasörünü Python ve pytest ile oluşturur. Bu adım atlanırsa sistem çalışmaz: tekrar planlaması, notlama ve kod koruması Python'a bağlı.

## 5. VS Code'da aç

- [ ] File → Open Folder → `teach-anything`.
- [ ] "Do you trust the authors?" sorusuna **Yes**.
- [ ] Sağ altta önerilen eklentiler (Python, Mermaid) çıkarsa **Install**.
- [ ] Komut paleti (Mac: `Cmd+Shift+P`, Windows: `Ctrl+Shift+P`) → "Python: Select Interpreter" → `.venv` içindekini seç.

## 6. Kontrol et

Claude panelinde **yeni bir sohbet** aç ve yaz: **"kurulum kontrolü yap"**.

- [ ] Claude `tools/doctor` çalıştırır: uv, `.venv` ve pytest ✓ görünmeli.
- [ ] Claude, oturum başında gelen durum bilgisinden bahseder ("profil henüz yok, mentor notu var" gibi). Bahsetmiyorsa hook çalışmıyor demektir. Windows'ta önce Git for Windows'u kontrol et.
- [ ] Bu kontrol sohbetini kapat. Öğrenen kendi yeni sohbetiyle başlasın.

## 7. İlk oturum

İlk 10 dakika yanında ol. Öğrenen yeni bir sohbet açıp **"Merhaba"** yazar. Onboarding, mentor notunu doğrulatır ve ilk adımı attırır. Bir izin penceresi çıkarsa bu klasördeki işler için "Allow" demesini göster.

## İlerlemenin yedeği (isteğe bağlı)

Öğrenenin verileri (`learner/`, `tracks/`, `workspace/`) sadece onun bilgisayarında durur ve git'e girmez. Yedek istersen klasörü ara ara kopyala. Ya da öğrenen için özel (private) bir repo açıp `.gitignore` dosyasındaki ilgili satırları kaldır.
