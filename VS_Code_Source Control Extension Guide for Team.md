# 🚀 VS Code Source Control (Git & GitHub) — Team SOP & Beginner Guide

> **Important Team Rule:** `main` branch **protected** hai! Koi bhi person directly `main` branch par code push nahi kar sakta. Sabhi ko apni **feature branch** banani hogi, kaam commit & push karke **Pull Request (PR)** raise karni hogi review ke liye.

---

## 🧭 1. VS Code Source Control Kahan Milega?

* Left sidebar par **Source Control** icon (3 connected dots / branch icon) par click karo.
* **Shortcut:** `Ctrl + Shift + G` (Windows/Linux) ya `Cmd + Shift + G` (Mac).
* **Bottom-Left Status Bar:** Yahan hamesha dikhega ki aap currently kis branch par ho (e.g., `main`, `feature/login`).

---

## 🔁 Standard Daily Workflow (End-to-End)

Follow this sequence for every new task:

```
1. Switch to 'main' & Pull latest code
   ⬇️
2. Create your own task branch
   ⬇️
3. Code changes karo (Test your work)
   ⬇️
4. Stage & Commit
   ⬇️
5. Pull (Rebase) if main is ahead
   ⬇️
6. Publish / Push Branch
   ⬇️
7. Create Pull Request (PR) on GitHub
```

---

## Step 1: Branch Check & Latest Code Lena

Naya kaam shuru karne se pehle ensure karo ki aap updated `main` par base kar rahe ho:

1. Bottom-left status bar me branch name par click karo.
2. List me se **`main`** select karo (branch switch ho jayegi).
3. Source Control panel me upar `...` (Three dots) > **Pull** par click karo.
   *(Ab aapke system par latest production/team code aa gaya).*

---

## Step 2: Apni Feature Branch Banao

Hamesha task ke hisaab se nayi branch banao:

1. Bottom-left me `main` par click karo.
2. Select: **Create new branch...** (ya *Create branch from...* > select `main`).
3. **Naming Convention:**
   * Naye feature ke liye: `feature/<task-name>` (e.g., `feature/user-auth`)
   * Bug fix ke liye: `fix/<bug-name>` (e.g., `fix/navbar-overlap`)
   * Aapke naam ke saath: `dev/<your-name>/<task>`
4. `Enter` press karo. Bottom-left me ab aapki nayi branch ka naam show hone lagega.

---

## Step 3: Kaam Karo & Changes Review Karo

Files me edit karo aur save (`Ctrl + S`) karo. Source Control panel me files aane lagengi:

* **M (Modified):** Existing file change hui hai.
* **U (Untracked):** Nayi file banayi gayi hai.
* **D (Deleted):** File delete ki gayi hai.
* Kisi bhi file par click karke dekho:
  * 🟥 **Red:** Purana code jo hata.
  * 🟩 **Green:** Naya code jo add hua.

---

## Step 4: Stage & Commit

1. **Stage Changes:**
   * Sabhi files save karni hain: **Changes** header ke samne `+` (Stage All Changes) click karo.
   * Sirf single file karni hai: Us file ke samne `+` click karo.
   * File(s) ab **"Staged Changes"** section me move ho jayengi.
2. **Commit Message Likho:**
   * Top text box me meaningful summary likho:
     * ✅ `feat: add reset password form validation`
     * ❌ `changes`, `done`, `asdf`
3. Click **Commit (✓)** blue button (ya `Ctrl + Enter`).

---

## Step 5: "Repo is Ahead" Problem & Pull with Rebase

Aksar aisa hoga ki jab tak aapne kaam kiya, tab tak kisi aur ka code `main` me merge ho chuka hai, aur aapka branch outdated ho gaya. Aise me clean history ke liye **Pull (Rebase)** use karo:

1. Source Control tab me upar `...` (Three dots) pe click karo.
2. Go to: **Branch** > **Rebase Branch...**
3. Select karo: `origin/main` ya `main`.
4. *Alternative GUI way:*
   * `...` (Three dots) > **Pull, Push** > **Pull (Rebase)**.
5. Isse team ke latest changes aapke code ke peeche safely arrange ho jayenge bina messy merge commits banaye.

---

## Step 6: Publish / Push to GitHub

Pehli baar nayi branch push karte waqt:

1. Blue button dikhega: **"Publish Branch"**. Uspe click kar do.
2. Next time jab usi branch par naye commits push karne hon:
   * Click **Sync Changes** ya `...` > **Push**.
3. *Note:* Agar direct `main` par push karoge to GitHub reject kar dega ("Protected branch hook declined"). Hamesha apni feature branch hi push karo!

---

## Step 7: Pull Request (PR) Raise Karna

Code push hone ke baad GitHub par PR banna zaroori hai:

1. Browser me repo open karo (ya VS Code me popup aayega *"Open on GitHub"*).
2. GitHub upar ek yellow banner dikhayega: **"Compare & pull request"**. Uspe click karo.
3. Check karo:
   * **Base:** `main`
   * **Compare:** `your-branch-name`
4. Title aur description me likho kya kaam kiya hai.
5. Click **"Create Pull Request"**.
6. Reviewer assign karo aur WhatsApp/Slack pe inform kar do!

---

## 🛠️ Undo / Oops Actions (Galti Sudharne Ke Tarike)

### 1. "De-commit" karna (Commit wapas rollback karna)
Agar galti se commit button daba diya aur kuch files miss ho gayi ya galat message chala gaya:
* Source Control me `...` (Three dots) par click karo.
* Select: **Commit** > **Undo Last Commit**.
* *Result:* Commit cancel ho jayega, but aapka code safe rahega (wapas Staged/Changes me aa jayega).

### 2. Unstage karna (Galti se `+` daba diya)
* **Staged Changes** section me file ke samne minus icon (`-`) click karo. File wapas normal Changes me chali jayegi.

### 3. Galti se galat code likh diya (Discard Changes)
* Agar koi experimental code likh diya jo nahi chahiye:
* File ke samne **Discard Changes** icon (`↩️` / counter-clockwise arrow) par click karo.
* *Warning:* Discard karne ke baad wo local changes permanently delete ho jate hain!

### 4. Temporary kaam save karke branch switch karni hai (Stash)
Agar bina commit kiye urgent dusri branch dekhni hai:
* `...` (Three dots) > **Stash** > **Stash (Include Untracked)**.
* Branch switch karo, kaam dekho, wapas aao.
* `...` > **Stash** > **Pop Stash** (Aapka aadha kaam wapas aa jayega).

---

## ⚡ Quick Cheat Sheet for Common Scenarios

| Situation / Problem | VS Code GUI Solution |
| :--- | :--- |
| **Wrong branch par khade ho?** | Bottom-left branch name par click karke correct branch choose karo. |
| **Main branch direct push reject hui?** | Nayi branch banao, code wahan commit karke push karo. |
| **Merge conflict aa gaya?** | File open karo -> Click `Accept Incoming` ya `Accept Current` -> Save (`Ctrl + S`) -> `+` Stage -> Commit. |
| **Changes gayab ho gaye?** | Check karo aapne branch to nahi badal li, ya Stash to nahi kar diya. |
| **GitHub password / auth maang raha hai?** | VS Code bottom-left accounts icon par click karke *"Sign in with GitHub"* authorize karo. |