# Zedu Channel Files Tab & Document Preview — Exquisite Design Specification

> **Target Component:** `ChannelDetailsDialog` ➔ `Files` Tab (`files-tab-container.tsx`) & `DocumentPreviewModal` (`document-preview-modal.tsx`)  
> **Frame Constraint:** Preserves exact parent dialog dimensions (`w-[600px]`, `h-[600px]`, scrollable viewport `h-[440px]`).  
> **Preview Modal Dimension:** Expands document preview from narrow box (~560px) to spacious **wide desktop canvas** (`w-[960px]` / `max-w-6xl`, `h-[88vh]`).  
> **Inspiration & Aesthetic Benchmark:** Slack + Notion + Native PDF Reader (clean, codebase-aligned, zero visual clutter, seamless micro-interactions).

---

## 1. Executive Summary & Design Rationale

### Current Flaws Identified in Production:
1. **Unrefined Content Hierarchy & Truncation:** Date dividers are raw text (`OCTOBER 6`), document items have misaligned thumbnail boxes and disjointed labels, and images have uneven aspect ratios with cut-off text (`eam lead`).
2. **Missing Discovery & Metadata:** In active channels with 300+ contributors, users cannot search files by name. No file size tags (e.g., `2.4 MB`), no semantic format badges, and no hover action triggers.
3. **No Direct Document Quick Actions:** Document files force users into cumbersome nested flows without direct `Download`, `Share`, or `Open in browser` action buttons.
4. **Cramped Document Preview Dialog:** In production, `DocumentPreviewModal` renders in a small, narrow modal (~560px–600px wide), squeezing page thumbnails and document sheets into an unreadable column with horizontal scrollbars.
5. **Over-engineered View Switching:** Introducing artificial list/grid toggles creates unnecessary UI noise. The existing codebase layout in `files-tab-container.tsx` already pairs a square media grid for images/videos with an item list for documents and audio.

### Redesign Goals:
* **Maintain exact modal bounds** (`h-[600px]`, `w-[600px]`) without altering the parent tab bar (`About`, `People [303]`, `Agents`, `Files [24]`).
* **Sub-Tab Categorization:** Sub-filters in exact order: `All (24)`, `Documents (10)` first right after All, `Images (8)`, `Videos (4)`, `Audio (2)` with item counters.
* **Remove View Toggle:** Eliminate grid/list toggle buttons from the sub-toolbar.
* **Codebase-Aligned "All" Tab Layout:** In every date group, render a 4-column square media grid at top for images/videos (with centered video play overlay), followed by a list of documents and audio underneath.
* **Inline "Open File" Cue:** Remove bulky `[Preview]` buttons. Display an interactive `Open file ↗` link cue on hover/interaction.
* **Document Action Buttons:** Equip document files with dedicated quick actions: `Download`, `Share`, and `Open in browser`.
* **Wide Document Preview Modal:** Redesign the document preview dialog into a wide desktop viewport (`w-[960px]`–`1024px`) with a top bar (`[PDF]`, `[⬇ Download]`, `[🔗 Share]`, `[↗ Open]`, `[✕]`), sub-toolbar (`Page 1 / 4`, zoom, fit, print), thumbnail sidebar, and crisp page canvas.

---

## 2. Design Tokens & Visual Foundations

| Token | Value | Application |
| :--- | :--- | :--- |
| **Brand Primary** | `#5F5FE1` (Indigo/Purple) | Active sub-tab pill fill, search focus ring, primary CTA |
| **Primary Subtle** | `#F1F1FE` | Active sub-tab background, card hover tint |
| **Download Accent** | `#7141F8` (Vibrant Purple) | Primary Download button in document preview header |
| **Surface Base** | `#FFFFFF` | Card backgrounds, modal surface |
| **Surface Subdued** | `#FAFBFD` / `#F8F9FB` | Sub-toolbar background, skeleton placeholders |
| **Border Soft** | `#EAEBF0` / `#E5E7EB` | File card dividers, input borders |
| **Border Active** | `#CBD0DC` | Hovered card stroke |
| **Text Dominant** | `#1D2939` / `#101828` | File names, modal headers |
| **Text Muted** | `#667085` | Uploader name, date headers, metadata |
| **Text Subtle** | `#98A2B3` | Timestamps, file size tags |
| **PDF Accent** | `#E53935` / `#D92D20` | PDF badge background / icon |
| **DOC Accent** | `#175CD3` | DOCX badge background |
| **Video Accent** | `#C11574` | MP4 video badge & duration tag |
| **Audio Accent** | `#B54708` / `#F79009` | Audio waveform / M4A badge |

---

## 3. Sub-Tab & Sub-Toolbar Specification

### 3.1 Sub-Toolbar (`px: 24px`, `py: 12px`, `bg: #FAFBFD`, `border-b: 1px solid #EAEBF0`)
1. **Search Input (`w: 140px`):**
   * Placeholder: `"Search files..."`
   * Prefix: Micro 13px search lens (`#98A2B3`).
   * Interaction: Real-time client-side filter with query highlighting.
2. **Sub-Filter Pills (`gap: 5px`):**
   * Pills order: `All (24)`, `Documents (10)` (first after All), `Images (8)`, `Videos (4)`, `Audio (2)`.
   * **Inactive Pill:** Border `#E4E7EC`, Text `#475467`, Background `#FFFFFF`, Hover `#F2F4F7`.
   * **Active Pill:** Background `#5F5FE1`, Text `#FFFFFF`, Border `#5F5FE1`, font-semibold.
3. **No View Mode Toggle:** No segmented buttons or view switchers; clean, uncluttered toolbar.

---

## 4. Layout Architecture: "All" Tab vs Demarcated Tabs

### 4.1 "All" Tab (Codebase Dual Listing Architecture)
In each date section (`October 6 · Today`, `October 5 · Yesterday`, `October 4 · Earlier`):
1. **Date Header:** Semantic badge e.g. `OCTOBER 6 · TODAY` (uppercase, 11px font, `#667085`).
2. **Media Grid (Top):**
   * 4 columns of aspect-square thumbnails (`code-media-grid`).
   * Images display cover thumbnail.
   * Videos display cover thumbnail with a centered play icon overlay (`video-play-center`) and duration tag (e.g. `45:12`).
   * Clicking any media triggers instant high-res media view.
3. **Document & Audio List Stack (Bottom):**
   * Non-media files (PDF, DOCX, M4A, FIG, XLSX, ZIP) listed underneath.
   * Elements: User avatar + semantic file type icon (PDF, DOC, FIG, AUDIO, ZIP) + filename + inline `Open file ↗` cue + file size tag + uploader & timestamp.
   * Document files have dedicated quick actions: `Download`, `Share`, `Open` (in browser).

### 4.2 "Documents" Tab
* Strictly lists documents only (zero images or videos).
* Features full document quick action buttons on every row: `[⬇ Download]`, `[🔗 Share]`, `[↗ Open in browser]`.
* Clicking the row or title opens the **Wide Document Preview** dialog.

### 4.3 "Images" & "Videos" Tabs
* Images tab strictly shows image assets with cover thumbnails and author tags.
* Videos tab strictly shows video recordings with duration stamps, centered play icons, and sizes.

### 4.4 "Audio" Tab
* Strictly shows voice notes and recordings with playable waveform visualizer bars.

---

## 5. Wide Document Preview Dialog Architecture

> **Solving Production Pain Point:** Replaces the cramped ~560px box with a wide `960px`–`1024px` desktop canvas.

### 5.1 Component Structure
```
┌───────────────────────────────────────────────────────────────────────────────────┐
│ [PDF] Ticket_Guide_Stage1.pdf (2.4 MB · @sadiq)    [⬇ Download] [🔗 Share] [↗ Open] [✕] │  <-- Header
├───────────────────────────────────────────────────────────────────────────────────┤
│ ≡ Page 1 / 4   |  −  100%  +   |   ⛶ Fit   ↻ Rotate   🖶 Print                    │  <-- PDF Sub-bar
├──────────────────────────┬────────────────────────────────────────────────────────┤
│ ┌──────────────────────┐ │                                                        │
│ │ [PAGE 1]             │ │              How to Submit Your Ticket                 │
│ │                      │ │              Stage 1 Ticket Guide                      │
│ └──────────────────────┘ │                                                        │
│ ┌──────────────────────┐ │              1. What is Stage 1?                       │
│ │ [PAGE 2]             │ │              Before your ticket goes on GitHub...      │
│ └──────────────────────┘ │                                                        │
│ ┌──────────────────────┐ │              The 4 Steps to Follow:                    │
│ │ [PAGE 3]             │ │              1. Copy the ticket template...            │  <-- Wide Canvas
│ └──────────────────────┘ │                                                        │
│ (Thumbnail Sidebar 220px)│                 (Wide 620px-680px Sheet Canvas)        │
├──────────────────────────┴────────────────────────────────────────────────────────┤
│                          Press  [ ESC ]  to close preview                          │  <-- Footer
└───────────────────────────────────────────────────────────────────────────────────┘
```

1. **Header (`h: 56px`, `bg: #FFFFFF`, `border-b: 1px solid #E5E7EB`):**
   * Left: Red `[PDF]` badge + document filename (`Ticket_Guide_Stage1.pdf`) + metadata (`2.4 MB · Shared by @sadiq in #zedu-contributors`).
   * Right Action Buttons:
     * `[⬇ Download]`: Purple fill (`bg: #7141F8`, text: `#FFFFFF`), download icon.
     * `[🔗 Share]`: Outlined secondary button, share icon.
     * `[↗ Open]`: Outlined secondary button, external link icon (opens raw file in new browser tab).
     * `[✕]`: Accessible close button.
2. **Sub-Toolbar (`h: 38px`, `bg: #323639`, `color: #E5E7EB`):**
   * Page counter: `Page 1 / 4`.
   * Zoom controls: `− 100% +`.
   * Tools: `⛶ Fit`, `↻ Rotate`, `🖶 Print`.
3. **Split Viewer Body:**
   * **Left Thumbnail Sidebar (`w: 220px`, `bg: #323639`):** Page cards (1, 2, 3, 4) with active blue/purple outline and page numbering.
   * **Right Canvas Sheet Area (`flex: 1`, `bg: #525659`):** Wide white document sheet (`620px` width) displaying crisp high-resolution ticket guide text, formatted table, and realistic margins without horizontal scrollbars.
4. **Footer:** `Press ESC to close preview`.

---

## 6. Reviewer Alignment & Production Implementation Summary

* **Codebase Alignment:** Re-uses the actual layout logic in `files-tab-container.tsx` (`groupFiles.filter(cat === 'image' || cat === 'video')` for grid, and `cat === 'document' || cat === 'audio'` for list stack).
* **Direct Actions:** Eliminates friction by placing `Download`, `Share`, and `Open` on document items and the preview header.
* **Desktop Ergonomics:** The wide document preview makes reading guidelines and reviewing code submissions legible and pleasant on desktop screens.
* **Interactive Prototype:** Available at `designs/files-tab-redesign/index.html`.
