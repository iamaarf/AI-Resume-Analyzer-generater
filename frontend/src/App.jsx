import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);
    }
  };


const analyzeResume = async () => {
  if (!file) {
    alert("Please choose a resume first.");
    return;
  }

  setLoading(true);
  setResult(null);

  const formData = new FormData();
  formData.append("file", file);
  formData.append("job_description", jobDescription);

 try {
  const response = await fetch("http://127.0.0.1:8000/analyze-resume", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));

    throw new Error(
      errorData.detail || "Resume analysis failed."
    );
  }

  const data = await response.json();
  setResult(data);

} catch (error) {
  alert(
    error.message ||
    "Could not connect to the Resume Analyzer backend."
  );

  console.error(error);

} finally {
  setLoading(false);
}
};


  return (
    <div className="app">
      {/* NAVBAR */}
      <header className="navbar">
        <div className="logo">
          <span className="logo-icon">R</span>
          ResumeAI
        </div>

        <nav>
          <a href="#home">Home</a>
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
        </nav>

        <div className="navbar-actions">
  <a href="#upload" className="nav-button">
    Analyze Resume
  </a>

  <button
    className="builder-nav-button"
    onClick={() => {
      window.location.href = "/resume-builder";
    }}
  >
    ✨ Create Resume
  </button>
</div>
      </header>

      {/* HERO SECTION */}
      <main>
        <section className="hero" id="home">
          <div className="hero-content">
            <div className="badge">
              ✨ AI-Powered Resume Analyzer
            </div>

            <h1>
              Build a Resume That
              <span> Gets Hired in Jobs👍</span>
            </h1>

            <p className="hero-text">
              Analyze your resume, discover its strengths and weaknesses,
              improve your ATS score, and create a stronger resume for your
              next job application.
            </p>

            <div className="hero-buttons">
              <a href="#upload" className="primary-button">
                📄 Upload Your Resume
              </a>

              <a href="#how-it-works" className="secondary-button">
                See How It Works →
              </a>
            </div>

            <div className="trust-points">
              <span>✓ PDF & DOCX</span>
              <span>✓ ATS Friendly</span>
              <span>✓ Smart Analysis</span>
            </div>
          </div>

          {/* SCORE CARD */}
          <div className="score-card">
            <div className="score-card-top">
              <span>Resume Analysis</span>
              <span className="status">● Ready</span>
            </div>

            <div className="score-circle">
              <div>
                <strong>82</strong>
                <small>/100</small>
              </div>
            </div>

            <h3>Good Resume</h3>
            <p>Your resume has a strong foundation.</p>

            <div className="score-list">
              <div>
                <span>✓ Skills</span>
                <b>Excellent</b>
              </div>

              <div>
                <span>✓ Experience</span>
                <b>Good</b>
              </div>

              <div>
                <span>⚠ Keywords</span>
                <b>Needs Work</b>
              </div>

              <div>
                <span>✓ Formatting</span>
                <b>Excellent</b>
              </div>
            </div>
          </div>
        </section>

        {/* UPLOAD SECTION */}
        <section className="upload-section" id="upload">
          <div className="section-heading">
            <div className="mini-badge">RESUME ANALYSIS</div>

            <h2>Analyze Your Resume</h2>

            <p>
              Upload your resume and get insights about ATS compatibility,
              skills, keywords, formatting and more.
            </p>
          </div>

          <div className="upload-box">
            <div className="upload-icon">📄</div>

            <h3>
              {file ? file.name : "Upload your resume"}
            </h3>

            <p>
              {file
                ? "Your resume is ready for analysis."
                : "Drag & drop your resume here or choose a file"}
            </p>

            <label className="upload-button">
              {file ? "Choose Another Resume" : "Choose Resume"}

              <input
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={handleFileChange}
                hidden
              />
            </label>


{file && (
  <button
    className="analyze-button"
    onClick={analyzeResume}
    disabled={loading}
  >
    {loading ? "Analyzing Resume..." : "Analyze Resume"}
  </button>
)}



            <span className="file-info">
              Supported formats: PDF, DOC, DOCX
            </span>
            <div className="job-description-box">
  <div className="job-description-header">
    <div>
      <span className="job-label">OPTIONAL BUT RECOMMENDED</span>
      <h3>Paste Job Description</h3>
    </div>
    <span className="job-icon">🎯</span>
  </div>

  <p>
    Paste the job description you're applying for. ResumeAI will compare
    your resume with the job requirements and identify matching and missing
    keywords.
  </p>

  <textarea
    value={jobDescription}
    onChange={(e) => setJobDescription(e.target.value)}
    placeholder="Paste the job description here..."
    rows="8"
  />

  <div className="job-description-footer">
    <span>
      {jobDescription.length} characters
    </span>

    <span>
      Job matching will improve your ATS analysis
    </span>
  </div>
</div>

            {result && (
  <div className="result-box">

    {/* RESULT HEADER */}
    <div className="result-header">

      <div>
        <span className="result-label">
          ANALYSIS COMPLETE
        </span>

        <h3>
          Resume Analysis Result
        </h3>

        <p className="result-description">
          Your resume has been analyzed for ATS compatibility,
          structure, contact information and keywords.
        </p>
      </div>

      <div className="score-main">
        <strong>
          {result.ats_analysis?.ats_score ?? 0}
        </strong>

        <span>/100</span>
      </div>

    </div>


    {/* SCORE OVERVIEW */}
    {result.job_match && !jobDescription.trim() && (
  <div className="no-job-description">
    <div className="no-job-description-icon">🎯</div>

    <span className="result-label">JOB MATCH</span>

    <h3>No Job Description Added</h3>

    <p>
      Add a job description to see how well your resume matches the job,
      including required skills, preferred skills and important job terms.
    </p>
  </div>
)}
    
{result.job_match && jobDescription.trim() && (
  <div className="job-match-section">

    {/* JOB MATCH HEADER */}
    <div className="job-match-header">
      <div>
        <span className="result-label">JOB DESCRIPTION MATCH</span>
        <h3>How Well Your Resume Matches This Job</h3>
      </div>

      <div className="job-match-score">
        <strong>{result.job_match.job_match_score}</strong>
        <span>% Match</span>
      </div>
    </div>


    {/* BASIC MATCH STATS */}
    <div className="job-match-stats">

      <div className="job-match-card">
        <span>🎯 Keyword Match</span>
        <strong>
          {result.job_match.keyword_match_score ?? 0}%
        </strong>
      </div>

      <div className="job-match-card">
        <span>📝 Phrase Match</span>
        <strong>
          {result.job_match.phrase_match_score ?? 0}%
        </strong>
      </div>

    </div>


    {/* REQUIREMENT BREAKDOWN */}
    <div className="job-breakdown">

      <div className="job-breakdown-header">
        <h4>📊 Job Match Breakdown</h4>
        <p>
          Required qualifications are given higher importance than preferred
          qualifications.
        </p>
      </div>


      {/* JOB TITLE MATCH */}
<div className="job-title-match">

  <div className="job-title-match-header">
    <div>
      <span className="result-label">JOB TITLE MATCH</span>
      <h4>How Closely Your Resume Fits the Job Role</h4>
    </div>

    <strong>
      {result.job_match.title_match_score ?? 0}%
    </strong>
  </div>

  <div className="breakdown-progress">
    <div
      className="breakdown-progress-fill"
      style={{
        width: `${result.job_match.title_match_score ?? 0}%`,
      }}
    ></div>
  </div>

  <div className="matched-title-list">

    {result.job_match.matched_job_titles?.length > 0 ? (

      result.job_match.matched_job_titles.map((title) => (
        <span
          key={title}
          className="keyword-tag"
        >
          ✓ {title}
        </span>
      ))

    ) : (

      <p>
        No direct job title match detected in the resume.
      </p>

    )}

  </div>

</div>


      {/* REQUIRED */}
      <div className="breakdown-row">

        <div className="breakdown-info">
          <span>🔴(Required Skill Match) These required skills from the job description were found in your resume.</span>
          <strong>
            {result.job_match.required_match_score ?? 0}%
          </strong>
        </div>

        <div className="breakdown-progress">
          <div
            className="breakdown-progress-fill required-fill"
            style={{
              width: `${result.job_match.required_match_score ?? 0}%`,
            }}
          ></div>
        </div>

      </div>


      {/* PREFERRED */}
      <div className="breakdown-row">

        <div className="breakdown-info">
          <span>🟡(Preferred Skills) Additional Skills That Can Help</span>
          <strong>
            {result.job_match.preferred_match_score ?? 0}%
          </strong>
        </div>

        <div className="breakdown-progress">
          <div
            className="breakdown-progress-fill preferred-fill"
            style={{
              width: `${result.job_match.preferred_match_score ?? 0}%`,
            }}
          ></div>
        </div>

      </div>

    </div>


    {/* REQUIRED SKILLS */}
    <div className="requirement-columns">

      <div className="requirement-card required-card">

        <div className="keyword-card-header">
          <h4>✓ Required Skills You Have</h4>

          <span>
            {result.job_match.matched_required_keywords?.length || 0}
          </span>
        </div>

        <div className="keyword-list">

          {result.job_match.matched_required_keywords?.length > 0 ? (

            result.job_match.matched_required_keywords.map((keyword) => (
              <span
                key={keyword}
                className="keyword-tag"
              >
                {keyword}
              </span>
            ))

          ) : (

            <p>No required skills matched.</p>

          )}

        </div>

      </div>


      <div className="requirement-card missing-required-card">

        <div className="keyword-card-header">
          <h4>⚠ Required Skills You May Need to Add</h4>

          <span>
            {result.job_match.missing_required_keywords?.length || 0}
          </span>
        </div>

        <div className="keyword-list">

          {result.job_match.missing_required_keywords?.length > 0 ? (

            result.job_match.missing_required_keywords.map((keyword) => (
              <span
                key={keyword}
                className="keyword-tag"
              >
                {keyword}
              </span>
            ))

          ) : (

            <p>No required skills appear to be missing.</p>

          )}

        </div>

      </div>

    </div>


    {/* PREFERRED SKILLS */}
    <div className="requirement-columns">

      <div className="requirement-card preferred-card">

        <div className="keyword-card-header">
          <h4>✓ Additional Skills You Have</h4>

          <span>
            {result.job_match.matched_preferred_keywords?.length || 0}
          </span>
        </div>

        <div className="keyword-list">

          {result.job_match.matched_preferred_keywords?.length > 0 ? (

            result.job_match.matched_preferred_keywords.map((keyword) => (
              <span
                key={keyword}
                className="keyword-tag"
              >
                {keyword}
              </span>
            ))

          ) : (

            <p>No preferred skills matched.</p>

          )}

        </div>

      </div>


      <div className="requirement-card missing-preferred-card">

        <div className="keyword-card-header">
          <h4>⚠ Additional Skills You Don't Have Yet</h4>

          <span>
            {result.job_match.missing_preferred_keywords?.length || 0}
          </span>
        </div>

        <div className="keyword-list">

          {result.job_match.missing_preferred_keywords?.length > 0 ? (

            result.job_match.missing_preferred_keywords.map((keyword) => (
              <span
                key={keyword}
                className="keyword-tag"
              >
                {keyword}
              </span>
            ))

          ) : (

            <p>No preferred skills appear to be missing.</p>

          )}

        </div>

      </div>

    </div>


    {/* ALL KEYWORDS */}
    <div className="keyword-columns">

      <div className="keyword-card matched">

        <div className="keyword-card-header">
          <h4>✓ Important Job Terms Found in Your Resume</h4>

          <span>
            {result.job_match.matched_keywords?.length || 0}
          </span>
        </div>

        <div className="keyword-list">

          {result.job_match.matched_keywords?.length > 0 ? (

            result.job_match.matched_keywords.map((keyword) => (
              <span
                key={keyword}
                className="keyword-tag"
              >
                {keyword}
              </span>
            ))

          ) : (

            <p>No matching keywords detected.</p>

          )}

        </div>

      </div>


      <div className="keyword-card missing">

        <div className="keyword-card-header">
          <h4>⚠ Important Job Terms Not Found in Your Resume</h4>

          <span>
            {result.job_match.missing_keywords?.length || 0}
          </span>
        </div>

        <div className="keyword-list">

          {result.job_match.missing_keywords?.length > 0 ? (

            result.job_match.missing_keywords.map((keyword) => (
              <span
                key={keyword}
                className="keyword-tag"
              >
                {keyword}
              </span>
            ))

          ) : (

            <p>No important keywords appear to be missing.</p>

          )}

        </div>

      </div>

    </div>

  </div>
)}


{/* EXPERIENCE ANALYSIS */}
{result.experience_analysis?.has_experience && (
  <div className="result-section experience-analysis-section">

    <div className="result-section-header">
      <div>
        <span className="result-label">EXPERIENCE ANALYSIS</span>
        <h3>Experience & Internship Review</h3>
      </div>

      <div className="analysis-score">
        <strong>
          {result.experience_analysis.experience_score ?? 0}
        </strong>
        <span>/100</span>
      </div>
    </div>

    <div className="score-grid">

      <div className="score-item">
        <span>Experience Section</span>
        <strong>
          {result.experience_analysis.section_present ? "Detected" : "Missing"}
        </strong>
      </div>

      <div className="score-item">
        <span>Internship</span>
        <strong>
          {result.experience_analysis.internship_detected ? "Detected" : "Not Detected"}
        </strong>
      </div>

      <div className="score-item">
        <span>Roles Detected</span>
        <strong>
          {result.experience_analysis.entries?.length ?? 0}
        </strong>
      </div>

      <div className="score-item">
        <span>Bullet Points</span>
        <strong>
          {result.experience_analysis.bullet_count ?? 0}
        </strong>
      </div>


      <div className="score-item">
        <span>Job Relevance</span>
        <strong>
          {result.experience_analysis.job_relevance_score ?? 0}%
        </strong>
      </div>

    </div>

    {/* DETECTED EXPERIENCE ENTRIES */}
    {result.experience_analysis.entries?.length > 0 && (
      <div className="result-subsection">

        <h4 className="result-section-title">
          💼 Detected Experience / Internship Entries
        </h4>

        {result.experience_analysis.entries.map((entry, index) => (
          <div className="result-point" key={index}>
            • {entry}
          </div>
        ))}

      </div>
    )}

    {/* ACTION VERBS */}
    {result.experience_analysis.action_verbs_detected?.length > 0 && (
      <div className="result-subsection">

        <h4 className="result-section-title">
          ⚡ Action Verbs Detected
        </h4>

        <div className="result-list">
          {result.experience_analysis.action_verbs_detected.map(
            (verb, index) => (
              <span className="result-tag" key={index}>
                {verb}
              </span>
            )
          )}
        </div>

      </div>
    )}

    {/* STRENGTHS */}
    {result.experience_analysis.strengths?.length > 0 && (
      <div className="result-subsection">

        <h4 className="result-section-title">
          💪 Experience Strengths
        </h4>

        {result.experience_analysis.strengths.map(
          (strength, index) => (
            <div className="result-point" key={index}>
              ✓ {strength}
            </div>
          )
        )}

      </div>
    )}

    {/* WEAKNESSES */}
    {result.experience_analysis.weaknesses?.length > 0 && (
      <div className="result-subsection">

        <h4 className="result-section-title">
          ⚠️ Experience Issues
        </h4>

        {result.experience_analysis.weaknesses.map(
          (weakness, index) => (
            <div className="result-point" key={index}>
              ⚠️ {weakness}
            </div>
          )
        )}

      </div>
    )}

       </div>

  
)}

{/* PROJECT ANALYSIS */}
{result.project_analysis?.has_projects && (
  <div className="result-section project-analysis-section">

    <div className="section-header">
      <div>
        <span className="result-label">PROJECT ANALYSIS</span>
        <h3>🚀 Project Review</h3>
      </div>

      <div className="section-score">
        <strong>
          {result.project_analysis.project_score ?? 0}/100
        </strong>
      </div>
    </div>

    {/* PROJECT SCORE */}
    <div className="score-grid">

      <div className="score-item">
        <span>📁Your Projects</span>
        <strong>
          {result.project_analysis.project_count ?? 0}
        </strong>
      </div>


      <div className="score-item">
        <span>🛠️ Technologies Used</span>
        <strong>
          {result.project_analysis.technologies_detected?.length ?? 0}
        </strong>
      </div>

      <div className="score-item">
        <span>📊 Metrics</span>
        <strong>
          {result.project_analysis.metrics_detected?.length ?? 0}
        </strong>
      </div>

    </div>

    {/* DETECTED PROJECTS */}
    {result.project_analysis.projects?.length > 0 && (
      <div className="keyword-section">

        <div className="keyword-card-header">
          <h4>📌 Detected Projects from Your Resume.</h4>
          <span>
            {result.project_analysis.projects.length}
          </span>
        </div>

        <div className="keyword-list">
          {result.project_analysis.projects.map((project, index) => (
            <span
              key={`${project}-${index}`}
              className="keyword-tag"
            >
              {project}
            </span>
          ))}
        </div>

      </div>
    )}

    {/* TECHNOLOGIES USED IN PROJECT */}
    {result.project_analysis.technologies_detected?.length > 0 && (
      <div className="keyword-section">

        <div className="keyword-card-header">
          <h4>🛠️ Technologies & Tools</h4>
        </div>

        <div className="keyword-list">
          {result.project_analysis.technologies_detected.map(
            (technology) => (
              <span
                key={technology}
                className="keyword-tag"
              >
                {technology}
              </span>
            )
          )}
        </div>

      </div>
    )}

    {/* ACTION VERBS */}
    {result.project_analysis.action_verbs_detected?.length > 0 && (
      <div className="keyword-section">

        <div className="keyword-card-header">
          <h4>⚡ Action Verbs</h4>
        </div>

        <div className="keyword-list">
          {result.project_analysis.action_verbs_detected.map(
            (verb) => (
              <span
                key={verb}
                className="keyword-tag"
              >
                {verb}
              </span>
            )
          )}
        </div>

      </div>
    )}

    {/* METRICS */}
    {result.project_analysis.metrics_detected?.length > 0 && (
      <div className="keyword-section">

        <div className="keyword-card-header">
          <h4>📈 Measurable Results</h4>
        </div>

        <div className="keyword-list">
          {result.project_analysis.metrics_detected.map(
            (metric, index) => (
              <span
                key={`${metric}-${index}`}
                className="keyword-tag"
              >
                {metric}
              </span>
            )
          )}
        </div>

      </div>
    )}

    {/* STRENGTHS */}
    {result.project_analysis.strengths?.length > 0 && (
      <div className="analysis-card success-card">

        <h4>💪 Project Strengths</h4>

        <ul>
          {result.project_analysis.strengths.map(
            (strength, index) => (
              <li key={index}>{strength}</li>
            )
          )}
        </ul>

      </div>
    )}

    {/* WEAKNESSES */}
    {result.project_analysis.weaknesses?.length > 0 && (
      <div className="analysis-card warning-card">

        <h4>⚠️ Project Weaknesses</h4>

        <ul>
          {result.project_analysis.weaknesses.map(
            (weakness, index) => (
              <li key={index}>{weakness}</li>
            )
          )}
        </ul>

      </div>
    )}

    {/* PROJECT RECOMMENDATIONS */}
    {result.project_analysis.recommendations?.length > 0 && (
      <div className="analysis-card recommendation-card">

        <h4>💡 Project Recommendations</h4>

        <ul>
          {result.project_analysis.recommendations.map(
            (recommendation, index) => (
              <li key={index}>{recommendation}</li>
            )
          )}
        </ul>

      </div>
    )}

  </div>
)}



{/* EDUCATION ANALYSIS */}
{result.education_analysis && (
  <div className="result-section education-analysis-section">

    <div className="result-section-header">
      <div>
        <span className="result-label">EDUCATION ANALYSIS</span>
        <h3>Education & Academic Review</h3>
      </div>

      <div className="analysis-score">
        <strong>
          {result.education_analysis.education_score ?? 0}
        </strong>
        <span>/100</span>
      </div>
    </div>

    <div className="score-grid">

      <div className="score-item">
        <span>Education Section</span>
        <strong>
          {result.education_analysis.section_present
            ? "Detected"
            : "Missing"}
        </strong>
      </div>

      <div className="score-item">
        <span>Degrees Detected From Your Resume.</span>
        <strong>
          {result.education_analysis.degrees?.length ?? 0}
        </strong>
      </div>

      <div className="score-item">
        <span>Institutions</span>
        <strong>
          {result.education_analysis.institutions?.length ?? 0}
        </strong>
      </div>

      <div className="score-item">
        <span>Dates Detected</span>
        <strong>
          {result.education_analysis.dates_detected?.length ?? 0}
        </strong>
      </div>

      <div className="score-item">
        <span>Relevant Keywords</span>
        <strong>
          {result.education_analysis.relevant_keywords?.length ?? 0}
        </strong>
      </div>

      

    </div>


    {/* DETECTED DEGREES From Your Resume.*/}
    {result.education_analysis.degrees?.length > 0 && (
      <div className="result-subsection">

        <h4 className="result-section-title">
          🎓 Degrees / Qualifications Detected
        </h4>

        {result.education_analysis.degrees.map(
          (degree, index) => (
            <div className="result-point" key={index}>
              • {degree}
            </div>
          )
        )}

      </div>
    )}


    {/* INSTITUTIONS */}
    {result.education_analysis.institutions?.length > 0 && (
      <div className="result-subsection">

        <h4 className="result-section-title">
          🏫 Institutions Detected From Your Resume.
        </h4>

        {result.education_analysis.institutions.map(
          (institution, index) => (
            <div className="result-point" key={index}>
              • {institution}
            </div>
          )
        )}

      </div>
    )}


    {/* STRENGTHS */}
    {result.education_analysis.strengths?.length > 0 && (
      <div className="result-subsection">

        <h4 className="result-section-title">
          💪 Education Strengths
        </h4>

        {result.education_analysis.strengths.map(
          (strength, index) => (
            <div className="result-point" key={index}>
              ✓ {strength}
            </div>
          )
        )}

      </div>
    )}


    {/* WEAKNESSES */}
    {result.education_analysis.weaknesses?.length > 0 && (
      <div className="result-subsection">

        <h4 className="result-section-title">
          ⚠️ Education Issues
        </h4>

        {result.education_analysis.weaknesses.map(
          (weakness, index) => (
            <div className="result-point" key={index}>
              ⚠️ {weakness}
            </div>
          )
        )}

      </div>
    )}
      




  </div>
      
)}
      <div className="score-grid">




      <div className="score-item">
        <span>📑 Sections</span>
        <strong>
          {result.ats_analysis?.section_score ?? 0}/100
        </strong>
      </div>

      <div className="score-item">
        <span>📞 Contact</span>
        <strong>
          {result.ats_analysis?.contact_score ?? 0}/100
        </strong>
      </div>

      <div className="score-item">
        <span>🔑 Keywords</span>
        <strong>
          {result.ats_analysis?.keyword_score ?? 0}/100
        </strong>

        <div className="score-progress">
  <div
    className="score-progress-fill"
    style={{
      width: `${result.ats_analysis?.section_score ?? 0}%`,
    }}
  ></div>
</div>



      </div>

      <div className="score-item">
        <span>📄 Characters</span>
        <strong>
          {result.characters ?? 0}
        </strong>
      </div>
      </div>
            
            

    

    {/* PERSONAL INFORMATION */}
    {result.ats_analysis?.personal_information && (
      <div className="result-section">

        <h4 className="result-section-title">
          👤 Personal Information
        </h4>

        <div className="score-grid">

          <div className="score-item">
            <span>📧 Email</span>
            <strong>
              {result.ats_analysis.personal_information.email || "Not detected"}
            </strong>
          </div>

          <div className="score-item">
            <span>📱 Phone</span>
            <strong>
              {result.ats_analysis.personal_information.phone || "Not detected"}
            </strong>
          </div>

          <div className="score-item">
            <span>💼 LinkedIn</span>
            <strong>
              {result.ats_analysis.personal_information.linkedin
                ? "Detected"
                : "Not detected"}
            </strong>
          </div>

          <div className="score-item">
            <span>💻 GitHub</span>
            <strong>
              {result.ats_analysis.personal_information.github
                ? "Detected"
                : "Not detected"}
            </strong>
          </div>

        </div>

      </div>
    )}


    {/* RESUME SECTIONS */}
    {result.ats_analysis?.found_sections?.length > 0 && (
      <div className="result-section">

        <h4 className="result-section-title">
          📚 Resume Sections Detected
        </h4>

        <div className="result-list">

          {result.ats_analysis.found_sections.map(
            (section, index) => (
              <span className="result-tag" key={index}>
                ✓ {section}
              </span>
            )
          )}

        </div>

      </div>
    )}


    {/* KEYWORDS */}
    {result.ats_analysis?.found_keywords?.length > 0 && (
      <div className="result-section">

        <h4 className="result-section-title">
          🔑 Skills & Keywords Detected
        </h4>

        <div className="result-list">

          {result.ats_analysis.found_keywords.map(
            (keyword, index) => (
              <span className="result-tag" key={index}>
                {keyword}
              </span>
            )
          )}

        </div>

      </div>
    )}


    {/* STRENGTHS */}
    {result.ats_analysis?.strengths?.length > 0 && (
      <div className="result-section">

        <h4 className="result-section-title">
          💪 Resume Strengths
        </h4>

        {result.ats_analysis.strengths.map(
          (strength, index) => (
            <div className="result-point" key={index}>
              ✓ {strength}
            </div>
          )
        )}

      </div>
    )}


    {/* WEAKNESSES */}
    {result.ats_analysis?.weaknesses?.length > 0 && (
      <div className="result-section">

        <h4 className="result-section-title">
          ⚠️ Areas That Need Improvement
        </h4>

        {result.ats_analysis.weaknesses.map(
          (weakness, index) => (
            <div className="result-point" key={index}>
              ⚠️ {weakness}
            </div>
          )
        )}

      </div>
    )}
        {/* RECOMMENDATIONS */}
    {(
      result.ats_analysis?.recommendations?.length > 0 ||
      result.experience_analysis?.recommendations?.length > 0 ||
      result.education_analysis?.recommendations?.length > 0 ||
      result.project_analysis?.recommendations?.length > 0 ||
      result.job_match?.missing_required_keywords?.length > 0
    ) && (
      <div className="result-section recommendations-section">

        <div className="result-section-header">
          <div>
            <span className="result-label">RECOMMENDATIONS</span>
            <h3>💡 How to Improve Your Resume</h3>
          </div>
        </div>


        {/* HIGH PRIORITY */}
        {(
          result.ats_analysis?.recommendations?.length > 0 ||
          result.job_match?.missing_required_keywords?.length > 0
        ) && (
          <div className="recommendation-group high-priority">

            <h4>🔴 High Priority</h4>

            {result.ats_analysis?.recommendations?.map(
              (recommendation, index) => (
                <div className="result-point" key={`ats-${index}`}>
                  💡 {recommendation}
                </div>
              )
            )}

            {result.job_match?.missing_required_keywords?.length > 0 && (
              <div className="result-point">
                🎯 Review missing required job skills:
                {" "}
                {result.job_match.missing_required_keywords.join(", ")}
              </div>
            )}

          </div>
        )}


        {/* MEDIUM PRIORITY */}
        {(
          result.experience_analysis?.recommendations?.length > 0 ||
          result.education_analysis?.recommendations?.length > 0
        ) && (
          <div className="recommendation-group medium-priority">

            <h4>🟡 Medium Priority</h4>

            {result.experience_analysis?.recommendations?.map(
              (recommendation, index) => (
                <div className="result-point" key={`experience-${index}`}>
                  💼 {recommendation}
                </div>
              )
            )}

            {result.education_analysis?.recommendations?.map(
              (recommendation, index) => (
                <div className="result-point" key={`education-${index}`}>
                  🎓 {recommendation}
                </div>
              )
            )}

          </div>
        )}


        {/* GOOD TO IMPROVE */}
        {result.project_analysis?.recommendations?.length > 0 && (
          <div className="recommendation-group good-to-improve">

            <h4>🟢 Good to Improve</h4>

            {result.project_analysis.recommendations.map(
              (recommendation, index) => (
                <div className="result-point" key={`project-${index}`}>
                  🚀 {recommendation}
                </div>
              )
            )}

          </div>
        )}

      </div>
    )}


   


          </div>
            )}
          </div>
        </section>

        {/* FEATURES */}
        <section className="features-section" id="features">
          <div className="section-heading">
            <div className="mini-badge">POWERFUL FEATURES</div>

            <h2>Everything You Need to Improve Your Resume</h2>

            <p>
              Get useful insights before sending your resume to your next
              employer.
            </p>
          </div>

          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>ATS Score</h3>
              <p>
                Understand how well your resume is prepared for ATS screening
                systems.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🔍</div>
              <h3>Resume Analysis</h3>
              <p>
                Identify missing information, weak sections and areas that
                need improvement.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🔑</div>
              <h3>Keyword Analysis</h3>
              <p>
                Find important keywords that can make your resume more
                relevant to a job description.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">✨</div>
              <h3>Resume Enhancement</h3>
              <p>
                Improve your resume content and create a cleaner,
                professional version.
              </p>
            </div>
          </div>
        </section>

        {/* HOW IT WORKS */}
        <section className="how-section" id="how-it-works">
          <div className="section-heading">
            <div className="mini-badge">HOW IT WORKS</div>

            <h2>Improve Your Resume in 3 Simple Steps</h2>
          </div>

          <div className="steps">
            <div className="step">
              <div className="step-number">01</div>
              <h3>Upload Resume</h3>
              <p>
                Upload your existing PDF or DOCX resume.
              </p>
            </div>

            <div className="step">
              <div className="step-number">02</div>
              <h3>Get Analysis</h3>
              <p>
                Our system analyzes your resume and provides a detailed score.
              </p>
            </div>

            <div className="step">
              <div className="step-number">03</div>
              <h3>Improve & Generate</h3>
              <p>
                Get recommendations and create an improved resume.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer>
        <div className="logo">
          <span className="logo-icon">R</span>
          ResumeAI
        </div>

        <p>Smart Resume Analysis for Better Career Opportunities.
          Use it and get hired.👍
        </p>

        <span>© 2026 ResumeAI. All rights reserved.</span>
      </footer>
    </div>
  );
}

export default App;