# 📌 PUSH TO GITHUB - SETUP GUIDE

## ❌ MASALAH: Permission Denied

Kode sudah siap untuk push, tapi perlu authentication ke GitHub.

## ✅ SOLUSI: 3 OPSI

### **OPSI 1: PERSONAL ACCESS TOKEN (Recommended)**

1. **Generate Token di GitHub:**
   - Buka https://github.com/settings/tokens
   - Klik "Generate new token"
   - Pilih "Personal access tokens (classic)"
   - Berikan permission: `repo` (full access)
   - Copy token (simpan di tempat aman!)

2. **Setup Git Credential:**
   ```powershell
   git config --global credential.helper manager
   ```

3. **Push ke GitHub:**
   ```powershell
   cd "d:\Kampus ITK\ABD\Tugas Besar - ABD 8 v2"
   git push -u origin main
   ```

4. **Saat diminta username/password:**
   - Username: `RayhanIIqbal13`
   - Password: **PASTE TOKEN YANG SUDAH DI-COPY**

---

### **OPSI 2: SSH KEY (More Secure)**

1. **Generate SSH Key:**
   ```powershell
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   - Tekan Enter untuk default location
   - Tekan Enter untuk skip passphrase (atau set password)

2. **Add SSH Key to GitHub:**
   ```powershell
   # Copy SSH public key
   Get-Content "$HOME\.ssh\id_ed25519.pub" | Set-Clipboard
   ```
   - Buka https://github.com/settings/keys
   - Klik "New SSH key"
   - Paste key
   - Klik "Add SSH key"

3. **Update Remote URL (SSH):**
   ```powershell
   cd "d:\Kampus ITK\ABD\Tugas Besar - ABD 8 v2"
   git remote remove origin
   git remote add origin git@github.com:RayhanIIqbal13/visualisasi-World-Happiness-2015-2024.git
   git push -u origin main
   ```

---

### **OPSI 3: UPDATE REPOSITORY SETTINGS**

1. **Check Repository Permissions:**
   - Buka https://github.com/RayhanIIqbal13/visualisasi-World-Happiness-2015-2024
   - Settings → Collaborators
   - Pastikan akun yang login punya akses

2. **Check Repository Visibility:**
   - Settings → General
   - Pastikan visibility adalah "Public" atau "Private" sesuai keinginan

3. **Re-authenticate GitHub:**
   ```powershell
   # Logout dari Git Credential Manager
   git credential reject
   protocol=https
   host=github.com
   
   # Try push lagi (akan diminta username/password baru)
   git push -u origin main
   ```

---

## 📋 CHECKLIST SEBELUM PUSH

- [ ] Account GitHub login sudah correct
- [ ] Repository URL sudah correct
- [ ] Personal Access Token sudah di-generate (Opsi 1) atau SSH key sudah di-setup (Opsi 2)
- [ ] Credentials sudah di-configure di Git

---

## 🔍 DEBUGGING

### Check Current Configuration:
```powershell
git config --list
git remote -v
```

### Check SSH Connection:
```powershell
ssh -T git@github.com
```

### Test HTTPS Connection:
```powershell
git ls-remote https://github.com/RayhanIIqbal13/visualisasi-World-Happiness-2015-2024.git
```

---

## 📍 SETELAH PUSH BERHASIL

1. **Verify push:**
   ```powershell
   git log --oneline -5
   ```

2. **Check di GitHub:**
   - Buka https://github.com/RayhanIIqbal13/visualisasi-World-Happiness-2015-2024
   - Verify semua files sudah terupload

3. **Next steps untuk Deploy:**
   - Repository sudah ready untuk Streamlit Cloud
   - Bisa langsung ke https://share.streamlit.io untuk deploy

---

## 💡 TIPS

- **Personal Access Token lebih simple** untuk push pertama kali
- **SSH Key lebih secure** untuk jangka panjang
- Kalau error lagi, cek error message di terminal lebih detail
- Butuh help? Lihat GitHub Docs: https://docs.github.com/en/authentication

---

Created: December 7, 2025
