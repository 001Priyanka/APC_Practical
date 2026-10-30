# BlogHub: Comprehensive QA, Security & Verification Report

**Date of Review:** October 2026  
**Auditor:** Senior QA Engineer & Security Reviewer  
**Target Codebase:** `D:\PythonBlogProject`  
**Primary Framework:** Django 5.1.15 / Python 3.10.7  

---

## 1. Executive Summary

A comprehensive architectural inspection, security audit, and test execution was conducted across the entire **BlogHub** platform. The codebase adheres to the Monolithic MTV architecture specified in [`PROJECT_PLAN.md`](file:///D:/PythonBlogProject/PROJECT_PLAN.md).

All **56 automated unit and integration tests** executed cleanly across all three core applications (`accounts`, `blogs`, `interactions`) with **0 failures and 0 errors**.

| Test Suite | Total Tests | Passed | Failed | Status |
| :--- | :---: | :---: | :---: | :---: |
| **`accounts`** | 19 | 19 | 0 | **PASS** |
| **`blogs`** | 26 | 26 | 0 | **PASS** |
| **`interactions`** | 11 | 11 | 0 | **PASS** |
| **Total Test Suite** | **56** | **56** | **0** | **PASS (100%)** |

---

## 2. Django System & Migration Integrity Checks

### 2.1 Django System Check
- **Command:** `python manage.py check`
- **Output:** `System check identified no issues (0 silenced).`
- **Result:** **PASS**

### 2.2 Unapplied Migration Detection
- **Command:** `python manage.py makemigrations --check --dry-run`
- **Output:** `No changes detected`
- **Result:** **PASS** (Models and database migration schemas are 100% in sync)

---

## 3. Database Connectivity & Environment Audit

### 3.1 MySQL Connectivity Test
- **Tested Host / Port:** `127.0.0.1:3306`
- **Result:** **OFFLINE (Timed out)**
- **Technical Explanation:**
  The Windows environment does not currently have an active MySQL 8 service running on port 3306 (MySQL Workbench is present, but MySQL Server service is stopped or uninstalled).
- **Graceful Fallback:**
  As required by the project specifications, **SQLite** (`db.sqlite3`) serves as the active, documented temporary development database via `.env` (`DB_ENGINE=sqlite`).
- **Steps to Enable MySQL:**
  1. Start MySQL Server: `net start MySQL80` (or start MySQL in XAMPP / MariaDB control panel).
  2. Create database:
     ```sql
     CREATE DATABASE bloghub_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
     ```
  3. Update `D:\PythonBlogProject\.env`:
     ```env
     DB_ENGINE=mysql
     DB_NAME=bloghub_db
     DB_USER=root
     DB_PASSWORD=your_actual_password
     DB_HOST=127.0.0.1
     DB_PORT=3306
     ```
  4. Run `python manage.py migrate`.

---

## 4. Security & Access Control Review

### 4.1 Row-Level Authorization
- **Blog Editing & Deletion:**
  - Tested: Attempting `GET` or `POST` to edit another author's blog (`/blogs/<slug>/edit/`) triggers an HTTP **403 Forbidden**.
  - Tested: Attempting `POST` to delete another author's blog (`/blogs/<slug>/delete/`) triggers an HTTP **403 Forbidden**.
- **Comment Deletion:**
  - Tested: Attempting `POST` to delete someone else's comment triggers an HTTP **403 Forbidden**.
  - Verified: Only the comment author or the blog owner can delete comments.
- **Profile Manipulation:**
  - The profile edit view (`profile_edit_view`) strictly updates `request.user` without accepting external user identifiers in URL patterns.

### 4.2 Draft Privacy Enforcement
- **Public Feed:** Verified that draft blogs are excluded from `/blogs/`, `/search/`, and author profiles.
- **Direct Slug Access:** Verified that requesting a draft's URL as an unauthenticated or non-author visitor triggers an HTTP **404 Not Found**.

### 4.3 Form & File Upload Validation
- **Image Upload Validator:**
  - Max avatar size: 2MB; Max cover size: 5MB.
  - Allowed extensions: `.jpg`, `.jpeg`, `.png`, `.webp`.
  - Server-side image verification using Pillow (`Image.verify()`).
- **CSRF Protection:**
  - Verified that all mutating actions (`POST`) contain valid CSRF tokens (`{% csrf_token %}`).
  - Destructive actions (deleting blogs, deleting comments) strictly disallow `GET` requests.

### 4.4 Information Leakage Prevention
- **Email Privacy:** Author email addresses are hidden on public author profile pages and directories.
- **Passwords:** Passwords are never stored or transmitted in plain text. Hashed using PBKDF2/SHA256.

---

## 5. Bugs Identified & Fixed During Audit

| Issue # | Component | Severity | Description | Fix Applied |
| :---: | :--- | :---: | :--- | :--- |
| **BUG-01** | `interactions` | High | `interactions/views.py` contained placeholder views from scaffolding, leaving comments, likes, and bookmarks unlinked on the frontend. | Implemented full views (`add_comment_view`, `delete_comment_view`, `toggle_like_view`, `toggle_bookmark_view`, `bookmarks_list_view`) with row-level permission enforcement and CSRF validation. |
| **BUG-02** | `templates/blogs/blog_detail.html` | High | Blog detail page was missing engagement controls (likes, bookmarks, comments list, and comment submission form). | Integrated reaction buttons with live counters, bookmarked status, comment list, and delete actions for authors. |
| **BUG-03** | `templates/base.html` | Medium | Navbar dropdown link to `Saved Bookmarks` previously routed to a placeholder view. | Created dedicated [`templates/interactions/bookmarks_list.html`](file:///D:/PythonBlogProject/templates/interactions/bookmarks_list.html) with pagination and un-bookmark actions. |
| **BUG-04** | `config/settings.py` | Low | Test client host `testserver` was rejected when running standalone scripts. | Added `testserver` to `ALLOWED_HOSTS` when `DEBUG=True`. |
| **BUG-05** | `accounts/tests.py` | Low | Django 5.1 `assertFormError` signature requires the form instance rather than the response object. | Updated test calls to `self.assertFormError(response.context['form'], ...)`. |

---

## 6. Remaining Issues / Operational Notes

1. **MySQL Offline in Local Host Environment:**
   MySQL service on `127.0.0.1:3306` is not currently started. The platform operates reliably with SQLite fallback until the user starts their MySQL service.
2. **Production Deployment Readiness:**
   Before deploying to a public server:
   - Set `DEBUG=False` in `.env`.
   - Generate a cryptographically random `SECRET_KEY`.
   - Update `ALLOWED_HOSTS` with your production domain name.

---

## 7. Exact Commands to Reproduce All Tests

Open PowerShell in `D:\PythonBlogProject`:

```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Run Django configuration check
python manage.py check

# 3. Check for schema/model drift
python manage.py makemigrations --check --dry-run

# 4. Run accounts unit tests (19 tests)
python manage.py test accounts

# 5. Run blogs unit & discovery tests (26 tests)
python manage.py test blogs

# 6. Run interactions unit & permission tests (11 tests)
python manage.py test interactions

# 7. Run full project test suite (56 tests)
python manage.py test
```
