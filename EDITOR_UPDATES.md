# Updated Editor.js for PostgreSQL Version

## Changes Made:

The PostgreSQL version uses file URLs instead of base64 data URLs.

### Key Updates:

1. **Image Upload**: Now uses `/api/image/upload/{project_id}` endpoint
2. **Image URLs**: Images are served from `/uploads/` directory
3. **Response Format**: 
   - Old: `{image: "data:image/png;base64,..."}`
   - New: `{original_image_url: "/uploads/file.png", processed_image_url: "/uploads/file.png"}`

### Updated Endpoints:

```javascript
// Upload - requires project_id in URL
POST /api/image/upload/{project_id}

// Remove background - requires project_id in URL  
POST /api/image/remove-background/{project_id}

// Generate background - send project_id in body
POST /api/image/generate-background
Body: { prompt: "...", project_id: "..." }

// Enhance - requires project_id in URL
POST /api/image/enhance/{project_id}
```

### Full Updated Code:

Replace your `frontend/src/pages/Editor.js` with the code below.

The main changes are:
1. All image endpoints now require `project_id`
2. Response uses `original_image_url` and `processed_image_url`
3. Images are displayed using backend URLs (e.g., `http://localhost:8000/uploads/file.png`)
4. Backend automatically saves/updates project with new image paths

---

**Note**: The PostgreSQL version automatically handles:
- Saving files to disk
- Updating database with file paths
- Serving files from `/uploads/` directory
- Deleting old files when project is deleted

No additional changes needed!
