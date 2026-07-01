import os
import re
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from duckduckgo_search import DDGS

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini Client using the environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

wiki_structure = {
    "welcome": [
        "Getting Started at NIT Calicut", "About NIT Calicut", "Campus Map of NIT Calicut",
        "Important Contacts at NIT Calicut", "Academic Calendar of NIT Calicut", "Frequently Asked Questions about NIT Calicut"
    ],
    "academics": [
        "Academics at NIT Calicut", "Departments of NIT Calicut", "Academic Programs at NIT Calicut",
        "Curriculum and Syllabus at NIT Calicut", "Course Reviews at NIT Calicut", "Elective Courses at NIT Calicut",
        "Professors at NIT Calicut", "CGPA and Grading System at NIT Calicut", "Academic Regulations of NIT Calicut",
        "Course Registration at NIT Calicut", "Examinations at NIT Calicut", "Previous Year Question Papers of NIT Calicut",
        "Academic Resources at NIT Calicut"
    ],
    "hostels": [
        "Hostels at NIT Calicut", "Boys' Hostels at NIT Calicut", "Girls' Hostels at NIT Calicut",
        "Hostel Allocation at NIT Calicut", "Hostel Facilities at NIT Calicut", "Hostel Rules at NIT Calicut",
        "Campus Wi-Fi at NIT Calicut", "Laundry Services at NIT Calicut"
    ],
    "student_life": [
        "Student Life at NIT Calicut", "Student Clubs at NIT Calicut", "Technical Teams at NIT Calicut",
        "Student Chapters at NIT Calicut", "Cultural Activities at NIT Calicut", "Sports Facilities at NIT Calicut",
        "Student Council of NIT Calicut", "Events at NIT Calicut", "Annual Festivals of NIT Calicut"
    ],
    "dining": [
        "Food and Dining at NIT Calicut", "Messes at NIT Calicut", "Canteens at NIT Calicut",
        "Cafés at NIT Calicut", "Night Food at NIT Calicut", "Nearby Restaurants for NIT Calicut Students"
    ],
    "career": [
        "Placements at NIT Calicut", "Career Development Centre of NIT Calicut", "Internships at NIT Calicut",
        "Placement Process at NIT Calicut", "Placement Statistics of NIT Calicut", "Interview Experiences at NIT Calicut"
    ],
    "research": [
        "Research at NIT Calicut", "Research Laboratories at NIT Calicut", "Faculty Research at NIT Calicut",
        "Student Research Opportunities at NIT Calicut", "Research Projects at NIT Calicut", "Research Publications of NIT Calicut"
    ],
    "services": [
        "Campus Services at NIT Calicut", "Central Library of NIT Calicut", "Health Centre at NIT Calicut",
        "Counselling Services at NIT Calicut", "Banking Services at NIT Calicut", "Printing Services at NIT Calicut",
        "Transportation at NIT Calicut"
    ],
    "resources": [
        "Study Resources for NIT Calicut Students", "Notes for NIT Calicut Courses", "Books for NIT Calicut Courses",
        "Software Available to NIT Calicut Students", "Programming Resources for NIT Calicut Students"
    ],
    "surroundings": [
        "Living Near NIT Calicut", "Transportation to NIT Calicut", "Railway Station Near NIT Calicut",
        "Airport Near NIT Calicut", "Shopping Near NIT Calicut", "Hospitals Near NIT Calicut", "Rentals Near NIT Calicut"
    ],
    "infrastructure": [
        "Buildings at NIT Calicut", "Academic Buildings at NIT Calicut", "Lecture Halls at NIT Calicut",
        "Laboratories at NIT Calicut", "Sports Complex at NIT Calicut", "Gymnasium at NIT Calicut",
        "Auditorium at NIT Calicut", "Open Air Theatre at NIT Calicut"
    ],
    "it_services": [
        "Technology Services at NIT Calicut", "ERP Portal of NIT Calicut", "Learning Management System of NIT Calicut",
        "Email Services at NIT Calicut", "VPN Access at NIT Calicut"
    ],
    "admissions": [
        "Admissions to NIT Calicut", "B.Tech Admissions at NIT Calicut", "M.Tech Admissions at NIT Calicut",
        "MBA Admissions at NIT Calicut", "MCA Admissions at NIT Calicut", "PhD Admissions at NIT Calicut",
        "Scholarships at NIT Calicut", "Fee Structure of NIT Calicut"
    ],
    "achievements": [
        "Achievements of NIT Calicut", "Student Achievements at NIT Calicut", "Faculty Achievements at NIT Calicut",
        "Research Achievements of NIT Calicut"
    ],
    "culture": [
        "Traditions of NIT Calicut", "Freshers' Guide to NIT Calicut", "Graduation at NIT Calicut",
        "Student Stories from NIT Calicut", "Campus Traditions of NIT Calicut"
    ],
    "community": [
        "Alumni of NIT Calicut", "Open Source Projects at NIT Calicut", "Student Startups from NIT Calicut",
        "Contributing to the NIT Calicut Wiki"
    ]
}

def get_clean_filename(topic_name):
    return topic_name.lower()\
        .replace(" at nit calicut", "").replace(" of nit calicut", "")\
        .replace(" for nit calicut students", "").replace(" near nit calicut", "")\
        .replace(" about nit calicut", "").strip()\
        .replace(" ", "_").replace("'", "") + ".md"

print("🚀 Starting full-scale wiki generation script (DuckDuckGo Bypass Mode)...")

os.makedirs("docs", exist_ok=True)
index_path = os.path.join("docs", "index.md")
if not os.path.exists(index_path):
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("# Welcome to the NITC Wiki\n\nAn automated, comprehensive knowledge base for NIT Calicut.")

failed_topics = []

for category, topics in wiki_structure.items():
    category_dir = os.path.join("docs", category)
    os.makedirs(category_dir, exist_ok=True)
    
    for topic in topics:
        print(f"\n🔄 [{category.upper()}] ➔ Processing: {topic}")
        
        filepath = os.path.join(category_dir, get_clean_filename(topic))
        if os.path.exists(filepath):
            print(f"⏭️ Already exists, skipping: {topic}")
            continue
            
        other_topics = [t for t in topics if t != topic][:3]
        recommendations_markdown = "\n\n## Related Articles\n"
        for ref_topic in other_topics:
            recommendations_markdown += f"- [{ref_topic}]({get_clean_filename(ref_topic)})\n"
            
        # --- NEW DUCKDUCKGO WEB SCRAPER BLOCK ---
        print(f"🔍 Scraping web context for {topic}...")
        web_context = ""
        try:
            raw_results = DDGS().text(f"{topic} NIT Calicut", max_results=3)
            web_context = "\n\n".join([f"Source snippet: {res.get('body', '')}" for res in raw_results])
            print("   ✅ Context retrieved.")
        except Exception as e:
            print(f"   ⚠️ Search failed ({e}), falling back to internal AI memory.")
            web_context = "No recent web context found. Rely entirely on your internal knowledge."
        # ----------------------------------------
            
        prompt = f"""
            Write a factual wiki page about "{topic}".

            This wiki is for students of NIT Calicut.

            Requirements:

            - Only include information that can be verified from reliable public sources.
            - Do NOT invent statistics, facilities, rankings, events, professors, or policies.
            - If information is unavailable, state that instead of guessing.
            - Write in an objective Wikipedia-style tone.
            - Use Markdown.
            - Begin with:

            # {topic}

            Use:
            ## Overview
            ## Details
            ## History (if applicable)
            ## Facilities (if applicable)
            ## Procedures (if applicable)
            ## References

            Whenever explaining a process or hierarchy, use Mermaid diagrams.

            Do not include marketing language.
            Do not include AI disclaimers.
            """
                    
        
        success = False
        attempts_this_topic = 0
        
        while not success and attempts_this_topic < 3:
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        # NATIVE GOOGLE SEARCH TOOL REMOVED HERE
                        temperature=0.2
                    )
                )
                
                generated_text = response.text if response.text is not None else "# Data Missing\n\nAPI returned no text content."
                final_markdown_content = generated_text + recommendations_markdown
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(final_markdown_content)
                    
                print(f"✅ Saved to: {filepath}")
                success = True
                
            except Exception as e:
                err_msg = str(e)
                attempts_this_topic += 1
                
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    print(f"⚠️ Rate limit encountered on attempt {attempts_this_topic}.")
                    
                    match = re.search(r"retry in (\d+\.?\d*)s", err_msg)
                    if match:
                        wait_time = float(match.group(1)) + 2.0  
                    else:
                        wait_time = 45.0  
                        
                    print(f"⏳ API requested cooldown. Sleeping for exact window: {wait_time}s...")
                    time.sleep(wait_time)
                    print("🔄 Resuming compilation sequence...")
                else:
                    print(f"❌ Non-quota compilation error: {err_msg}")
                    failed_topics.append({"category": category, "topic": topic})
                    break 
                    
        if success:
            # Short 12-second delay between successful gens to respect standard text quotas
            time.sleep(12)

if failed_topics:
    print("\n🚨 The following pages completely failed due to non-quota processing errors:")
    for item in failed_topics:
        print(f" - [{item['category'].upper()}] {item['topic']}")
else:
    print("\n🎉 Full wiki compilation successful! Your folder generation is complete.")