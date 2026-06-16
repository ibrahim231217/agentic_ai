# Usage Examples - How to Use the Application

This guide shows practical examples of using the Agentic AI Document Assistant.

---

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Workflow Scenarios](#workflow-scenarios)
3. [Tips & Tricks](#tips--tricks)
4. [Example Outputs](#example-outputs)

---

## Basic Usage

### Example 1: Simple Document Processing

**Scenario:** You have a project proposal that needs review and summary

**Steps:**

1. **Start the app:**
   ```bash
   cd c:\coding_foLdER\agentic_AI
   streamlit run app.py
   ```
   Browser opens at `http://localhost:8501`

2. **Upload document:**
   - Click "Choose a document"
   - Select your proposal file (PDF, DOCX, or TXT)
   - Wait for "✅ Document loaded successfully!"

3. **View preview:**
   - Click "📖 Document Preview"
   - Review first 500 characters
   - Verify text extracted correctly

4. **Run first agent (Document Agent):**
   - Click "✍️ Document Agent" button
   - Wait ~15-30 seconds
   - See "✅ Document Agent completed successfully!"

5. **View results:**
   - Expanded section shows:
     - **Improved Document** - Grammar corrected version
     - **Changes Summary** - What was fixed
   - Click "⬇️ Download Improved Document" to save

6. **Run second agent (Summary Agent):**
   - Click "📊 Summary Agent" button
   - Wait ~15-30 seconds
   - See results in new section:
     - Executive summary (3-5 sentences)
     - Bullet points
     - Key takeaways
   - Download summary if needed

7. **Run third agent (Info Agent):**
   - Click "📈 Info Agent" button
   - Wait ~15-30 seconds
   - Extract:
     - Important entities
     - Action items
     - Key data points
     - Categorized information

8. **Download complete report:**
   - Click "⬇️ Download Complete Report (All Agents)"
   - Contains all results from all three agents
   - Great for stakeholders

### Expected Flow

```
Upload Document
    ↓ (Check preview)
Click Document Agent
    ↓ (Wait 15-30 sec)
View improved document
    ↓ (Optional: Download)
Click Summary Agent
    ↓ (Wait 15-30 sec)
View executive summary
    ↓ (Optional: Download)
Click Info Agent
    ↓ (Wait 15-30 sec)
View extracted information
    ↓ (Optional: Download)
Download Complete Report
    ↓
Done!
```

**Total time:** ~2-5 minutes per document

---

## Workflow Scenarios

### Scenario 1: Business Proposal Review

**Situation:** Received a 10-page business proposal, need to understand quickly

**What to do:**

1. Upload the proposal (PDF or DOCX)
2. **Only run Summary Agent**
   - Get executive summary (2 min)
   - Review bullet points
   - Identify key terms and metrics
3. Download summary for team review
4. Optionally run Document Agent if editing needed

**Time:** ~5 minutes for entire review

---

### Scenario 2: Document Improvement for Submission

**Situation:** Need to improve writing quality before submitting document

**What to do:**

1. Upload document (TXT, DOCX)
2. **Run Document Agent first**
   - Get grammar corrections
   - See writing improvements
   - Review changes summary
3. Download improved document
4. Open in Word/Notepad
5. Review changes
6. Use improved version for submission

**Time:** ~5-10 minutes

---

### Scenario 3: Research Paper Analysis

**Situation:** Have academic paper, need structured summary and key points

**What to do:**

1. Convert paper to PDF (if needed)
2. Upload paper
3. **Run all three agents in order:**
   - Summary Agent → Get structured summary
   - Info Agent → Extract entities, citations, methodology
   - Document Agent → Review for clarity (optional)
4. Download complete report
5. Use for literature review or presentation prep

**Time:** ~10 minutes for complete analysis

---

### Scenario 4: Meeting Minutes Processing

**Situation:** Have meeting notes, need action items and summary

**What to do:**

1. Save meeting notes as TXT
2. Upload file
3. **Run Info Agent**
   - Extract action items
   - Identify responsible parties
   - Find deadlines
4. **Run Summary Agent**
   - Get meeting overview
   - Key decisions made
5. Download both reports
6. Share with team

**Time:** ~8 minutes

---

### Scenario 5: Batch Processing Multiple Documents

**Situation:** Have 5 documents to process quickly

**What to do:**

1. Start app
2. For each document:
   - Upload
   - Run agents (2-5 min each)
   - Download results
   - Clear for next document
3. Compile all downloads into folder

**Tips:**
- Focus on one agent per document if time-limited
- Summary Agent usually quickest for initial review
- Save results immediately

**Time:** ~30 minutes for 5 documents

---

## Tips & Tricks

### Performance Tips

**Faster Processing:**
- Use TXT files instead of PDF/DOCX
- Upload documents < 5MB for best speed
- Use WiFi instead of mobile hotspot
- Close other browser tabs

**Better Results:**
- Use well-formatted documents
- Remove images/formatting if not needed
- Use documents with clear sections
- Avoid scanned PDFs (text extraction won't work)

### Quality Tips

**Document Agent Best Results:**
- Works best with academic/professional documents
- Good for fixing grammar errors
- Great for improving clarity
- Use for formal submissions

**Summary Agent Best Results:**
- Best with Gemini API (check "API Used")
- Good for long documents (1000+ words)
- Great for technical documents
- Quick understanding of content

**Info Agent Best Results:**
- Best for structured documents
- Great for reports with data
- Good for identifying entities
- Useful for action items

### Workflow Tips

**Tip 1: Check Preview First**
```
Always click "Document Preview" before running agents
Ensures text extracted correctly
Saves time if extraction failed
```

**Tip 2: Start with One Agent**
```
Don't run all at once
Test Document Agent first
Verify it works before others
```

**Tip 3: Download as You Go**
```
Don't wait until end to download
Download each agent result individually
Prevents losing work if something fails
```

**Tip 4: Use Complete Report**
```
Use "Complete Report" when running all agents
Combines everything in professional format
Easy to share with team
Better for documentation
```

**Tip 5: Save Outputs**
```
Create folders for each project
Save reports immediately
Backup important results
Organize by date
```

### Troubleshooting During Use

| Issue | Quick Fix |
|-------|-----------|
| Blank response | Try shorter document or simpler format |
| Slow processing | Check internet, try smaller file |
| Wrong API used | Verify API keys, restart app |
| Download fails | Try different browser, check storage space |
| Agents not showing | Verify .env file, restart app |

---

## Example Outputs

### Example 1: Document Agent Output

**Input Document:**
```
The project have been completed last week. It was a sucessful 
initiative that achieved it's goals. The team worked hard and 
were very productive.
```

**Output from Document Agent:**

```
IMPROVED DOCUMENT
=====================================
The project was completed last week. It was a successful 
initiative that achieved its goals. The team worked hard and 
demonstrated exceptional productivity.

CHANGES SUMMARY
=====================================
- Fixed verb tense: "have been completed" → "was completed"
- Corrected spelling: "sucessful" → "successful"
- Fixed possessive: "it's" → "its"
- Enhanced language: "were very productive" → "demonstrated exceptional productivity"
- Improved overall professional tone and clarity
```

---

### Example 2: Summary Agent Output

**Input Document:** (5-paragraph project proposal)

**Output from Summary Agent:**

```
EXECUTIVE SUMMARY
We propose a new customer management system to streamline 
operations and reduce processing time by 40%. The project 
requires $100K investment and will be completed in Q3 2024.

BULLET-POINT SUMMARY
• Objective: Implement CRM system for better customer service
• Budget: $100,000
• Timeline: 6 months (Complete by Q3 2024)
• Team: 3 developers, 1 project manager
• Expected ROI: 40% reduction in processing time
• Training: 2-week implementation period

KEY TAKEAWAYS
• System should reduce manual work and errors
• Budget is realistic for scope of work
• Timeline requires experienced team
• Success depends on stakeholder adoption
• Recommend phased implementation approach
```

---

### Example 3: Information Agent Output

**Input Document:** (Meeting notes)

**Output from Information Agent:**

```
IMPORTANT ENTITIES
• Sarah Johnson - Product Lead
• Engineering Team - 5 members
• Q2 2024 - Timeline
• AWS Infrastructure - Technology
• 50% increase - Performance target

ACTION ITEMS
• Sarah: Create detailed requirements document (Due: Tuesday)
• Engineering Lead: Estimate development time (Due: Friday)
• Finance: Approve budget allocation (Due: Next week)
• IT: Provision AWS resources (Due: Before start date)

KEY DATA POINTS
• Budget: $250,000
• Team size: 5 engineers
• Timeline: 6 months
• Expected performance improvement: 50%
• Number of modules: 7
• Integration points: 3 external systems

CATEGORIZED INFORMATION
TECHNICAL:
- Tech stack: Python backend, React frontend
- Database: PostgreSQL
- Infrastructure: AWS

BUSINESS:
- Budget: $250K
- ROI timeline: 12 months
- Priority: High

PEOPLE:
- Project Lead: Sarah Johnson
- Team: 5 developers
- Sponsor: CFO

DISTRIBUTION-READY REPORT
Meeting held: 2024-01-15
Key Decision: Approved project go-ahead
Budget Approved: $250,000
Next Steps: Requirements document by Tuesday
Follow-up Meeting: Friday 2PM
```

---

## Advanced Usage Patterns

### Pattern 1: Quality Improvement Cycle

```
1. Upload Document
2. Run Document Agent
3. Review Changes
4. Download Improved Version
5. Re-upload if further improvement needed
6. Run Document Agent again
7. Compare and choose best version
```

### Pattern 2: Multi-Perspective Analysis

```
1. Upload Document
2. Run All Agents Simultaneously (wait for all)
3. Review from Different Angles:
   - Writing Quality (Document Agent)
   - Key Points (Summary Agent)
   - Structured Data (Info Agent)
4. Combine insights for comprehensive review
5. Download Complete Report
```

### Pattern 3: Team Collaboration

```
1. Run all agents on document
2. Download Complete Report
3. Share with team members
4. Each reviews different sections
5. Compile feedback
6. If needed, run agents on revised document
```

### Pattern 4: Batch Project Analysis

```
For 10+ documents:
1. Create processing queue
2. Process documents in batches of 3-4
3. Focus on Summary Agent for speed
4. Save all outputs
5. Compile master summary
```

---

## Best Practices

### Document Preparation

**Do:**
- ✅ Use clear, well-formatted documents
- ✅ Check text is readable (not scanned image)
- ✅ Use proper grammar for better AI results
- ✅ Include relevant headers/sections
- ✅ Keep documents focused on main topic

**Don't:**
- ❌ Use scanned PDFs without OCR
- ❌ Mix multiple unrelated topics
- ❌ Upload corrupted files
- ❌ Use files larger than 50MB
- ❌ Upload binary/executable files

### Processing Strategy

**For Speed:**
1. Start with Summary Agent (fastest)
2. Only run others if needed
3. Use TXT format

**For Quality:**
1. Run all three agents
2. Use original format (PDF/DOCX better preserved)
3. Download individual reports
4. Review each carefully

**For Collaboration:**
1. Use Complete Report download
2. Share with stakeholders
3. Collect feedback
4. Process updated documents

### Output Management

**Do:**
- ✅ Download results immediately
- ✅ Organize by project in folders
- ✅ Date stamp important files
- ✅ Keep originals and improved versions separate
- ✅ Use meaningful filenames

**Don't:**
- ❌ Leave downloads in Downloads folder
- ❌ Overwrite original documents
- ❌ Trust only screen captures
- ❌ Delete important results
- ❌ Store sensitive info in browser cache

---

## FAQ - Common Questions During Use

**Q: How long does processing take?**
A: Usually 15-30 seconds per agent, depends on document size

**Q: Can I process multiple documents at once?**
A: No, process one at a time. Good for Phase 2 enhancement

**Q: What if I don't want to run all agents?**
A: Click only the agents you need. Each works independently

**Q: Can I modify the results before downloading?**
A: Not in current version. Copy-paste to edit manually

**Q: How do I process very long documents?**
A: Split into sections, process each separately, combine

**Q: Can I undo an agent run?**
A: Reload the page or upload document again

**Q: Is my document saved somewhere?**
A: No, all processing is temporary. Download results immediately

**Q: Can I use same API key for multiple instances?**
A: Yes, but may hit rate limits with multiple concurrent users

---

**Ready to use? Start with a simple document and one agent!** 🚀
