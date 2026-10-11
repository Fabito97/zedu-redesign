### Name
Fabian Muoghalu

### Zedu username
Fabbenco

### Zedu team
Team Vader

### Summary / Description
The Files tab in the channel details dialog mixes media and documents indiscriminately, suffers from awkward aspect ratios with clipped labels ("eam lead"), lacks search and file size indicators, and provides no direct document actions. Furthermore, the document preview dialog is cramped and small, forcing dual scrollbars on desktop. Propose a clean, codebase-aligned redesign of the Files tab and a wide Document Preview dialog: remove the unnecessary grid/list view toggle, replace bulky preview buttons with an inline "Open file" cue, equip document files with dedicated quick action buttons (Download, Share, Open in browser), retain the codebase's dual listing layout for the All tab (media grid on top, documents and audio below), and expand the document preview window to a wide desktop canvas.

### Why is this ticket needed?
In active channels like #zedu-contributors (with 300+ members and hundreds of shared assets), finding lecture slides, video recordings, wireframes, or sprint briefs is slow and frustrating. Currently:
1. Videos and images are lumped together with documents without duration stamps or proper aspect ratios, filenames are clipped (e.g. "eam lead"), and there are no file sizes.
2. Documents lack immediate quick actions: learners must hunt for links instead of having one-click Download, Share, or Open in browser buttons.
3. The document preview dialog (`DocumentPreviewModal`) is currently small and narrow (~560px–600px), causing the thumbnail sidebar and document canvas to squeeze together with horizontal scrollbars (proof: attached screenshot).
4. An over-complicated grid/list view toggle adds visual clutter instead of aligning with the existing codebase pattern (`files-tab-container.tsx`), where media is shown in a square grid and non-media documents are listed below.

Placing Documents first after All, providing inline "Open file" cues, adding Download/Share/Open action buttons, adhering to the codebase layout, and widening the document preview dialog solves all these usability problems cleanly.

### Details
Current behaviour:
- Files and media are mixed without clear demarcation; video recordings and images share the same container without duration stamps or proper aspect ratios.
- Filenames and labels are cut off awkwardly (e.g., "eam lead" instead of full descriptive titles).
- No file size tags (e.g., 2.4 MB, 128 MB) or distinct file-type badges.
- Search is completely absent in the Files tab; users cannot filter files by name, extension, or uploader.
- Bulky "Preview" buttons clutter file cards or lack clear affordance.
- Document files have no direct action buttons for Download, Share, or Open in browser on their rows.
- The Document Preview modal dialog is small and narrow, squeezing PDF pages and thumbnail rails into a cramped space with awkward horizontal scrollbars.
- No empty states for search queries, empty filter categories, or channels with zero files.

Proposed design:
- **Clean Sub-Toolbar (No Grid/List Toggle):** Clean, native sticky bar containing search input and sub-filter pills in exact order: All (24), Documents (10) placed first right after All, Images (8), Videos (4), Audio (2).
- **Codebase-Aligned "All" Tab Layout:** Each date group employs the exact structure in `files-tab-container.tsx`:
  - **Media Grid at Top:** 4-column square aspect-ratio grid for images and videos (with centered video play overlay and duration stamp).
  - **Document & Audio List Underneath:** Clean rows for documents, audio, and archives with uploader avatar, file type badge, uploader name, timestamp, and size.
- **Inline "Open File" Cue:** Bulky "Preview" buttons are removed. Hovering or clicking on a file displays a tiny "Open file ↗" cue, and clicking opens the file directly.
- **Dedicated Document Action Buttons:** Every document row provides explicit, accessible action buttons:
  - `Download`: Direct one-click download.
  - `Share`: Copies the shareable file URL to clipboard.
  - `Open`: Opens the raw document in a new browser tab.
- **Wide Document Preview Dialog:** Expands from a cramped ~600px box to a spacious wide modal (`w-[960px]` / `max-w-6xl`, `88vh` height):
  - **Header:** File badge (`[PDF]`), full filename, purple primary `[⬇ Download]` button, outlined `[🔗 Share]` button, outlined `[↗ Open]` button, and `[✕]` close button.
  - **PDF Sub-Toolbar:** Page counter (`Page 1 / 4`), zoom controls (`− 100% +`), page fit, rotate, print.
  - **Spacious Split View:** Left thumbnail sidebar with comfortable page cards; right wide document sheet canvas displaying high-resolution readable pages without horizontal clipping.
  - **Footer:** `Press ESC to close` keyboard shortcut cue.
- **Special States:** Search active with query highlighting, empty search results / category filter, zero channel files, and skeleton shimmer loading.

### Scope: frontend only.
No backend change is needed.

### Steps to reproduce
1. Open #zedu-contributors (or any channel with shared assets).
2. Click the channel header or details icon, then navigate to the Files tab.
3. Observe that videos and images are lumped together with truncated labels ("eam lead") and no duration stamps.
4. Try to search for a specific file like "Ticket_Guide"—no search bar is available.
5. Click on a PDF document (such as `Ticket_Guide_Stage1.pdf`)—observe that the preview dialog is cramped, narrow, and cuts off document margins horizontally.

### Acceptance criteria
- Sub-filter pills strictly follow the order: All, Documents, Images, Videos, Audio, each displaying accurate count badges.
- No segmented grid/list view toggle; interface remains clean, focused, and codebase-native.
- In the "All" tab, each date section displays images and videos in a 4-column square media grid at the top, and non-media files (documents, audio) listed below.
- Bulky "Preview" buttons are removed; hovering or clicking on a file displays a tiny "Open file ↗" cue.
- Document files feature explicit action buttons: Download, Share, and Open in browser.
- The document preview window/dialog box is wide (`w-[960px]`–`1024px`), preventing page clipping and eliminating horizontal scrollbars.
- The document preview dialog includes top action buttons matching production: `[Download]` (purple), `[Share]`, `[Open]`, and `[✕]`, with page thumbnails and `ESC` to close.
- Search input filters files in real time, highlighting matching text and displaying a "Showing X files matching <query> · Clear search" banner.
- Empty states are provided for: (1) no search results / empty category filter with a "Reset filters" CTA, and (2) zero files in channel with an "Upload file" CTA.
- Loading displays smooth skeleton shimmer cards instead of an empty space or generic spinner.
- Preserves the parent dialog frame (600px × 600px) and channel header elements (# zedu-contributors, close ✕, Star, Mute).

### Links / Screenshots
### Before:

Narrow, cramped document preview dialog in production:
<img width="1918" height="909" alt="Before - Cramped Document Preview" src="https://github.com/user-attachments/assets/9d8a434a-e740-4fa0-83d8-3a4120173420" />

### After:
(Interactive prototype and design specification featuring clean codebase layout, document quick actions, tiny open file cues, and wide document preview window)

- Interactive Prototype: `c:\Users\hp\Documents\hng\zedu\designs\files-tab-redesign\index.html`
- Design Specification: `c:\Users\hp\Documents\hng\zedu\designs\files-tab-redesign\DESIGN_SPEC_FILES_TAB.md`
